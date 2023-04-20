import cv2
import time
import nanocamera as nano
import sys
import odrive

def driveForward(val, duration):
    odrv0.axis0.controller.input_vel = val
    odrv0.axis1.controller.input_vel = -val
    time.sleep(duration)
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def driveForwardInches(inches):
    timeVal = (0.5)*inches/9.46
    driveForward(20, timeVal)

# Variable when QR code is found
foundQR = False
#odrv0 = odrive.find_any()
# Video define and captrue
detector = cv2.QRCodeDetector()
camera = nano.Camera(flip=0, width=480, height=360, fps=5)


odrv0.axis0.controller.input_vel = 20
odrv0.axis1.controller.input_vel = -20
while foundQR == False:
    # Get frame by frame from drone
    img = camera.read()

    # Get QR code data
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if len(data) > 0:
        foundQR = True
        print(data)
        break

    # Display in video feed
    #img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    cv2.waitKey(1)

    # Quit the program using 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close video recording after done
# close the camera instance
camera.release()

odrv0.axis0.controller.input_vel = 0
odrv0.axis1.controller.input_vel = 0
time.sleep(5)
driveForwardInches(50)

    # remove camera object
del camera
cv2.destroyAllWindows()
