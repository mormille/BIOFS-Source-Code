# oled_display.py
import machine
import time
import utime
from ssd1306 import SSD1306_I2C  # from Micropython_ssd1306 library, ver .3 by Stefan Lehmann
from machine import Pin, I2C
from oled import Write, GFX, SSD1306_I2C as OLED_SSD1306_I2C  # from Micropython_oled library, ver 1.13 by Yieson Cardona
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

# Define display dimensions.
WIDTH = 128
HEIGHT = 64

# Global variables for our display objects.
i2c = None
oled = None
write15 = None
write20 = None

def init_display():
    """
    Initialize the OLED display.
    Sets up the I2C bus, creates the display instance, and the two font writer objects.
    """
    global i2c, oled, write15, write20
    # Initialize I2C on channel 1 with SDA=Pin14 and SCL=Pin15.
    i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15), freq=400000)
    # Create the SSD1306 display instance.
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
    # Create writer objects with two different fonts.
    write15 = Write(oled, ubuntu_mono_15)  # Smaller font (about 18 characters per line)
    write20 = Write(oled, ubuntu_mono_20)  # Larger font (about 12 characters per line)
    clear_display()
    print("OLED Display initialized")

def clear_display():
    """
    Clears the OLED display.
    """
    oled.fill(0)
    oled.show()

def update_display(timestamp_str, line1, line2, line3, line4=""):
    """
    Displays up to four lines of text along with a timestamp on the OLED.
    
    Args:
        timestamp_str (str): A formatted timestamp string (e.g., "YYYY-MM-DD HH:MM:SS").
        line1 (str): Text for line 1.
        line2 (str): Text for line 2.
        line3 (str): Text for line 3.
        line4 (str, optional): Text for line 4 (default is an empty string).
    """
    clear_display()
    # Display the timestamp on the top line.
    write15.text(timestamp_str, 0, 0)
    # Display subsequent lines of information.
    write15.text(line1, 0, 15)
    write15.text(line2, 0, 30)
    write15.text(line3, 0, 45)
    if line4:
        # If you need to use a different font (e.g., larger) you could choose write20.
        write15.text(line4, 0, 60)
    oled.show()

def show_sensor_data(timestamp, light_data, temperature):
    """
    Formats and displays sensor data on the OLED.
    
    Args:
        timestamp (tuple or str): Either a tuple (year, month, day, hour, minute, second)
                                  or a pre-formatted timestamp string.
        light_data (dict): A dictionary with keys "red", "green", "blue", "ir".
        temperature (float): Temperature value.
    """
    # If timestamp is a tuple, convert it to a formatted string.
    if isinstance(timestamp, tuple):
        timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*timestamp)
    else:
        timestamp_str = timestamp

    # Create display lines using sensor data.
    # Here we combine some light sensor readings on two lines.
    line1 = "Light R:{} G:{}".format(light_data["red"], light_data["green"])
    line2 = "Light B:{} IR:{}".format(light_data["blue"], light_data["ir"])
    line3 = "Temp: {:.2f}C".format(temperature)
    # You can add more information on line4 if needed.
    line4 = ""
    
    update_display(timestamp_str, line1, line2, line3, line4)

# Optional test code to verify the module.
if __name__ == '__main__':
    init_display()
    
    # Run a simple test: show a test message first.
    clear_display()
    write15.text("Testing display", 0, 0)
    write15.text("123456789012345678", 0, 15)
    write15.text("123456789012345678", 0, 30)
    write15.text("123456789012345678", 0, 45)
    oled.show()
    time.sleep(3)
    
    # Now, display date and time.
    current_time = utime.localtime()
    ts = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0],
                                                            current_time[1],
                                                            current_time[2],
                                                            current_time[3],
                                                            current_time[4],
                                                            current_time[5])
    clear_display()
    write15.text("Date = {:02d},{:02d}".format(current_time[1], current_time[2]), 0, 0)
    write15.text("Time = {:02d}:{:02d}".format(current_time[3], current_time[4]), 0, 15)
    write15.text("Line 3 =", 0, 30)
    write15.text("Line 4 =", 0, 45)
    oled.show()
    time.sleep(5)
    
    # Finally, test the show_sensor_data() function with dummy values.
    dummy_light = {"red": 100, "green": 150, "blue": 200, "ir": 250}
    dummy_temp = 26.5
    show_sensor_data(current_time, dummy_light, dummy_temp)
    time.sleep(5)
    
    clear_display()
