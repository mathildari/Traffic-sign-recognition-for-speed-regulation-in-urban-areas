"""
Ultrasonic distance measurement with HC-SR04 on Raspberry Pi.

Usage:
    python ultrasonic_sensor.py --trigger 23 --echo 24 --interval 0.5 --timeout 0.03

Notes:
    - Requires running on a Raspberry Pi with RPi.GPIO installed.
    - Press Ctrl+C to exit cleanly.
"""
import argparse
import time

try:
    import RPi.GPIO as GPIO  # type: ignore
except Exception as e:
    raise SystemExit("This script must run on a Raspberry Pi with RPi.GPIO installed.\n"
                     f"Import error: {e}")

SPEED_OF_SOUND_CM_S = 34300.0  # ~343 m/s

def setup(trigger_pin: int, echo_pin: int) -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigger_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(echo_pin, GPIO.IN)

def measure_distance(trigger_pin: int, echo_pin: int, timeout_s: float = 0.03) -> float:
    """Return the measured distance in centimeters.
    timeout_s prevents blocking when no echo is received (e.g., out of range).
    """
    # 10µs trigger pulse
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(1e-5)
    GPIO.output(trigger_pin, GPIO.LOW)

    start = time.time()
    # Wait for echo to go high
    while GPIO.input(echo_pin) == 0:
        if time.time() - start > timeout_s:
            return float('inf')  # no echo (timeout)
    pulse_start = time.time()

    # Wait for echo to go low
    while GPIO.input(echo_pin) == 1:
        if time.time() - pulse_start > timeout_s:
            return float('inf')  # echo held too long (timeout)
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start  # round trip
    distance_cm = (pulse_duration * SPEED_OF_SOUND_CM_S) / 2.0
    return distance_cm

def main() -> None:
    parser = argparse.ArgumentParser(description="Ultrasonic distance measurement (HC-SR04)")
    parser.add_argument("--trigger", type=int, default=23, help="BCM pin for TRIGGER (default: 23)")
    parser.add_argument("--echo", type=int, default=24, help="BCM pin for ECHO (default: 24)")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between reads (default: 1.0)")
    parser.add_argument("--timeout", type=float, default=0.03, help="Echo timeout in seconds (default: 0.03)")
    args = parser.parse_args()

    setup(args.trigger, args.echo)
    print("Starting distance measurements. Press Ctrl+C to stop.")
    try:
        while True:
            dist = measure_distance(args.trigger, args.echo, args.timeout)
            if dist == float('inf'):
                print("Distance: -- (timeout)")
            else:
                print(f"Distance: {dist:.2f} cm")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()