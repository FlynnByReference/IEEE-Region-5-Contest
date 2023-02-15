# from main import
import pygame
import sys
from djitellopy import tello

display = pygame.display.set_mode((10, 10))
maverick = tello.Tello()
maverick.connect()
# \\\maverick.turn_motor_on()
print(maverick.get_battery())

# creating a running loop
while True:

    # creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                maverick.move("back", 20)
                print("s")
            if event.key == pygame.K_a:
                maverick.move("left", 20)
                print("a")
            if event.key == pygame.K_w:
                maverick.move("forward", 20)
                print("s")
            if event.key == pygame.K_d:
                maverick.move("right", 20)
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