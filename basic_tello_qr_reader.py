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

frame_width = int(vid.get(3))
frame_height = int(vid.get(4))

size = (frame_width, frame_height)

result = cv2.VideoWriter('droneVid.mp4',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

maverick.takeoff()

while True:
    # Get frame by frame from drone
    img = maverick.get_frame_read().frame

    ret, frame = vid.read()

    if ret == True:
        result.write(img)
        cv2.imshow('Frame', img)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    else:
        break

    # Get QR code data
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if len(data) > 0:
        print(data)

    # Display in video feed
    img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    cv2.waitKey(1)

    # Capture the video frame by frame
    ret, frame = vid.read()

    maverick.move_forward(40)

    # Quit the program using 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close video recording after done
vid.release()
result.release()
cv2.destroyAllWindows()