#################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime


#################################################################
# описание класса:
# класс потока
# в этом потоке производится обсчёт полученных данных
# и подготовка их к записи в БД
# и вообще все обсчёты данных
#################################################################

class THREAD_ARBMON_MCYCLE(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс рабочего цикла запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс рабочего цикла запущен")

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс рабочего цикла завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс рабочего цикла завершён")