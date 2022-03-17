import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot


class UDT_TRACKER_EXPORTER(QObject):

    signal_Done = pyqtSignal()

    def __init__(self, *params):

        super().__init__()

        self.list = params[0]
        self.file_name = params[1]

        self.signal_Done.connect(self.deleteLater)

    @pyqtSlot()
    def exportToFile(self):

        file = open(self.file_name, "w")

        for k, item in enumerate(self.list):

            txt = str(k) + ": " + item + "\n"
            file.write(txt)

        file.close()

        self.signal_Done.emit()


