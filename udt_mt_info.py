from enums import *
from udt_mt_count_flags import UDT_MT_COUNT_FLAGS

########################################################################################################################
# описание класса:
# - состояние станка - структура похожая на структуру которая хранится в БД (массив битов)
########################################################################################################################

class UDT_MT_INFO():

    ####################################################################################################################

    def __init__(self):

        self.mt_id = ENM_MACHINE_TOOLS.UNKNOWN

        self.offline = False
        self.alr_failure = False
        self.alr_material = False
        self.stp_failure = False
        self.stp_material = False
        self.stp_process = False
        self.stp_quality = False
        self.aux_1 = False
        self.aux_2 = False

        self.com_yellow = False
        self.com_red = False

        self.view = 1   # normal view

        self.cf = UDT_MT_COUNT_FLAGS()

    ####################################################################################################################

    def toChar(self, val):

        if val:
            return "t"
        else:
            return "f"

    ####################################################################################################################

    def toDBField(self):

        q_str = "(" + self.toChar(self.offline) + "," + \
                self.toChar(self.alr_failure) + "," + \
                self.toChar(self.alr_material) + "," + \
                self.toChar(self.stp_failure) + "," + \
                self.toChar(self.stp_material) + "," + \
                self.toChar(self.stp_process) + "," + \
                self.toChar(self.stp_quality) + "," + \
                self.toChar(self.aux_1) + "," + \
                self.toChar(self.aux_2) + ")"

        return q_str
    ####################################################################################################################

    def update(self):

            self.com_yellow = not self.offline and( self.alr_failure or self.alr_material )
            self.com_red = not self.offline and (self.stp_failure or self.stp_material or self.stp_process or self.stp_quality)

            if self.offline:
                self.view = 0   # grey footprint
            else:
                if self.com_red:
                    self.view = 3   # red footprint
                elif self.com_yellow:
                    self.view = 2   # yellow footprint
                else:
                    self.view = 1   # black footprint (machine tool is online and no error encountered)

    ####################################################################################################################

    def cfToDBField(self):

        q_str = "(" + self.toChar(self.cf.count_alr_time) + "," + \
                self.toChar(self.cf.count_stp_time) + ")"

        return q_str

    ####################################################################################################################





