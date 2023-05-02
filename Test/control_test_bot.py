# GPIO library
import Jetson.GPIO as GPIO

# Handles time
import time

# Pin Definition
PWM_R = 7
PWM_L = 11
Control_R = 13
Control_L = 15

# Set up the GPIO channel
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PWM_L, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Control_L, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Control_R, GPIO.OUT, initial=GPIO.LOW)


print("Press CTRL+C when you want the LED to stop blinking")

# Blink the LED
while True:
    # Turn right
    time.sleep(2)
    GPIO.output(PWM_R, GPIO.HIGH)
    GPIO.output(PWM_L, GPIO.HIGH)
    GPIO.output(Control_R, GPIO.LOW)
    GPIO.output(Control_L, GPIO.HIGH)
    print("Turning right")

    # Turn left
    time.sleep(2)
    GPIO.output(PWM_R, GPIO.HIGH)
    GPIO.output(PWM_L, GPIO.HIGH)
    GPIO.output(Control_R, GPIO.LOW)
    GPIO.output(Control_L, GPIO.HIGH)
    print("turning left")

    # Drive forward
    time.sleep(2)
    GPIO.output(PWM_R, GPIO.HIGH)
    GPIO.output(PWM_L, GPIO.HIGH)
    GPIO.output(Control_R, GPIO.HIGH)
    GPIO.output(Control_L, GPIO.HIGH)
    print("Driving Forward")

    # Drive backward
    time.sleep(2)
    GPIO.output(PWM_R, GPIO.HIGH)
    GPIO.output(PWM_L, GPIO.HIGH)
    GPIO.output(Control_R, GPIO.LOW)
    GPIO.output(Control_L, GPIO.LOW)
    print("Driving Back")

    break
