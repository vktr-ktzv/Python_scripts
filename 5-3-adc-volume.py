import RPi.GPIO as GPIO
import time



dac = [26, 19, 13,  6, 5, 11,  9, 10]
DacRev = [10,  9, 11,  5, 6, 13, 19, 26]
arr = [ 0,  0,  0,  0, 0,  0,  0,  0]
led = [21, 20, 16, 12, 7,  8, 25, 24]

bits = len(dac)
troyka = 17
cmp = 4
levels = 2**bits
maxvoltage = 3.3

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(cmp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    for i in 7, 6, 5, 4, 3, 2, 1, 0:
        GPIO.output(DacRev[i], 1)
        arr[7 - i] = 1
        time.sleep(0.01)
        if (GPIO.input(cmp) == 0):
            GPIO.output(DacRev[i], 0)
            arr[7 - i] = 0
    return

try:
    while True:
        value   = 0
        arr     = [0, 0, 0, 0, 0, 0, 0 , 0]
        arr_led = [0, 0, 0, 0, 0, 0, 0 , 0]

        GPIO.output(dac, arr)
        adc()

        for j in range (7):
            value += arr[j] * (2**(7-j))
            voltage = value / levels * maxvoltage
        
        signal = dec2bin(value)

        value1 = value 

        for k in range(8):
            if value >= 256 / 8:
                arr_led[k] = 1
                value -= 256 / 8

        GPIO.output(led, arr_led)
        print("ADC val = {:^3} -> {}, input voltage = {:2f}".format(value1, signal, voltage))

except KeyboardInterrupt:
    print("\n programm stopped by user")
    
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(led)
    print("\n GPIO cleaned")
 