#################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime

#################################################################
# описание класса:
#################################################################
# класс потока
# в этом потоке производится анализ, какие из узлов доступны
#################################################################

class THREAD_CHECK_NETWORK(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс CheckNetwork запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс CheckNetwork запущен")

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс CheckNetwork завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс CheckNetwork завершён")