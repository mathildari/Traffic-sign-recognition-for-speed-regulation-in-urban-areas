"""
Simple motor test sequence based on your original Motor.py.
"""
import time
from raspberry.motor import Motor

def loop():
    m = Motor()
    m.setMotorModel(2000,2000,2000,2000); time.sleep(3)  # Forward
    m.setMotorModel(-2000,-2000,-2000,-2000); time.sleep(3)  # Back
    m.setMotorModel(-500,-500,2000,2000); time.sleep(3)  # Left
    m.setMotorModel(2000,2000,-500,-500); time.sleep(3)  # Right
    m.setMotorModel(0,0,0,0)

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        Motor().setMotorModel(0,0,0,0)