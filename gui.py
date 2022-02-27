from tkinter import *
from time import time


class Indikator:
    def __init__(self):
        self.root = Tk()
        self.no_val = "----kg"
        self.curr_val = Label(self.root, text=self.no_val, font=("Courier", 40))
        self.curr_val.pack()
        self.last_update = None
        self.clock()

    def update_val(self, val):
        val = int(val)
        self.curr_val.configure(text=f"{val}kg")
        self.last_update = time()

    def clock(self):
        if self.last_update is None or ((time() - self.last_update) > 10):
            self.curr_val.configure(text=self.no_val)
        self.root.after(1000, self.clock)
