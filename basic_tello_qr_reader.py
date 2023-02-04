from djitellopy import tello
import cv2


# Connect to drone start stream and print battery
maverick = tello.Tello()
maverick.connect()
print(maverick.get_battery())
maverick.streamon()

# Video define and captrue
detector = cv2.QRCodeDetector()


while True:
    # Get frame by frame from drone
    img = maverick.get_frame_read().frame

    # Get QR code data
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if len(data) > 0:
        print(data)

    # Display in video feed
    img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    cv2.waitKey(1)

    # Quit the program using 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close video recording after done
cv2.destroyAllWindows()