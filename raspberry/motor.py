"""
Raspberry Pi motor control using PCA9685 (keeps original logic).
Relies on a module `PCA9685` providing `PCA9685.setPWMFreq` and `setMotorPwm(chan, duty)`.
"""
import time

try:
    from PCA9685 import PCA9685  # Provided by your board/vendor library
except Exception as e:
    raise SystemExit("Missing PCA9685 module. Install your vendor's `PCA9685` Python lib.\n"
                     f"Import error: {e}")

class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)

    def duty_range(self, d1, d2, d3, d4):
        def clamp(v):
            return 4095 if v > 4095 else (-4095 if v < -4095 else v)
        return clamp(d1), clamp(d2), clamp(d3), clamp(d4)

    def left_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(0, 0); self.pwm.setMotorPwm(1, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(1, 0); self.pwm.setMotorPwm(0, abs(duty))
        else:
            self.pwm.setMotorPwm(0, 4095); self.pwm.setMotorPwm(1, 4095)

    def left_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(3, 0); self.pwm.setMotorPwm(2, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(2, 0); self.pwm.setMotorPwm(3, abs(duty))
        else:
            self.pwm.setMotorPwm(2, 4095); self.pwm.setMotorPwm(3, 4095)

    def right_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(6, 0); self.pwm.setMotorPwm(7, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(7, 0); self.pwm.setMotorPwm(6, abs(duty))
        else:
            self.pwm.setMotorPwm(6, 4095); self.pwm.setMotorPwm(7, 4095)

    def right_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(4, 0); self.pwm.setMotorPwm(5, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(5, 0); self.pwm.setMotorPwm(4, abs(duty))
        else:
            self.pwm.setMotorPwm(4, 4095); self.pwm.setMotorPwm(5, 4095)

    def setMotorModel(self, d1, d2, d3, d4):
        d1, d2, d3, d4 = self.duty_range(d1, d2, d3, d4)
        self.left_Upper_Wheel(d1)
        self.left_Lower_Wheel(d2)
        self.right_Upper_Wheel(d3)
        self.right_Lower_Wheel(d4)