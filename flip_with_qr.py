from djitellopy import tello
import cv2
from threading import Thread
from image_transformer import ImageTransformer
from util import save_image
import os

# Connect to drone st
# art stream and print battery
# Video define and captrue
detector = cv2.QRCodeDetector()

# Variable when QR code is found
foundQR = True

# Connect to drone and turn on camera
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

# Make output dir
if not os.path.isdir('output'):
    os.mkdir('output')

def flyQRRead():
    global rotated_img
    while foundQR:
        # Get frame by frame from drone
        img = drone.get_frame_read().frame

        # Instantiate the image transformer class
        it = ImageTransformer(img)
        rotated_img = it.rotate_along_axis(theta=45)

        # Get QR code data
        data, bbox, straight_qrcode = detector.detectAndDecode(rotated_img)
        if len(data) > 0:
            print(data)

    save_image('output/{}.jpg'.format(str(45).zfill(3)), rotated_img)

# Start thread of
record = Thread(target=flyQRRead)
record.start()

# Take off
drone.takeoff()

# Move and flip for QR
# drone.move_right(50)
drone.flip_forward()
drone.move_forward(50)

# Land drone
drone.land()

# Close video recording after done
foundQR = False
cv2.destroyAllWindows()
drone.streamoff()
record.join()
