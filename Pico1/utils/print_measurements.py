# print_measurements.py
# module that provides a function to print the  measurements on the console

def print_measures(i, light, temperature, dt):
    print("")
    print("=> Measurement {}.".format(i+1))
    print("Timestamp: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]))
    print("Light: Red={}, Green={}, Blue={}, IR={}.".format(light["red"], light["green"], light["blue"], light["ir"]))
    print("Temperature: {:.2f}°C.".format(temperature))
    print("------------------------------------------")