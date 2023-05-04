import cv2
from keras.models import load_model  # TensorFlow is required for Keras to work
import pyrealsense2 as rs
import numpy as np
import tensorflow
import odrive
import time

################ Pre-made code from Training #####################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("/home/capstone/IEEE-Region-5-Contest/RealSenseDetection/keras_model.h5", compile=False)
# Load the labels
class_names = open("/home/capstone/IEEE-Region-5-Contest/RealSenseDetection/labels.txt", "r").readlines()

#################################################################

#ODRIVE DECLARATION
odrv0 = odrive.find_any()

def driveForward(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveForwardInches(inches):
    timeVal = (0.5)*inches/9.46
    driveForward(20, timeVal)

def rotateRight(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

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
        rotateRight(20, timeVal)

class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()


    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
            pass
        if not self.endStates:
            raise InitializationError("at least one state must be an end_state")

        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]


def start_transitions(count):
    count = 0
    print("5 seconds until launch")
    time.sleep(5)
    newState = "Drive_state"
    return (newState, count)

def drive_state_1(count):
    if count < 1:
        with open("jetson_drive_to_qr.py") as f:
            exec(f.read())
        newState = "Find_box_state"
    else:
        newState = "Exit_state"
    return (newState, count)

def find_box(count):
    with open("jetson_drive_to_box.py") as f:
        exec(f.read())
    newState = "Launch_drone_state"
    return (newState, count)

def launch_drone(count):
    #launch drone and try to read a qr then land
    with open("top_level_drone.py") as f:
        exec(f.read())
    if count == 7:
        newState = "Drive_state1"
    #else rotate 60 degs and search for box again
    else:
        newState = "Rotate_state"
    return (newState, count)

def rotate_jetson(count):
    #Rotate left until a box is found
    #if not, Rotate right until a box is found
    #lol this sends the bot forward again
    with open("jetson_rotate_left.py") as f:
        exec(f.read())
    newState = "Find_box_state"
    return (newState, count)

#def drive_state_3(count):
 #   newState = "Center_state"
  #  return (newState, count)

#def center_box(count):
 #   print("Looped")
  #  print(count)
   # count = count + 1
    #newState = "Drive_state"
    #return (newState, count)

def exit_state(count):
    print("Exiting")
    return ("Exit_state", "")


m = StateMachine()
m.add_state("Start", start_transitions)
m.add_state("Drive_state", drive_state_1)
m.add_state("Find_box_state", find_box)
m.add_state("Launch_drone_state", launch_drone)
m.add_state("Rotate_state", rotate_jetson)
#m.add_state("Drive_state3", drive_state_3)
#m.add_state("Center_state", center_box)
m.add_state("Exit_state", None, end_state=1)
m.set_start("Start")
m.run("")
