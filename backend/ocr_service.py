import os
import cv2
import pytesseract
from PIL import Image
import numpy as np
import uuid

def extract_text_from_image(image_path, lang='eng'):
    try:
        # Load image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Denoise
        gray = cv2.medianBlur(gray, 3)

        # Threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Optional dilation
        kernel = np.ones((1, 1), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        # Save temporary image with unique name
        temp_filename = f"temp_ocr_{uuid.uuid4().hex}.png"
        cv2.imwrite(temp_filename, dilated)

        # OCR
        text = pytesseract.image_to_string(Image.open(temp_filename), lang=lang)

        # Cleanup
        os.remove(temp_filename)

        return text.strip()

    except Exception as e:
        print(f"[OCR ERROR]: {e}")
        return ""
