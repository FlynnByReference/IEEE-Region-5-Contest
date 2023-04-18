import cv2  # Install opencv-python
from keras.models import load_model  # TensorFlow is required for Keras to work
import numpy as np
import odrive
import nanocamera as nano

################ Pre-made code from Training #####################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("/home/capstone/IEEE-Region-5-Contest/BoxDetectionModel/keras_model.h5", compile=False)
# Load the labels
class_names = open("/home/capstone/IEEE-Region-5-Contest/BoxDetectionModel/labels.txt", "r").readlines()
# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture(0)
#################################################################


# Variable to stop rotating when looking at box
stopRotating = False


odrv0 = odrive.find_any()

# CAMERA can be 0 or 1 based on default camera of your computer
#camera = cv2.VideoCapture(0)
camera = nano.Camera(camera_type=1, device_id=0, width=640, height=480, fps=30)

# Loop to turn till facing box
while True:

    ################ Pre-made code from Training #####################
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

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
    if str(class_name[2:]) != "Box\n":
        if np.round(confidence_score * 100) >= 50:
            # Print what drone is doing
            print("Rotate 20 degree")
            odrv0.axis0.controller.input_vel = 20
            odrv0.axis1.controller.input_vel = 20
            # Rotate drone 10 degrees
            # drone.rotate_counter_clockwise(20)
            
            pass

    # Stop rotating when box is found
    elif str(class_name[2:]) == "Box\n":
        if np.round(confidence_score * 100) >= 50:
            odrv0.axis0.controller.input_vel = 0
            odrv0.axis1.controller.input_vel = 0
            stopRotating = True
            print("At box")

    # Break when looking at box
    if stopRotating:
        break

# Disconnect everything
cv2.destroyAllWindows()
