import time
import si7021

# Connect sensor
sensor = si7021.SI7021()

count = 0
while True:
    hum, temp = None

    try:
        hum = sensor.getRH()
        temp = sensor.readTemp()
    except OSError as e:
        print("Exception occured while measuring data")
        print("errno: ", e.errno)

    print(hum, temp)

    time.sleep(10)