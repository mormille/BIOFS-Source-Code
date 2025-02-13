# led_control.py
import machine
import utime

# Initialize the external LED on Pin 13.
led_external = machine.Pin(13, machine.Pin.OUT)

def error_signal(interval=0.5):
    """
    Blinks the LED indefinitely to signal an error condition.
    
    Args:
        interval (float): The delay (in seconds) between LED toggles.
    """
    while True:
        led_external.toggle()
        utime.sleep(interval)

def turn_on():
    """
    Turns the LED on (solid red light).
    """
    led_external.on()

def turn_off():
    """
    Turns the LED off.
    """
    led_external.off()