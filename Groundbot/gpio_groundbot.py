# GPIO library
import Jetson.GPIO as GPIO


class GPIOClass:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

    def controlMotors(self):
        pass

    def ultrasonicSensor(self):
        pass