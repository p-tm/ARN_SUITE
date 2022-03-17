########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer

########################################################################################################################
# описание класса:
# - просто раздаёт сигналы таймера, по которым производится
#   опрос узлов и опрос данных
########################################################################################################################

class UDT_ARTERM_DISPATCHER(QObject):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data


        self.timer_MainCycle = QTimer()
        self.timer_MainCycle.setInterval(200)   # с этой периодичностью производится main_cycle а также обновление окон (!)
        self.timer_MainCycle.start()
        self.timer_MainCycle.timeout.connect(self.appData.worker_MCycle.msgprc_OnMainCycle)

        self.timer_GetRTData = QTimer()
        self.timer_GetRTData.setInterval(500)   # обращение к БД 2 р/сек - чаще думаю нельзя
        self.timer_GetRTData.start()
        self.timer_GetRTData.timeout.connect(self.appData.worker_DBAccess.msgprc_ReadRTData)


    ####################################################################################################################