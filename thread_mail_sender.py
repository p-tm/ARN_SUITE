#################################################################

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime

#################################################################
# описание класса:
#################################################################

class THREAD_MAIL_SENDER(QThread):

    signal_ThreadStarted = pyqtSignal(str)
    signal_ThreadFinished = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        self.signal_ThreadStarted.emit(
            "процесс MailSender запущен @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс MailSender запущен")

    def on_finished(self):
        self.signal_ThreadFinished.emit(
            "процесс MailSender завершён @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        print("процесс MailSender завершён")