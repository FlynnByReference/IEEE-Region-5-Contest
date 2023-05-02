# from main import
import pygame
import sys
from djitellopy import tello
import cv2

# Set display
display = pygame.display.set_mode((10, 10))

# Connect to drone and print battery
maverick = tello.Tello()
maverick.connect()
print(maverick.get_battery())

# Turn drone camera on
maverick.streamon()

# Video define and capture
vid = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()



# Loop for drone to run
while True:

    # try/except block for debugging
    try:
        # Get current frame by frame from drone
        img = maverick.get_frame_read().frame

        # Read qr code, get data and print
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if len(data) > 0:
            print(data)
    except:
        pass

    # # Display camera from drone
    # img = cv2.resize(img, (360, 240))
    # cv2.imshow("results", img)
    # cv2.waitKey(1)
    #
    # # Might not need this
    # ret, frame = vid.read()


    # Loop to check events
    for event in pygame.event.get():
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # For each key that has an event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                maverick.move("back", 70)
                print("s")
            if event.key == pygame.K_a:
                maverick.move("left", 50)
                print("a")
            if event.key == pygame.K_w:
                maverick.move("forward", 50)
                print("w")
            if event.key == pygame.K_d:
                maverick.move("right", 50)
                print("a")
            if event.key == pygame.K_UP:
                maverick.takeoff()
                print("up")
            if event.key == pygame.K_DOWN:
                maverick.land()
                print("down")
            if event.key == pygame.K_RIGHT:
                maverick.rotate_clockwise(30)
                print("right")
            if event.key == pygame.K_LEFT:
                maverick.rotate_counter_clockwise(30)
                print("left")
            if event.key == pygame.K_f:
                maverick.flip_forward()
                print("flip")
            if event.key == pygame.K_UP:
                maverick.move_up(20)
            if event.key == pygame.K_DOWN:
                maverick.move_down(20)


# Close video recording after done
vid.release()
cv2.destroyAllWindows()
