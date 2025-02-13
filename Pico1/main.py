# main.py

#Importing Sensors
from sensors import s11059_light_sensor as hamamatsu_sensor
from sensors import temp_sensor
from sensors import timestamp
#Importing Utils
from utils import oled_display
from utils import print_measurements as pm
from utils import led_control
#Importing necessary libraries
import time

# Initializing sensors (necessary to do it once at the beginning of the script)
hamamatsu_sensor.init_sensor()
oled_display.init_display()

def read_sensors(i):
    """
    Retrieve measurements from all sensors in Pico 1
    """
    # Get the light sensor values.
    light = hamamatsu_sensor.get_light_values()
    # Get temperature sensor reading.
    temperature = temp_sensor.read_temperature()
    # Get the current timestamp from the timestamp module.
    dt = timestamp.get_timestamp()
    
    # print the measurements to the console
    pm.print_measures(i, light, temperature, dt)
    # display the measurements on the OLED display
    oled_display.show_sensor_data(dt, light, temperature)
    
    #return light, temperature, dt
    
try:
    for i in range(5):
        # get and display the measurements from the sensors
        read_sensors(i)
        time.sleep(2)
except Exception as e:
    print("An error ocurred:", e)
    # In case of an error, signal it by blinking the LED light.
    oled_display.clear_display()
    led_control.error_signal()

print("")
print("Finished taking measurements.")
oled_display.clear_display()
led_control.turn_on()
time.sleep(5)
led_control.turn_off()
