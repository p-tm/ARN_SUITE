#################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime

#################################################################
# описание класса:
#################################################################

class THREAD_ARGATE_DB_CONNECT(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)
    signal_ThreadStartedB = pyqtSignal()    # используется для подключения к БД

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс DBAccess запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс DBAccess запущен")
        self.signal_ThreadStartedB.emit()

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс DBAccess завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс DBAccess завершён")