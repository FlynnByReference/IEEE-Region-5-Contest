##########################################################################################
#    Title: Finite State Machine in Python
#    Author: Bernd Klein
#    Date: February 1, 2022
#    Availability: https://python-course.eu/applications-python/finite-state-machine.php
##########################################################################################

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
    return(new_state)

def rotate_to_bot_transitions():
    # if looking for box
    #   new_state = "rotate_to_box"
    # elif going to bot
    #   new_state = "fly_to_bot"
    # else
    #   new_state = "error_state"
    return(new_state)

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
    return(new_state)

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