import serial
import re
from datetime import datetime
from db import DB
from port_search import port_search


class Receiver:
    def __init__(self, gui):
        pattern = r";\d\d\d\d;\d\d\d\d\d-\d\d\d\d\d\d"
        self.pattern = re.compile(pattern)
        self.port = port_search(9600)
        self.gui = gui
        self.db = DB()

    def run(self):

        saved_id_old = None
        buff = ""
        while True:
            try:
                if not self.port.isOpen():
                    self.port.open()
                data = self.port.read(100)
            except serial.serialutil.SerialException:
                self.port = port_search(9600)
                continue

            data = data.decode("utf-8", errors="ignore")
            buff += data
            match = re.search(string=buff, pattern=self.pattern)
            while match is not None:
                start, end = match.span()
                if start >= 4:
                    start -= 4
                found = buff[start:end]
                buff = buff[end:]
                data = found.strip().split(";")
                if len(data) == 3:
                    current_kg, saved, saved_id_new = found.strip().split(";")
                else:
                    break
                try:
                    current_kg = int(current_kg)
                    saved = int(saved)
                except Exception as e:
                    print(e)
                    break
                if saved_id_old is None:
                    saved_id_old = saved_id_new
                if saved_id_new != saved_id_old:
                    saved_id_old = saved_id_new
                    print("uloženo:", saved)
                    self.db.write(weight=saved)
                curr_time = datetime.now().replace(microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                print(f"{curr_time} {current_kg}kg")
                self.gui.update_val(current_kg)
                match = re.search(string=buff, pattern=self.pattern)
