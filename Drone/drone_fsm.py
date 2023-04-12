from drone_class import DroneClass
from djitellopy import tello
import cv2  # Install opencv-python


class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise InitializationError("at least one state must be an end_state")

        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]

def idle_transitions():
    # if good to start
    #   new_state = "takeoff_state"
    # else
    #   new_state = "error_state"

    # this will keep drone off to not waste resources
    drone.turn_motor_off()
    drone.streamoff()

    return (new_state)

def takeoff_transitions():
    # if looking for box
    #   new_state = "rotate_to_box_state"
    # elif looking for bot
    #   new_state = "rotate_to_bot_state"
    # elif landing
    #   new_state = "land_state"
    # else
    #   new_state = "error_state"
    return(new_state)

def rotate_to_box_transitions():
    # if flying to the box
    #   new_state = "fly_to_box"
    # else
    #   new_state = "error_state"
    return(new_state)

def fly_to_box_transitions():
    # if QR Code
    #   new_state = "scan_qr_code"
    # else
    #   new_state = "error_state"
    return(new_state)

def scan_qr_code_transitions():
    # if looking for next box
    #   new_state = "rotate_to_box"
    # elif looking for bot
    #   new_state = "rotate_to_bot"
    # else
    #   new_state = "error_state"

    # This code will be added to the correct spot in this function
    # Turn on the drone camera
    drone.streamon()

    # Video define and captrue
    detector = cv2.QRCodeDetector()

    while True:
        # Get frame by frame from drone
        img = drone.get_frame_read().frame

        # Get QR code data
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if len(data) > 0:
            print(data)

            # Turn off the drone camera
            drone.streamoff()
            break

        # probably don't need this
        # Display in video feed
        # img = cv2.resize(img, (360, 240))
        # cv2.imshow("results", img)
        # cv2.waitKey(1)


    # Close video recording after done
    cv2.destroyAllWindows()


    return(new_state)


# Probably change this to fly over box
def rotate_to_bot_transitions():
    # if looking for box
    #   new_state = "rotate_to_box"
    # elif going to bot
    #   new_state = "fly_to_bot"
    # else
    #   new_state = "error_state"
    return(new_state)


# Probably will remove this
def fly_to_bot_transitions():
    # if going to land
    #   new_state = "land"
    # else
    #   new_state = "error_state"
    return(new_state)

def land_transitions():
    # if staying in idle
    # new_state = "idle"
    # else
    #   new_state = "error_state"

    # Really only functionality we need
    drone.land()
    return(new_state)


# Drone initializer
drone = tello.Tello()
drone.connect()


# Code to add states
m = StateMachine()
m.add_state("idle", idle_transitions())
m.add_state("takeoff", takeoff_transitions())
m.add_state("rotate_to_box", rotate_to_box_transitions())
m.add_state("rotate_to_bot", rotate_to_bot_transitions())
m.add_state("fly_to_box", fly_to_box_transitions())
m.add_state("fly_to_bot", fly_to_bot_transitions())
m.add_state("scan_qr_code", scan_qr_code_transitions())
m.add_state("land", land_transitions())
m.set_start("idle")
# m.run(input)