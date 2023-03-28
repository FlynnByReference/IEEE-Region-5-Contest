from camera_ground_top_level import Ground_Camera
from gpio_groundbot import GPIOClass

groundCamera = Ground_Camera()
groundPins = GPIOClass()

groundPins.controlMotors()
