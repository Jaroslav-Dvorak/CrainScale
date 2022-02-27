from threading import Thread
from gui import Indikator
from receiver_232 import Receiver


if __name__ == '__main__':
    indikator = Indikator()
    receiver = Receiver(indikator)

    t1 = Thread(target=receiver.run)
    t1.daemon = True
    t1.start()

    indikator.root.mainloop()
