import cv2
from drone_class import DroneClass

test = DroneClass()

data = test.scanQRCode()

print(data)

# test.flyToBox()
