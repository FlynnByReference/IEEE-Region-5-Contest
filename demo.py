# from main import
import sys
from djitellopy import tello

maverick = tello.Tello()
maverick.connect()
# \\\maverick.turn_motor_on()
print(maverick.get_battery())

maverick.takeoff()
for i in range(2):
    maverick.move("right", 500)
maverick.rotate_counter_clockwise(90)
for i in range(2):
    maverick.move("right", 500)
maverick.rotate_counter_clockwise(90)
maverick.land()
# for i in range(4):
#     maverick.move("right", 500)
# maverick.rotate_counter_clockwise(90)
# for i in range(6):
#     maverick.move("right", 500)
# maverick.rotate_counter_clockwise(90)
# for i in range(2):
#     maverick.move("right", 500)
# maverick.rotate_counter_clockwise(90)

sys.exit()