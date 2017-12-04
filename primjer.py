import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
from time import sleep
GPIO.setwarnings(False)
try:
    GPIO.cleanup()
except RuntimeWarning:
    pass
########################
########################


pin = 33

GPIO.setup(pin, GPIO.OUT)


GPIO.output(pin, 1)
sleep(0.5)

GPIO.output(pin, 0)
sleep(0.5)

GPIO.output(pin, 1)
sleep(0.5)

GPIO.output(pin, 0)
sleep(0.5)

#GPIO.cleanup()
print("ok")

