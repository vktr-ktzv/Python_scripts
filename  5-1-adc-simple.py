import RPi.GPIO as GPIO
import time 

dac = [26, 19, 13, 6, 5, 11, 9, 10]
num_of_bits = len(dac)
maxvoltage = 3.3
levels = 2**num_of_bits
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac , GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

try:
    while True:
        for value in range(256):
            signal = num2dac(value)
            voltage = value / levels * maxvoltage
            time.sleep(0.01)
            CompVal = GPIO.input(comp)
            if CompVal == 0:
                print("ADC val = {:^3} -> {}, input voltage = {:2f}".format(value, signal, voltage))
                
                break
except KeyboardInterrupt:
    print("\n programm stopped by user")

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("\n GPIO cleaned")
