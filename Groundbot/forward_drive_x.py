# from main import
import pygame
import sys
import odrive
import time
from pygame.locals import *

#pygame.init()
display = pygame.display.set_mode((10,10))
odrv0 = odrive.find_any()

def driveForward(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    #time.sleep(duration)
    #odrv0.axis0.controller.input_vel = 0
    #odrv0.axis1.controller.input_vel = 0

def driveForward1(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveBackward(val, duration):
    odrv0.axis0.controller.input_vel = -val
    odrv0.axis1.controller.input_vel = val
    #time.sleep(duration)
    #odrv0.axis0.controller.input_vel = 0
   # odrv0.axis1.controller.input_vel = 0

def rotateLeft(val, duration):
    odrv0.axis0.controller.input_vel = -val
    odrv0.axis1.controller.input_vel = -val
    #time.sleep(duration)
   # odrv0.axis0.controller.input_vel = 0
   # odrv0.axis1.controller.input_vel = 0

def rotateLeft1(val, duration):
    odrv0.axis0.controller.input_vel = -val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def rotateRight(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = val
    #time.sleep(duration)
  #  odrv0.axis0.controller.input_vel = 0
   # odrv0.axis1.controller.input_vel = 0

def rotateRight1(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

#front left wheel is point of rotation
def bankLeft(val, duration):
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = -val
    #time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

#back right wheel is point of rotation
def bankRight(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = 0
    #time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveForwardInches(inches):
    timeVal = (0.5)*inches/9.46
    driveForward1(20, timeVal)

def rotateDegrees(degrees, direction):
    timeVal = (0.5)*degrees/104.2
    if direction == "L":
        rotateLeft1(20, timeVal)
    else:
        rotateRight1(20, timeVal)
    #driveForward1(20, timeVal)

# creating a running loop
while True:

    # creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # checking if keydown event happened or not
        keys = pygame.key.get_pressed()
        #if event.type == pygame.KEYPRESSED:
        if keys[K_s]:
            driveBackward(20, 0.1)
            print("s")
        elif keys[K_a]:
            rotateLeft(20, 0.1)
            print("a")
        elif keys[K_w]:
            driveForward(20, 0.1)
            print("w")
        elif keys[K_d]:
            rotateRight(20, 0.1)
            print("d")
        elif keys[K_q]:
            rotateDegrees(90, "L")
        elif keys[K_e]:
            rotateDegrees(90, "R")
        elif keys[K_r]:
            driveForwardInches(72)
        elif keys[K_f]:
            driveForwardInches(20)
        else:
            odrv0.axis0.controller.input_vel = 0
            odrv0.axis1.controller.input_vel = 0

      
