import os
import threading
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import tensorflow as tf

# 1. Initialize the Flask App
app = Flask(__name__)
CORS(app)

# --- THREADING WORKER FUNCTION ---
def log_prediction(breed):
    """Saves the prediction to a text file in the background."""
    try:
        with open("prediction_log.txt", "a") as f:
            f.write(f"Predicted: {breed}\n")
        print(f" Background Log updated: {breed}")
    except Exception as e:
        print(f"Failed to write log: {e}")

# 2. Load the pre-trained model and labels
print("Loading model...")
model = tf.keras.layers.TFSMLayer('model', call_endpoint='serving_default')

print("Loading labels...")
labels_df = pd.read_csv('labels.csv')

# Get all 120 unique breeds and sort them alphabetically
breed_labels = sorted(labels_df['breed'].unique().tolist())
print(f"Loaded {len(breed_labels)} breeds successfully.")

# 3. Helper function to format the image
def prepare_image(image, target_size=(224, 224)):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    
    # ResNet50V2 specific preprocessing
    img_array = tf.keras.applications.resnet_v2.preprocess_input(img_array)
    return img_array

# 4. Create the API Route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Open and Prepare the image
        image = Image.open(file.stream)
        processed_image = prepare_image(image)
        
        # Make the prediction
        predictions_dict = model(processed_image)   
        predictions = list(predictions_dict.values())[0].numpy()
        predicted_index = np.argmax(predictions, axis=1)[0]
        
        # Get the actual breed name
        predicted_breed = breed_labels[predicted_index]

        # --- THREADING CONCEPT APPLIED ---
        # We start a new thread to handle the file writing (I/O task) 
        # so the user doesn't have to wait for the hard drive to spin up.
        log_thread = threading.Thread(target=log_prediction, args=(predicted_breed,))
        log_thread.start()
        
        # Return the result immediately
        return jsonify({
            'success': True,
            'breed': str(predicted_breed)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 5. Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)