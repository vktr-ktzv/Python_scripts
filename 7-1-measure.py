#import libraries
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

#values
max_value = 256
max_voltage = 3.3

# define GPIOs
leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setwarnings(False)

# setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

# function to convert decimal number into binary list
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

# function to measure valuecurrent_value level (from 0 to 255)
def adc():
    value = 0
    for i in range (8):
        GPIO.output(dac[i], 1)
        time.sleep(0.01)
        if not(GPIO.input(comp)):
            GPIO.output(dac[i], 0) 
        else:
            value += (1<<(7-i))
    
    GPIO.output(dac, 0) 
    return value


# function to show valuecurrent_value in binary form on leds
def show_value(value):
    GPIO.output(leds, decimal2binary(value))

# start measurement
try:
    adc_results = []

    # start charging
    start_time = time.time()
    GPIO.output(troyka, 1)
    current_value = 0
    while current_value < 0.94*max_value:
        current_value = adc()
        show_value(current_value)
        print(current_value, "{:.2f}V".format(current_value/max_value*max_voltage))
        adc_results.append(current_value)

    # start discharging
    charge_time = time.time()
    current_value = adc()
    GPIO.output(troyka, 0)
    while current_value > 0.02*max_value:
        show_value(current_value)
        print(current_value, "{:.2f}V".format(current_value/max_value*max_voltage))
        adc_results.append(current_value)
        current_value = adc()
    end_time = time.time()

    # calculate experiment time
    experiment_time = end_time - start_time

    # build the plot
    plt.plot(adc_results)
    plt.show()

    # # write data into files
    # with open("data.txt", 'w') as data:
    #     for item in adc_results:
    #        # data.write(' \n'.join([str(item)]))
    #        data.write('{}\n'.format(str(item)))
        
    #     data.close()

    # with open("settings.txt", 'w') as settings:
    #     settings.write("Discretization frequency: {:.2f}\n".format(len(adc_results)/experiment_time))
    #     settings.write("Quantization step: {:.2f}V".format(max_voltage/max_value))

    #     settings.close()
   
    # print experiment data
    print("Experiment time: ", str(experiment_time))
    print("charge time: ", str(charge_time - start_time))
    print("Measurement period: {:.2f}".format(experiment_time/len(adc_results)))
    print("Discretization frequency: {:.2f}".format(len(adc_results)/experiment_time))
    print("Quantization step: {:.2f}V".format(max_voltage/max_value))

# turning off GPIOs
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
