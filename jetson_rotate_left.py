import time
import sys
import odrive

def driveForward(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveForwardInches(inches):
    timeVal = (0.5)*inches/9.46
    driveForward(20, timeVal)

def rotateLeft(val, duration):
    odrv0.axis0.controller.input_vel = -val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def rotateDegrees(degrees, direction):
    timeVal = (0.5)*degrees/104.2
    if direction == "L":
        rotateLeft(20, timeVal)
    else:
        rotateRight1(20, timeVal)

# Variable when QR code is found
rotateDegrees(90, "L")
