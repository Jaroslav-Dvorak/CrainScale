import serial
from is_rpi import is_rpi


def port_search(bauld):

    predev = "/dev/ttyUSB" if is_rpi() else "COM"

    while True:
        for p in range(10):
            dev = predev + str(p)
            print(dev)
            try:
                port = serial.Serial(dev, bauld)
            except serial.serialutil.SerialException:
                continue
            else:
                return port

port_search(9600)
