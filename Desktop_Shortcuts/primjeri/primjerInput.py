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

GPIO.setup(pin, GPIO.IN)

while True:
    if GPIO.input(pin):
        print("ok")
    

