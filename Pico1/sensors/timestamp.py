# timestamp.py
import time

def get_timestamp():
    """
    Returns the current date and time as a formatted string.
    Format: "YYYY-MM-DD HH:MM:SS"
    """
    dt = time.localtime()
    return dt[0], dt[1], dt[2], dt[3], dt[4], dt[5]

# run when executing this module directly.
if __name__ == '__main__':
    for i in range(10):
        t = get_timestamp()
        print("Current Timestamp: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(t[0], t[1], t[2], t[3], t[4], t[5]))
        time.sleep(2)