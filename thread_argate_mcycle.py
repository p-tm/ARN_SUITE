#################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime

from window_argate_main_window import WINDOW_ARGATE_MAIN_WINDOW

#################################################################
# описание класса:
# класс потока
# в этом потоке производится обсчёт полученных данных
# и подготовка их к записи в БД
# и вообще все обсчёты данных
#################################################################

class THREAD_ARGATE_MCYCLE(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс MCycle запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс MCycle запущен")

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс MCycle завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс MCycle завершён")