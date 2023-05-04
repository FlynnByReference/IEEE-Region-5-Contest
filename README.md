# IEEE-Region-5-Contest
University of Arkansas team for IEEE Region 5 robotics competition working code

Object Detection usage: https://github.com/Surya-Murali/Real-Time-Object-Detection-With-OpenCV/blob/master/real_time_object_detection.py

Robot built in colaboration with the University of Arkansas' Robotics Interdisciplinary Organization of Teams: https://hogsync.uark.edu/organization/riot

**Drone:** 
[Ryze DJI Tello] (https://www.ryzerobotics.com/tello)

**Robot:**
1. [Intel Realsense stereo camera] (https://www.intelrealsense.com/depth-camera-d415/)
2. [Nvidia Jetson Nano] (https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/)
3. Pycamera
4. 2 motors
5. 2x2 omni wheels

## IEEE Region 5 Robotics Competition 2023
Detailed rules for the competition can be found at Rules_for_2023_R5_Student_Robotics_V5.pdf.

The goal of the competition is to build a robot that communicates with a drone and work together to navigate a course of boxes in a particular order. The drone must be able to scan QR codes attatched to the tops of boxes indicating which box it is looking at, and the robot must be able to scan QR codes attatched to the inside of the box to indicate the next box to navigate to.

The competition was held in Denver, Colorado in April 2023 for 16 teams from across the middle United States.

## Preparation
Make sure the drone is turned on and connect the Nvidia Jetson Nano to the Tello's wifi network. It will not have any internet connection, so keep that in mind.

## Usage
Run FSM.py to run the Finite State Machine for robot logic, it will automatically send commands to the drone.

## Testing
The Test folder is full of tests to experiment with and make sure the hardware is working as expected.