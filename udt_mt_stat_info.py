########################################################################################################################
from PyQt5.QtCore import QTime

from datetime import timedelta

########################################################################################################################

from enums import *
from udt_interval import UDT_INTERVAL

########################################################################################################################
# описание класса:
# - состояние станка - структура похожая на структуру которая хранится в БД (массив времён)
########################################################################################################################

class UDT_MT_STAT_INFO():

    def __init__(self):

        self.mt_id = ENM_MACHINE_TOOLS.UNKNOWN

        self.offline = UDT_INTERVAL()
        self.alr_failure = UDT_INTERVAL()
        self.alr_material = UDT_INTERVAL()
        self.stp_failure = UDT_INTERVAL()
        self.stp_material = UDT_INTERVAL()
        self.stp_process = UDT_INTERVAL()
        self.stp_quality = UDT_INTERVAL()
        self.aux_1 = UDT_INTERVAL()
        self.aux_2 = UDT_INTERVAL()

        self.alr_sum = UDT_INTERVAL()
        self.stp_sum = UDT_INTERVAL()

