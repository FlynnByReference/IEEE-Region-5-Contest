import cap as cap
from djitellopy import tello
import cv2

# Connect to drone start stream and print battery
maverick = tello.Tello()
maverick.connect()
print(maverick.get_battery())

# Make sure camera is off
maverick.streamoff()

# Turn camera on
maverick.streamon()

# Create a Cascade for faces
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:

    # Get fram by fram and set size of video
    img = maverick.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    # cv2.imshow("results", img)
    cv2.waitKey(1)

    # Convert image to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Getting corners around the face, 1.3 = scale factor, 5 = minimum neighbor can be detected
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)

    # For box around face
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255,   0), 3)

    # Show video stream from drone with face detection
    cv2.imshow('Testing', img)

    # Use 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Close video recording after done
maverick.streamoff()
cv2.destroyAllWindows()
cap.release()
cv2.destroyWindow('Testing')
