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

def rotateRight(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = val
    #time.sleep(duration)
  #  odrv0.axis0.controller.input_vel = 0
   # odrv0.axis1.controller.input_vel = 0

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
    timeVal = inches/9.77
    driveForward1(20, timeVal)

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
            bankLeft(20, 0.1)
        elif keys[K_e]:
            bankRight(20, 0.1)
        elif keys[K_r]:
            driveForwardInches(12)
        elif keys[K_f]:
            driveForwardInches(20)
        else:
            odrv0.axis0.controller.input_vel = 0
            odrv0.axis1.controller.input_vel = 0

      
