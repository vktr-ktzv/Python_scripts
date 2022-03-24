import RPi.GPIO as GPIO

dac = [26,19,13,6,5,11,9,10]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]


try:
    while(1):
        a = input("input val\n")
        if(a == 'q'):
            break
        
        

        if  not a.isdigit(): 
            print("Вы ввели неподходящее значение.. Пока")
            break
    
        if int(a) > 255:
            print("Вы ввели неподходящее значение.. Пока")
            break



        GPIO.output(dac, decimal2binary(int(a)) )
        print("Предполагаемое напряжение - {:.3f}".format(int(a)/256*3.3))

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()