import time, cv2, numpy as np

param1 = 80
param2 = 40
dp = 1.2
min_dist = 25
min_radius = 10
max_radius = 120

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Could not open camera 0.")

print("Press q to quit. Tunable keys: i/k (dp), o/l (param1), p/m (param2).")

while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(0.02)
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 1.5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, min_dist,
                               param1=param1, param2=param2,
                               minRadius=min_radius, maxRadius=max_radius)

    if circles is not None:
        circles = np.around(circles).astype(np.int32)
        for (x, y, r) in circles[0, :]:
            if r > 0:
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

    overlay = f"[i|k] dp: {dp:0.2f}   [o|l] param1: {param1:d}   [p|m] param2: {param2:d}   circles: {0 if circles is None else circles.shape[1]}"
    cv2.putText(frame, overlay, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.imshow("HoughCircles Tuner", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('i'):
        dp = min(10.0, dp + 0.05)
    elif key == ord('k'):
        dp = max(0.1, dp - 0.05)
    elif key == ord('o'):
        param1 = min(255, param1 + 1)
    elif key == ord('l'):
        param1 = max(1, param1 - 1)
    elif key == ord('p'):
        param2 = min(255, param2 + 1)
    elif key == ord('m'):
        param2 = max(1, param2 - 1)

cap.release()
cv2.destroyAllWindows()