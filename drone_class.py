from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from djitellopy import tello
from image_transformer import ImageTransformer

class DroneClass:
    def __init__(self):
        pass

    def scanQRCode(self):
        # Connect to drone start stream and print battery
        maverick = tello.Tello()
        maverick.connect()
        print(maverick.get_battery())
        maverick.streamon()
        maverick.takeoff()
        maverick.move_down(30)

        # Video define and captrue
        detector = cv2.QRCodeDetector()

        QRdata = "A"

        count = 1

        while True:
            # Get frame by frame from drone
            img = maverick.get_frame_read().frame

            # Instantiate the image transformer class
            it = ImageTransformer(img)
            rotated_img = it.rotate_along_axis(theta=60)
            rotated_img = cv2.resize(rotated_img, (360, 1000))

            # Get QR code data
            data, bbox, straight_qrcode = detector.detectAndDecode(rotated_img)
            if len(data) > 0:
                print(data)
                QRdata = data
                # maverick.move_forward(80)

            # Display in video feed
            cv2.imshow("results", rotated_img)
            cv2.waitKey(1)

            # Quit the program using 'q'
            if cv2.waitKey(1) & 0xFF == ord('q') or count == 100:
                break

            count = count + 1

        maverick.land()

        # Close video recording after done
        cv2.destroyAllWindows()

        return QRdata

    def flyToBox(self):
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

        # Variable to stop rotating when looking at box
        stopRotating = False

        # Connect to drone, get battery
        drone = tello.Tello()
        drone.connect()
        print(drone.get_battery())

        # Turn on camera, takeoff, move to level of box
        drone.streamon()
        drone.takeoff()
        # drone.move_down(20)

        # Loop to turn till facing box
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
                break

        # Disconnect everything
        drone.land()
        drone.streamoff()
        cv2.destroyAllWindows()