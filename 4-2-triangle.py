import RPi.GPIO as GPIO
import time

dac = [26,19,13,6,5,11,9,10]

def decimal2binary(value):
 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

a = float(input("input period \n"))

try: 
    i = 0  
     
    flag = 1
    while (1):
        
        
        
        time.sleep(a/512)
        if  (flag == 1):
            if i >= 255:
                flag = 0
            
            i+=1
        if (flag == 0):
            if (i <= 1):
                flag = 1

            i-=1
        GPIO.output(dac, decimal2binary(int(i)))
            
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()          