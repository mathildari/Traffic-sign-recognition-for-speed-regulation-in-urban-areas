"""Real-time circular sign detection + classification using pretrained kNN.

- Detect circles with HoughCircles
- Crop + resize to 100x100
- Flatten RGB to features and classify with models/knn.joblib
Keys:
    q : quit
    s : save crops to ./captures
"""
import os, time
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
import joblib

from tsr.features import image_array_to_rgb_list

CAPTURES = Path("captures"); CAPTURES.mkdir(exist_ok=True, parents=True)

def detect_circles(frame: np.ndarray):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 1.5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=25,
                               param1=80, param2=35, minRadius=12, maxRadius=120)
    return None if circles is None else np.around(circles).astype(np.int32)

def crop_circle(frame, x, y, r, pad=6):
    h, w = frame.shape[:2]
    x0, y0 = max(0, x - r - pad), max(0, y - r - pad)
    x1, y1 = min(w, x + r + pad), min(h, y + r + pad)
    crop = frame[y0:y1, x0:x1].copy()
    return None if crop.size == 0 else cv2.resize(crop, (100, 100), interpolation=cv2.INTER_AREA)

def save_crops(crops):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    paths = []
    for i, c in enumerate(crops):
        p = CAPTURES / f"sign_{ts}_{i}.png"
        cv2.imwrite(str(p), c)
        paths.append(str(p))
    return paths

def main():
    # Load model
    bundle = joblib.load("models/knn.joblib")
    clf = bundle["model"]; classes = bundle["classes"]

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open camera 0")

    last_crops = []
    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.02); continue

        circles = detect_circles(frame)
        last_crops = []

        if circles is not None:
            for (x,y,r) in circles[0, :]:
                if r <= 0: continue
                cv2.circle(frame, (x, y), r, (0,255,0), 2)
                cv2.circle(frame, (x, y), 2, (0,0,255), -1)
                crop = crop_circle(frame, x, y, r)
                if crop is None: continue
                last_crops.append(crop)
                # classify
                feat = np.array([image_array_to_rgb_list(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))], dtype=float)
                pred = clf.predict(feat)[0]
                label = classes[pred]
                cv2.putText(frame, f"{label}", (x - r, max(0, y - r - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        info = f"Circles: {0 if circles is None else circles.shape[1]}  [s] save  [q] quit"
        cv2.putText(frame, info, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        cv2.imshow("Real-time TSR", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            paths = save_crops(last_crops)
            print("Saved:", *paths, sep="\n - ") if paths else print("No crops to save.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()