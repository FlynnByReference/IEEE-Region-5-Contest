import cv2  # Install opencv-python
from keras.models import load_model  # TensorFlow is required for Keras to work
import numpy as np
import nanocamera as nano


class Ground_Camera:
    def __init__(self):
        pass

    def qrReading(self):
        detector = cv2.QRCodeDetector()
        # Create the Camera instance
        camera = nano.Camera(camera_type=1, device_id=0, width=640, height=480, fps=30)
        print('CSI Camera ready? - ', camera.isReady())
        while camera.isReady():
            try:
                # read the camera image
                frame = camera.read()

                # get QR code data
                data, bbox, straight_qrcode = detector.detectAndDecode(frame)
                if len(data) > 0:
                    print(data)

                # display the frame
                cv2.imshow("Results", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            except KeyboardInterrupt:
                break

        # close the camera instance
        camera.release()

        # remove camera object
        del camera

    def objectDetection(self):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model("/home/capstone/PycharmProjects/IEEE-Region-5-Contest/Groundbot/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("/home/capstone/PycharmProjects/IEEE-Region-5-Contest/Groundbot/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        camera = cv2.VideoCapture(0)

        while True:
            # Grab the webcamera's image.
            ret, image = camera.read()

            (h, w) = image.shape[:2]

            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Show the image in a window
            cv2.imshow("Webcam Image", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # (startX, startY) = temp
            # startX = int(startX * w)
            # startY = int(startY * h)
            # endX = int(endX * w)
            # endY = int(endY * h)

            # image = cv2.rectangle(image, (startX, startY), (startX+100, startY+100), (255, 0, 0), 2)

            # Predicts the model
            prediction = model.predict(image)
            print(prediction)
            index = np.argmax(prediction)
            print(index)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

            # Listen to the keyboard for presses.
            keyboard_input = cv2.waitKey(1)

            # 27 is the ASCII for the esc key on your keyboard.
            if keyboard_input == 27:
                break

        camera.release()
        cv2.destroyAllWindows()
