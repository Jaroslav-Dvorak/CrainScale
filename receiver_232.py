import serial
import re
from datetime import datetime
from db import DB


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
        self.db = DB()

    def run(self):
        if not self.port.isOpen():
            self.port.open()
        saved_id_old = None
        buff = ""
        while True:
            data = self.port.read(100)
            data = data.decode("utf-8", errors="ignore")
            buff += data
            match = re.search(string=buff, pattern=self.pattern)
            while match is not None:
                start, end = match.span()
                if start >= 4:
                    start -= 4
                found = buff[start:end]
                buff = buff[end:]
                current_kg, saved, saved_id_new = found.strip().split(";")
                try:
                    current_kg = int(current_kg)
                    saved = int(saved)
                except Exception as e:
                    print(e)
                    continue
                curr_time = datetime.now().replace(microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                if saved_id_old is None:
                    saved_id_old = saved_id_new
                if saved_id_new != saved_id_old:
                    saved_id_old = saved_id_new
                    print("uloženo:", saved)
                    self.db.write(weight=saved)
                print(f"{curr_time} {current_kg}kg")
                self.gui.update_val(current_kg)
                match = re.search(string=buff, pattern=self.pattern)
