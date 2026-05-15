import unittest
import numpy as np
from PIL import Image
import os
from app import prepare_image, breed_labels

class TestDogIdentifier(unittest.TestCase):



    def test_image_preprocessing_shape(self):
        test_img = Image.new('RGB', (500, 500), color='red')
        processed = prepare_image(test_img)
        self.assertEqual(processed.shape, (1, 224, 224, 3))



    # Test 4: Handling RGBA (Transparency)
    def test_rgba_conversion(self):
        """Ensures images with alpha channels are converted to 3-channel RGB"""
        rgba_img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        processed = prepare_image(rgba_img)
        # Check that the last dimension is 3 (RGB), not 4 (RGBA)
        self.assertEqual(processed.shape[3], 3, "Failed to convert RGBA to RGB")

    # Test 5: Extreme Aspect Ratio (Panoramas or Vertical shots)
    def test_extreme_dimensions(self):
        """Ensures very thin or wide images still result in 224x224"""
        wide_img = Image.new('RGB', (1000, 100), color='blue')
        processed = prepare_image(wide_img)
        self.assertEqual(processed.shape[1:3], (224, 224), "Failed to resize wide image")

    # Test 6: Image Normalization Range
   

if __name__ == '__main__':
    unittest.main()