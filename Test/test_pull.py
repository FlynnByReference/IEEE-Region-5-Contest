import Jetson.GPIO as GPIO

testPin = 11

GPIO.setmode(GPIO.BOARD)


tempVal = None
GPIO.setup(testPin, GPIO.IN)

loopVal = True
while loopVal:
	pinValue = GPIO.input(testPin)
	if pinValue == GPIO.LOW:
		print("Low")
	else:
		print("High")

GPIO.cleanup()
