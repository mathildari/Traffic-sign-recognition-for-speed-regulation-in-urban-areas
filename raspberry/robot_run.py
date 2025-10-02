"""
Run the robot loop:
- Capture image with Picamera2
- Detect circle (Hough)
- Crop/resize to 100x100
- Flatten RGB and classify with models/knn.joblib
- Map class label to motor duties and drive
"""
import time
from pathlib import Path

import cv2
import numpy as np
import joblib

from tsr.features import image_array_to_rgb_list
from raspberry.motor import Motor
from raspberry.speed_profiles import duty_tuple
from raspberry.camera_still import capture_to

IMG_PATH = Path("/home/pi/TIPE/image.jpg")  # you can change this path

def detect_crop(img_bgr: np.ndarray):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=150, param2=40, minRadius=80, maxRadius=150)
    if circles is None:
        return None
    circles = np.uint16(np.around(circles))
    x, y, r = circles[0, :][0]  # take first
    # bounding box with small expansion
    expansion = 15
    x0 = max(x - r - expansion, 0)
    y0 = max(y - r - expansion, 0)
    x1 = min(x + r + expansion, img_bgr.shape[1])
    y1 = min(y + r + expansion, img_bgr.shape[0])
    crop = img_bgr[y0:y1, x0:x1]
    if crop.size == 0:
        return None
    crop = cv2.resize(crop, (100, 100), interpolation=cv2.INTER_AREA)
    return crop

def main():
    bundle = joblib.load("models/knn.joblib")
    clf = bundle["model"]; classes = bundle["classes"]

    motor = Motor()
    print("Robot loop started. Ctrl+C to stop.")

    try:
        while True:
            # 1) Capture
            capture_to(str(IMG_PATH))
            img = cv2.imread(str(IMG_PATH))

            # 2) Detect & crop
            crop = detect_crop(img)
            if crop is None:
                print("No circle detected; stopping motors for safety.")
                motor.setMotorModel(0, 0, 0, 0)
                time.sleep(0.2)
                continue

            # 3) Classify
            feat = np.array([image_array_to_rgb_list(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))], dtype=float)
            pred = clf.predict(feat)[0]
            label = classes[pred]
            print("Detected sign:", label)

            # 4) Drive
            d = duty_tuple(str(label), reverse=True)
            motor.setMotorModel(*d)

            # Small dwell so we don't hammer motors
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        motor.setMotorModel(0, 0, 0, 0)

if __name__ == "__main__":
    import numpy as np
    main()