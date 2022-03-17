########################################################################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime

from window_argate_main_window import WINDOW_ARGATE_MAIN_WINDOW

########################################################################################################################
# описание класса:
# класс потока
# в этом потоке происводится получение данных со станций
# сбора данных
########################################################################################################################

class THREAD_FIELD_STATION_CONNECT(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс FieldIOAccess запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс FieldIOAccess запущен")

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс FieldIOAccess завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс FieldIOAccess завершён")