"""
Map speed-limit class labels to motor PWM duties.
Values taken directly from your original scripts.
"""
# Your comments indicated:
# 1300 ~ 50 km/h, 1900/1950 ~ 70 km/h, 2250/2500 ~ 90 km/h
# We'll expose both forward (+) and reverse (-) convenience tuples.
SPEED_TO_DUTY = {
    "50":  1300,
    "70":  1900,   # or 1950 in another file
    "90":  2250,   # or 2500 in another file
}

def duty_tuple(speed_label: str, reverse: bool = True):
    duty = SPEED_TO_DUTY.get(speed_label, 1300)
    duty = -duty if reverse else duty
    return (duty, duty, duty, duty)