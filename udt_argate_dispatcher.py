########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer

########################################################################################################################
# описание класса:
# - просто раздаёт сигналы таймера, по которым производится
#   опрос узлов и опрос данных
########################################################################################################################

class UDT_ARGATE_DISPATCHER(QObject):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.timer_CheckNetwork = QTimer()
        self.timer_CheckNetwork.setInterval(5000)
        self.timer_CheckNetwork.start()
        self.timer_CheckNetwork.timeout.connect(self.appData.worker_CheckNetwork.msgprc_OnDoCheck)

        self.timer_GetFieldData = QTimer()
        self.timer_GetFieldData.setInterval(750)
        self.timer_GetFieldData.start()
        self.timer_GetFieldData.timeout.connect(self.appData.worker_FieldAccess.msgprc_OnGetFieldData)

        self.timer_DbWrite = QTimer()
        self.timer_DbWrite.setInterval(500)
        self.timer_DbWrite.start()
        self.timer_DbWrite.timeout.connect(self.appData.worker_MCycle.msgprc_OnPrepareDataForDB)

        self.timer_TickUpdate = QTimer()
        self.timer_TickUpdate.setInterval(200)
        self.timer_TickUpdate.start()
        self.timer_TickUpdate.timeout.connect(self.appData.worker_MCycle.msgprc_OnMainCycle)

    ####################################################################################################################




