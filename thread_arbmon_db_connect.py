########################################################################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime

########################################################################################################################
# описание класса:
# - объект-поток
#
########################################################################################################################

class THREAD_ARBMON_DB_CONNECT(QThread):

    signal_ThreadStartedB = pyqtSignal()    # используется для подключения к БД

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        print("процесс DBAccess запущен")
        self.signal_ThreadStartedB.emit()

    def on_finished(self):
        print("процесс DBAccess завершён")