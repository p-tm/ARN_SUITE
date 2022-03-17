########################################################################################################################

from PyQt5.QtCore import QThread

########################################################################################################################
# описание класса:
# - объект-поток
#
########################################################################################################################

class THREAD_ARTERM_DISPATCHER(QThread):


    def __init__(self):

        super().__init__()

        self.started.connect(self.on_started)
        self.finished.connect(self.on_finished)

    def on_started(self):
        print("процесс Dispatcher запущен")

    def on_finished(self):
        print("процесс Dispatcher завершён")

