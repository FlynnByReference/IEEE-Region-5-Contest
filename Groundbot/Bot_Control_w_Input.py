
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


def start_transitions(count):
    count = 0
    newState = "Drive_state"
    return (newState, count)

def drive_state_1(count):
    if count < 7:
        newState = "QR_state"
    else:
        newState = "Exit_state"
    return (newState, count)

def qr_read(count):
    newState = "Drive_state2"
    return (newState, count)

def drive_state_2(count):
    newState = "Locate_state"
    return (newState, count)

def locate_box(count):
    #Rotate left until a box is found
    #if not, Rotate right until a box is found
    newState = "Drive_state3"
    return (newState, count)

def drive_state_3(count):
    newState = "Center_state"
    return (newState, count)

def center_box(count):
    print("Looped")
    print(count)
    count = count + 1
    newState = "Drive_state"
    return (newState, count)

def exit_state(count):
    print("Exiting")
    return ("Exit_state", "")


m = StateMachine()
m.add_state("Start", start_transitions)
m.add_state("Drive_state", drive_state_1)
m.add_state("QR_state", qr_read)
m.add_state("Drive_state2", drive_state_2)
m.add_state("Locate_state", locate_box)
m.add_state("Drive_state3", drive_state_3)
m.add_state("Center_state", center_box)
m.add_state("Exit_state", None, end_state=1)
m.set_start("Start")
m.run("")