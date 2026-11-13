import easyocr
import cv2
import time
import os
import numpy as np


def trim_pure_black(image_path, output_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Find all pixels where the sum of channels is greater than 0
    # (i.e., any pixel that isn't completely black)
    mask = img.sum(axis=2) > 0
    
    # Get the coordinates of these non-black pixels
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    # Find the bounding box edges
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    
    # Crop the image using slicing
    cropped_img = img[ymin:ymax+1, xmin:xmax+1]
    
    # Save the result
    cv2.imwrite(output_path, cropped_img)

# Open the OBS Virtual Camera. 
# 0 is usually the default webcam. If you have an internal webcam, try 1, 2, or -1.
cap = cv2.VideoCapture(0)
# Initialize the EasyOCR reader for English
reader = easyocr.Reader(['en'], gpu=True)
count = 0
output_folder_name  = "pikmin_frames"
cwd = os.getcwd()
output_folder = os.path.join(cwd, output_folder_name)
os.makedirs(output_folder, exist_ok=True)  # Creates folder if it doesn't exist

if not cap.isOpened():
    print("Error: Could not open OBS Virtual Camera.")
    exit()

try:
    while True:
        # Read a single frame from the OBS stream
        # frame = cv2.imread("cropped_output_2.jpg")
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame.")
            break

        mask = frame.sum(axis=2) > 0
    
        # Get the coordinates of these non-black pixels
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        # Find the bounding box edges
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
    
    # Crop the image using slicing
        cropped_img = frame[ymin:ymax+1, xmin:xmax+1]
        # Display the frame in a window
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # _, frame = cv2.threshold(frame, 100, 200, cv2.THRESH_BINARY)
        alpha = 1.5  # Contrast control (1.0-3.0)
        beta = 0    # Brightness control (0-100)
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        cv2.imshow('OBS Frame Reader', frame)
        # trim_pure_black(frame, frame)

        # gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        results = reader.readtext(frame, allowlist='0123456789')
        # Print the extracted text
        for bbox, text, prob in results:
            print(f'Detected: {text} (Confidence: {prob:.2f})')

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(5)
        # count += 1
finally:
    # Always clean up and release the camera resource
    cap.release()
    cv2.destroyAllWindows()