# Module for the S11059 Hamamatsu Light Sensor
import machine
import time

# sensor I2C address and register constants
SENSOR_ADDRESS = 0x2A
CONTROL_REG1   = 0x00
CONTROL_REG2   = 0x01
DATA_START_REG = 0x03


# I2C on the Raspberry Pi Pico 
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17), freq=400000)

# The Internal LED is defined for the Raspberry Pi Pico W, NOT the regular Pico
#led = machine.Pin('WL_GPIO0',machine.Pin.OUT)


def init_sensor():
    """
    Initialize the sensor:
      - Reset to factory defaults
      - Set initial control register settings.
    """
    # Reset sensor to factory default
    i2c.writeto_mem(SENSOR_ADDRESS, CONTROL_REG1, b'\x00')
    time.sleep(1)
    
    # Set control register 1 to start the sensor
    i2c.writeto_mem(SENSOR_ADDRESS, CONTROL_REG1, b'\x09')
    time.sleep(0.5)
    print("Light sensor initialized")
    
def get_light_values():
    """
    Reads the light sensor and returns a dictionary with the following keys:
        'red', 'green', 'blue', 'ir'
    
    It does this by:
      - Writing to CONTROL_REG2 to start output data mode.
      - Reading 8 bytes from the sensor.
      - Combining each pair of bytes into an integer for red, green, blue, and IR.
    """
    # Tell the sensor to prepare data output by writing to CONTROL_REG2
    i2c.writeto_mem(SENSOR_ADDRESS, CONTROL_REG2, b'\x03')
    time.sleep(1)
    
    # Read 8 bytes from the sensor starting at DATA_START_REG
    data = i2c.readfrom_mem(SENSOR_ADDRESS, DATA_START_REG, 8)
    time.sleep(1)
    
    # Convert the two-byte readings into integer values
    red   = (data[0] << 8) | data[1]
    green = (data[2] << 8) | data[3]
    blue  = (data[4] << 8) | data[5]
    ir    = (data[6] << 8) | data[7]
    
    # Return the readings as a dictionary
    return {'red': red, 'green': green, 'blue': blue, 'ir': ir}

if __name__ == '__main__':
    print("Initializing sensor...")
    init_sensor()
    for i in range(10):
        values = get_light_values()
        print("Measurement {}: Red: {}, Green: {}, Blue: {}, IR: {}.".format(i+1, values["red"], values["green"], values["blue"], values["ir"]))
        time.sleep(2)
