# For object detection
from keras.models import load_model

# For accessing camera's
import cv2

# Will probably be removed eventually
import numpy as np

# Access to the drone SDK
from djitellopy import tello

# For Realsense need to uncomment when running
import pyrealsense2 as rs

# Handles time
import time

# Used for threading functions
from threading import Thread

# GPIO library
import Jetson.GPIO as GPIO

################ Pre-made code from Training #####################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("keras_Model.h5", compile=False)
# Load the labels
class_names = open("labels.txt", "r").readlines()
# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture(0)
#################################################################

# Variable when QR code is found
foundQR = True

# Connect to drone start stream and print battery
# Video define and captrue
detector = cv2.QRCodeDetector()

# Create drone object
drone = tello.Tello()

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


# Function for reading QR codes
def flyQRRead():
    while foundQR:
        # Get frame by frame from drone
        img = drone.get_frame_read().frame

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # Break out of loop when esc is hit
        if keyboard_input == 27:
            break

        # Get QR code data
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if len(data) > 0:
            print(data)
            foundQR = False


# For the drone to find the box and rotate to it
def rotateToBox():

    # Connect to drone, get battery, turn camera on, and takeoff
    drone.connect()
    print(drone.get_battery())
    drone.streamon()
    drone.takeoff()

    # Loop until box is found
    while True:

        ################ Pre-made code from Training #####################
        # Grab the webcamera's image.
        image = drone.get_frame_read().frame
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        #################################################################

        # If looking at not box rotate 10 degrees
        if str(class_name[2:]) == "Neutral\n":
            if np.round(confidence_score * 100) >= 50:
                # Print what drone is doing
                print("Rotate 20 degree")

                # Rotate drone 10 degrees
                # drone.rotate_counter_clockwise(20)
                drone.rotate_clockwise(20)
                pass

        # Stop rotating when box is found
        elif str(class_name[2:]) == "Box\n":
            if np.round(confidence_score * 100) >= 50:
                drone.move_forward(100)
                stopRotating = True
                print("At box")

        # Break when looking at box
        if stopRotating:
            drone.land()
            drone.streamoff()
            cv2.destroyAllWindows()
            break

def scanBoxSide():
    try:
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = rs.pipeline()

        # Configure streams
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        # Start streaming
        pipeline.start(config)

        while True:
            # This call waits until a new coherent set of frames is available on a device
            # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
            time.sleep(7)
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            if not depth: continue

            # Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
            coverage = [0] * 64
            for y in range(480):
                for x in range(640):
                    dist = depth.get_distance(x, y)
                    if 0 < dist and dist < 1:
                        coverage[x // 10] += 1
                if y % 20 == 19:
                    line = ""
                    for c in coverage:
                        line += " .:nhBXWW"[c // 25]
                    coverage = [0] * 64
                    print(line)
            print(depth.get_distance(240, 320))
            exit(0)
    except Exception as e:
        print(e)
        pass

# Loop to run code
while True:
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # Break out of loop when esc is hit
    if keyboard_input == 27:
        break

    # Key 'A' is hit check for QR code
    if keyboard_input == 65:
        flyQRRead()

    # Key 'B' is hit rotate to box
    if keyboard_input == 66:
        rotateToBox()

    # Key 'C' is hit to scan box
    if keyboard_input == 67:
        scanBoxSide()
    