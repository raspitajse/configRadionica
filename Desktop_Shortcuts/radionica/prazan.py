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



