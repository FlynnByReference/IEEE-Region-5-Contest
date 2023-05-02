import cv2
import nanocamera as nano

# Video define and captrue
detector = cv2.QRCodeDetector()
camera = nano.Camera(flip=0, width=480, height=360, fps=5)

while True:
    # Get frame by frame from drone
    img = camera.read()

    # Get QR code data
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if len(data) > 0:
        print(data)

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

    # remove camera object
del camera
cv2.destroyAllWindows()
