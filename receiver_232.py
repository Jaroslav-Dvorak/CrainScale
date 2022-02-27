import serial
import re
from datetime import datetime


def is_rpi():
    try:
        with open('/sys/firmware/devicetree/base/model') as model:
            rpi_model = model.read()
    except FileNotFoundError:
        return False
    else:
        return rpi_model


class Receiver:
    def __init__(self, gui):
        dev = "/dev/ttyUSB0" if is_rpi() else "COM3"
        bauld = 9600
        pattern = r";\d\d\d\d;\d\d\d\d\d-\d\d\d\d\d\d"
        self.pattern = re.compile(pattern)
        self.port = serial.Serial(dev, bauld)
        self.gui = gui

    def run(self):
        if not self.port.isOpen():
            self.port.open()
        saved_id_old = None
        buff = ""
        while True:
            data = self.port.read(1024)
            data = data.decode("utf-8", errors="ignore")
            buff += data
            match = re.search(string=buff, pattern=self.pattern)
            while match is not None:
                start, end = match.span()
                if start >= 4:
                    start -= 4
                found = buff[start:end]
                buff = buff[end:]
                current, saved, saved_id_new = found.strip().split(";")
                if saved_id_old is None:
                    saved_id_old = saved_id_new
                if saved_id_new != saved_id_old:
                    saved_id_old = saved_id_new
                    print("uloženo:", saved)
                    with open("crain.txt", "a", encoding="utf-8") as f:
                        curr_time = datetime.now().replace(microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                        f.write(f"{curr_time} {saved}\n")
                print("aktuální:", current)
                self.gui.update_val(current)
                match = re.search(string=buff, pattern=self.pattern)
