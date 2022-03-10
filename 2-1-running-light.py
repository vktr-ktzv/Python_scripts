import RPi.GPIO as GPIO
import time 



led = [21, 20, 16, 12, 7, 8, 25, 24]


GPIO.setmode(GPIO.BCM)

GPIO.setup(led, GPIO.OUT)

for j in range (3):
    for i in led:
        GPIO.output(i, 3)
        time.sleep(0.2)
        GPIO.output(i, 0)



GPIO.cleanup()



