"""
Capture a still image with Picamera2 to a file (blocking).
"""
from picamera2 import Picamera2
import time

def capture_to(path: str, warmup_s: float = 1.5):
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration()
    picam2.start(show_preview=False)
    time.sleep(warmup_s)
    picam2.switch_mode_and_capture_file(capture_config, path)
    time.sleep(0.5)
    picam2.stop()
    return path