import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


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


GPIO.setwarnings(False)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def num2dac(value):
    signal = dec2bin(value)
    GPIO.output(dac, signal)
    return signal

def adc():
    value = 0
    for i in 7, 6, 5, 4, 3, 2, 1, 0:
        GPIO.output(DacRev[i], 1)
        arr[7 - i] = 1
        time.sleep(0.01)
        if (GPIO.input(cmp) == 0):
            GPIO.output(DacRev[i], 0)
            arr[7 - i] = 0

        else:
            value += (1<<(7-i))
    return value

def show_voltage(value):
    GPIO.output(led, dec2bin(value))

try:
    voltage_results = []

    # start charging
    start_time = time.time()
    GPIO.output(troyka, 1)
    current_voltage = adc()
    while current_voltage < 0.96*256:
        show_voltage(current_voltage)
        print(current_voltage, "{:.2f}V".format(current_voltage/256*3.3))
        voltage_results.append(current_voltage/256*3.3)
        current_voltage = adc()

    # start discharging
    current_voltage = adc()
    GPIO.output(troyka, 0)
    while current_voltage > 0.02*256:
        show_voltage(current_voltage)
        print(current_voltage, "{:.2f}V".format(current_voltage/256*3.3))
        voltage_results.append(current_voltage/256*3.3)
        current_voltage = adc()
    end_time = time.time()

    # calculate experiment time
    experiment_time = end_time - start_time

    # build the plot
    plt.plot(voltage_results)
    plt.show()

    # write data into files
    with open("data.txt", 'w') as data:
        for item in voltage_results:
            data.write('\n'.join([str(item)]))
    with open("settings.txt", 'w') as settings:
        settings.write("Discretization frequency: {:.2f}".format(len(voltage_results)/experiment_time), '\n')
        settings.write("Quantization step: {:.2f}V".format(3.3/256))

    # print experiment data
    print("Experiment time: ", str(experiment_time))
    print("Measurement period: {:.2f}".format(experiment_time/len(voltage_results)))
    print("Discretization frequency: {:.2f}".format(len(voltage_results)/experiment_time))
    print("Quantization step: {:.2f}V".format(3.3/256))

# turning off GPIOs
finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()