import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

GPIO.output(17, GPIO.input(27))