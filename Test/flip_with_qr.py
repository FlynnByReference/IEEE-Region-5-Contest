from djitellopy import tello
import cv2
from threading import Thread
import time

# Connect to drone start stream and print battery
# Video define and captrue
detector = cv2.QRCodeDetector()

# Variable when QR code is found
foundQR = True

# Connect to drone and turn on camera
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

def flyQRRead():
    while foundQR:
        # Get frame by frame from drone
        img = drone.get_frame_read().frame

        # Get QR code data
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if len(data) > 0:
            print(data)


# Start thread of
record = Thread(target=flyQRRead)
record.start()

# Take off
drone.takeoff()

# Move and flip for QR
drone.move_right(50)
drone.flip_forward()
drone.move_forward(40)

# Land drone
drone.land()

# Close video recording after done
foundQR = False
cv2.destroyAllWindows()
drone.streamoff()
record.join()
