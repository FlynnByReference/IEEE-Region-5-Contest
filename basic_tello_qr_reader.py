from djitellopy import tello
import cv2


# Connect to drone start stream and print battery
maverick = tello.Tello()
maverick.connect()
print(maverick.get_battery())
maverick.streamon()

# Video define and captrue
vid = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()


while True:
    # Get frame by frame from drone
    img = maverick.get_frame_read().frame

    #
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if len(data) > 0:
        print(data)
    img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    cv2.waitKey(1)

    # Capture the video frame by frame
    ret, frame = vid.read()

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close video recording after done
vid.release()
cv2.destroyAllWindows()