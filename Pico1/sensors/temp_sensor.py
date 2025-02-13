# temp_sensor.py
import machine
import onewire
import ds18x20
import time


#  remember GP pin 22 is actual pin #29
# the signal wire on pin 22 should use a pull up resistor 3.3K or 4.7K to high 3.3 Volts
ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# assumption only one temp sensor
roms = ds_sensor.scan()
if not roms:
    raise Exception("No (Temperature sensor (DS18X20) found!")
else:
    print("Temperature sensor found.")
    #print("DS18X20 device(s) found:", roms)

def read_temperature():
    """
    Initiates a temperature conversion and reads the temperature from the first
    DS18X20 device found.

    Returns:
        float: The temperature in degrees Celsius.
    """
    # Start temperature conversion.
    ds_sensor.convert_temp()
    # Wait for the conversion to complete (typical max conversion time is 750ms).
    time.sleep_ms(750)
    # Read the temperature from the first found device.
    temperature = ds_sensor.read_temp(roms[0])
    return temperature

# When running this module directly, print temperature readings in a loop.
if __name__ == '__main__':
    while True:
        temp = read_temperature()
        print("Temperature:", temp)
        time.sleep(3)