import RPi.GPIO as GPIO
import time 

led = [21, 20, 16, 12, 7, 8, 25, 24]
aux = [22, 23, 27, 18, 15, 14 ,3, 2]

GPIO.setmode(GPIO.BCM)

GPIO.setup(led, GPIO.OUT)
for i in range(len(aux)): 
    GPIO.setup(aux[i], GPIO.IN)




while 1:
    GPIO.output(led[i%8], GPIO.input(aux[i%8]))
    i+=1
    