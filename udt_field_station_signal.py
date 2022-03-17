########################################################################################################################

from PyQt5.QtCore import QDateTime, QDate, QTime

########################################################################################################################

from enums import *

########################################################################################################################
# описание класса:
# - это зеркало данных из ПЛК - по кнопкам или другим сигналам
# - все сигналы со станции считаем "кнопкамИ"
########################################################################################################################

class UDT_FIELD_STATION_SIGNAL():

    #id = ENM_HANDPULT_BUTTONS.UNKNOWN

    # часть - зеркало из ПЛК

    #Q = False
    #QR_E = False
    #QR_Time = QDateTime()
    #QF_E = False
    #QF_Time = QDateTime()

    # часть - данные, которые рассчитываются и хранятся в программе



    def __init__(self, button_id):

        self.id = button_id

        # зеркало из ПЛК

        self.Q = False
        self.QR_E = False
        self.QR_Time = QDateTime()
        self.QF_E = False
        self.QF_Time = QDateTime()

        # доп.данные в ПК

        self.Q_Z1 = False

        self.timeQR_a = QDateTime()     # absolute
        self.timeQF_a = QDateTime()     # absolute

        self.timeQR_s = QDateTime()     # within shift
        self.timeQF_s = QDateTime()     # within shift

        self.timeQR_d = QDateTime()     # within day
        self.timeQF_d = QDateTime()     # within dat

        self.msActiveElapsedTime_a = 0
        self.msInactiveElapsedTime_a = 0

        self.msActiveElapsedTime_s = 0
        self.msInactiveElapsedTime_s = 0

        self.msActiveElapsedTime_d = 0
        self.msInactiveElapsedTime_d = 0


