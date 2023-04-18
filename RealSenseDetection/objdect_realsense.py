import cv2
from keras.models import load_model  # TensorFlow is required for Keras to work
import pyrealsense2 as rs
import numpy as np
import tensorflow
import odrive
import time


def driveForward(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveBackward(val, duration):
    odrv0.axis0.controller.input_vel = -val
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

def rotateRight(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

################ Pre-made code from Training #####################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("/home/capstone/IEEE-Region-5-Contest/RealSenseDetection/keras_model.h5", compile=False)
# Load the labels
class_names = open("/home/capstone/IEEE-Region-5-Contest/RealSenseDetection/labels.txt", "r").readlines()

#################################################################

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Connect to odrive
odrv0 = odrive.find_any()

stopRotating = False

print("[INFO] Starting streaming...")
pipeline.start()
print("[INFO] Camera ready.")

while True:

    ################ Pre-made code from Training #####################
    # Grab the RealSense image.
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    scaled_size = (color_frame.width, color_frame.height)

    # Resize the raw image into (224-height,224-width) pixels
    color_image = cv2.resize(color_image, (224, 224), interpolation=cv2.INTER_AREA)
    # Make the image a numpy array and reshape it to the models input shape.
    color_image = np.asarray(color_image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    color_image = (color_image / 127.5) - 1
    # Predicts the model
    prediction = model.predict(color_image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()

    width = depth.get_width()
    height = depth.get_height()

    dist = depth.get_distance(int(width / 2), int(height / 2))


    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    print("Distance: ", dist)
    #################################################################

    # Break when looking at box
    if stopRotating:

        while dist > 1.0:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            scaled_size = (color_frame.width, color_frame.height)

            # Resize the raw image into (224-height,224-width) pixels
            color_image = cv2.resize(color_image, (224, 224), interpolation=cv2.INTER_AREA)
            # Make the image a numpy array and reshape it to the models input shape.
            color_image = np.asarray(color_image, dtype=np.float32).reshape(1, 224, 224, 3)
            # Normalize the image array
            color_image = (color_image / 127.5) - 1
            # Predicts the model
            prediction = model.predict(color_image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()

            width = depth.get_width()
            height = depth.get_height()

            dist = depth.get_distance(int(width / 2), int(height / 2))

            print("Distance: ", dist)

        odrv0.axis0.controller.input_vel = 0
        odrv0.axis1.controller.input_vel = 0
        break
        
    # If looking at not box rotate 10 degrees
    if str(class_name[2:]) != "Box\n":
        if np.round(confidence_score * 100) >= 50:
            # Print what drone is doing
            #odrv0.axis0.controller.input_vel = -20
            #odrv0.axis1.controller.input_vel = -20
            #time.sleep(0.5)
            #odrv0.axis0.controller.input_vel = 0
            #drv0.axis1.controller.input_vel = 0
            rotateLeft(20, 0.5)
            time.sleep(0.5)
            
            pass

    # Stop rotating when box is found
    elif str(class_name[2:]) == "Box\n":
        if np.round(confidence_score * 100) >= 50:
            #odrv0.axis0.controller.input_vel = 20
            #odrv0.axis1.controller.input_vel = -20
            #time.sleep(5)
            driveForward(20, 5)
            stopRotating = True
            print("At box")

    


# Disconnect everything
pipeline.stop()
cv2.destroyAllWindows()
