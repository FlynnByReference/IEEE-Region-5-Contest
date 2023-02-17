import time
import cv2
from threading import Thread
from djitellopy import tello

# Connect to drone
drone = tello.Tello()
drone.connect()

drone.streamon()
frameDrone = drone.get_frame_read()

recordVal = True


def recordVid():
    height, width, _ = frameDrone.frame.shape
    vid = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while recordVal:
        vid.write(frameDrone.frame)
        time.sleep(1 / 30)

    vid.release()


record = Thread(target=recordVid)
record.start()

drone.takeoff()
drone.move_right(50)
drone.rotate_counter_clockwise(90)
drone.move_right(200)
drone.rotate_counter_clockwise(90)
drone.move_right(100)
drone.rotate_counter_clockwise(90)
drone.move_right(200)
drone.rotate_counter_clockwise(90)
drone.move_right(50)

drone.land()
drone.streamoff()
recordVal = False
record.join()
