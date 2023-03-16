from keras.models import load_model  # TensorFlow is required for Keras to work
import pyrealsense2 as rs
import numpy as np
import cv2
import tensorflow

################ Pre-made code from Training #####################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("keras_model.h5", compile=False)
# Load the labels
class_names = open("labels.txt", "r").readlines()
# CAMERA can be 0 or 1 based on default camera of your computer
# camera = cv2.VideoCapture(0)
#################################################################

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

print("[INFO] Starting streaming...")
pipeline.start(config)
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

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    #################################################################

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break


# Disconnect everything
pipeline.stop()
cv2.destroyAllWindows()