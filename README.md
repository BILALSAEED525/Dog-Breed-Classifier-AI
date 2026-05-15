---
title: Dog Classifier
emoji: 🐶
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
---

# 🐶 Dog Breed Identifier

A full-stack AI-powered web application that identifies dog breeds from uploaded images using a fine-tuned **ResNet50V2** deep learning model.

> **Original Repository Credit:**  
> This project is built upon and modified from the original Kaggle Dog Breed Identification dataset and base model. All changes are documented below.

---

## 👤 Author

**Tawsif Mayaz**  
Computer Engineering student at the University of Waterloo | Self-taught Developer

[![GitHub](https://img.shields.io/badge/GitHub-tawsifrm-181717?style=flat&logo=github)](https://github.com/tawsifrm)
[![Portfolio](https://img.shields.io/badge/Portfolio-tawsifrm.netlify.app-orange?style=flat&logo=netlify)](https://tawsifrm.netlify.app/)
[![Email](https://img.shields.io/badge/Email-tawsifmayaz@gmail.com-red?style=flat&logo=gmail)](mailto:tawsifmayaz@gmail.com)

---

## 🌐 Live Demo

- **Hugging Face Deployment:** `[https://huggingface.co/spaces/bilalsaeed5439/Dog-Classifier]`
- **GitHub Repository:** [https://github.com/BILALSAEED525](https://github.com/BILALSAEED525/Dog-Breed-Classifier-AI)

---

## 📌 Project Overview

The Dog Breed Identifier takes an image of a dog as input and predicts its breed from **120 possible breeds**. The frontend allows users to drag and drop (or browse) an image, which is then sent to a Flask REST API backend. The backend runs the image through the ResNet50V2 model and returns the predicted breed as a JSON response.

---

## ✨ Features

- 🖼️ Drag-and-drop image upload with live preview
- 🧠 ResNet50V2 deep learning model (pre-trained on ImageNet, fine-tuned on 120 dog breeds)
- ⚡ Real-time breed prediction via REST API
- 🧵 **Multi-threading** — prediction logging runs in a background thread so the user gets instant results
- 📋 Background logging saves every prediction to `prediction_log.txt`
- ✅ Error handling for missing files, invalid formats, and server errors
- 🧪 Unit tests using Python's `unittest` framework

---

## 🗂️ Project Structure

```
Dog-Breed-Identifier/
│
├── app.py                    # Flask backend API
├── dog-breed-identification.py  # Original model training script
├── testing.py                # Unit tests (unittest framework)
├── index.html                # Frontend UI (HTML + Tailwind CSS + Vanilla JS)
├── labels.csv                # Breed labels mapped to image IDs
├── prediction_log.txt        # Auto-generated log of all predictions (threading)
│
├── model/                    # Saved ResNet50V2 model
│   ├── saved_model.pb
│   └── variables/
│
├── train/                    # Training images (120 dog breed subfolders)
└── test/                     # Test images (3 sample dog photos)
```

---

## ⚙️ Tech Stack

| Layer                | Technology                                    |
| -------------------- | --------------------------------------------- |
| **Frontend**         | HTML5, Tailwind CSS (CDN), Vanilla JavaScript |
| **Backend**          | Python, Flask, Flask-CORS                     |
| **AI Model**         | TensorFlow 2.x, Keras, ResNet50V2             |
| **Image Processing** | Pillow (PIL), NumPy                           |
| **Data Handling**    | Pandas                                        |
| **Concurrency**      | Python `threading` module                     |
| **Testing**          | Python `unittest`, Postman                    |

---

## 🚀 How to Run Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/tawsifrm/Dog-Breed-Identifier.git
cd Dog-Breed-Identifier
```

### Step 2: Install Dependencies

```bash
pip install Flask Flask-Cors Pillow tensorflow numpy pandas
```

### Step 3: Start the Backend Server

```bash
python app.py
```

Wait until you see:

```
Loading model...
Loaded 120 breeds successfully.
* Running on http://127.0.0.1:5000
```

### Step 4: Open the Frontend

Double-click `index.html` to open it in your browser (Chrome or Edge recommended).

### Step 5: Use the App

1. Drag & drop a dog image into the upload zone (or click to browse)
2. Click **"Identify Breed"**
3. The predicted breed appears on screen instantly

---

## 🔌 API Endpoint

### `POST /predict`

Sends a dog image to the model and returns the predicted breed.

**Request:**

- Method: `POST`
- Body: `form-data`
- Key: `file` (type: File)
- Value: A JPG, PNG, or WEBP image of a dog

**Successful Response:**

```json
{
  "success": true,
  "breed": "german_shepherd"
}
```

**Error Response:**

```json
{
  "error": "No file uploaded"
}
```

---

## 🧵 Threading Implementation

When a prediction is made, a **background thread** is launched to log the result to `prediction_log.txt`. This means the user receives their answer **immediately** without waiting for file I/O to complete.

```python
log_thread = threading.Thread(target=log_prediction, args=(predicted_breed,))
log_thread.start()
# User gets response instantly while the thread writes to disk in parallel
```

---

## 🧪 Running Unit Tests

```bash
python testing.py
```

The test suite covers:

| Test                             | Description                                                           |
| -------------------------------- | --------------------------------------------------------------------- |
| `test_image_preprocessing_shape` | Verifies output is (1, 224, 224, 3)                                   |
| `test_rgba_conversion`           | Ensures 4-channel PNG images are converted to 3-channel RGB           |
| `test_extreme_dimensions`        | Ensures panoramic or vertical images are correctly resized to 224×224 |
| `test_preprocessing_values`      | Verifies pixel values are normalized (not raw 0–255)                  |

---

## 🔄 Changes Made from Original Repository

1. **Keras 3 Compatibility Fix:** Replaced deprecated `tf.keras.models.load_model()` with `tf.keras.layers.TFSMLayer()` to support the newer SavedModel format.

2. **Flask REST API:** Created a new `app.py` file wrapping the original prediction logic into a web server with a `/predict` route.

3. **Label Fix (120 Breeds):** Fixed a label misalignment bug — the original code loaded only some breeds; updated to load all 120 breeds sorted alphabetically to match the model's output layer.

4. **Threading:** Added Python `threading` module to run prediction logging in the background without blocking API responses.

5. **Custom Frontend:** Built a responsive, modern UI with drag-and-drop upload, image preview, loading spinner, and animated result card.

6. **Unit Tests:** Created `testing.py` with 4 test cases covering image preprocessing edge cases.

---

## ⚠️ Limitations

- The model runs on **CPU only** (no GPU required), so predictions may take 1–3 seconds.
- Accuracy is limited by the quality and variety of the training dataset.
- The app currently identifies a single dog per image (no multi-dog detection).
- On Hugging Face free tier, the app may go to **sleep** after 48 hours of inactivity and take ~1–2 minutes to wake up.

---

## 🔮 Future Work

- Deploy to Hugging Face Spaces using Docker
- Add confidence percentage display alongside the breed name
- Support multi-dog detection using bounding boxes
- Add a breed history page showing past predictions from the log file
- Improve accuracy by fine-tuning on a larger, more diverse dataset

---

## 📄 License

This project is for **educational purposes** as part of a university course assignment.  
Original dataset: [Kaggle Dog Breed Identification](https://www.kaggle.com/c/dog-breed-identification)
