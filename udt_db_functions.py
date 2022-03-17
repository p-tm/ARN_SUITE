########################################################################################################################

from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime

########################################################################################################################

from enums import *

########################################################################################################################
# описание класса:
# - вспомогательный класс для хранения функций преобразования форматов даты/времени (в формат БД)
########################################################################################################################

class DBTIME():

    @staticmethod
    def QDateTime2DbDateTime(dt):

        return dt.toString("yyyy-MM-dd hh:mm:ss.zzz")

    @staticmethod
    def QTime2DbTime(t):

        return t.toString("hh:mm:ss.zzz")

    @staticmethod
    def DBDateTime2QDateTime(dt):

        return 0


########################################################################################################################
# описание класса:
# - запись для таблицы <tbl_states_history>
########################################################################################################################

class DBREC_STATES_HISTORY():       # это запись для каждого индивидуального state_type_id
                                    # это запись для таблицы <tbl_states_history>

    def __init__(self, machine_tool_id, state_type_id):

        self.rec_time = QDateTime()
        #self.fk_machine_tool_id = ENM_MACHINE_TOOLS.UNKNOWN
        #self.fk_state_type_id = ENM_STATE_TYPES.UNKNOWN
        self.state_value = 0
        self.fk_event_hrec_id = 0
        self.fk_shift_id = 1
        self.b_time = QDateTime()
        self.fk_b_shift_id = 1
        #self.c_time_full = QTime()
        #self.c_time_w_shift = QTime()
        #self.c_time_w_day = QTime()

        self.sql_str_1 = ""



        self.fk_machine_tool_id = machine_tool_id
        self.fk_state_type_id = state_type_id

        _date = QDate(1990, 1, 1)
        _time = QTime(0, 0, 0, 0)

        self.b_time.setDate(_date)
        self.b_time.setTime(_time)

        self.c_time_full = _time
        self.c_time_w_shift = _time
        self.c_time_w_day = _time

    ####################################################################################################################

    def MakeStatesHistoryRec(self):

        s = "("
        s += "TIMESTAMP'" + DBTIME.QDateTime2DbDateTime(self.rec_time) + "',"
        s += str(self.fk_machine_tool_id) + ","
        s += str(self.fk_state_type_id) + ","
        s += str(self.state_value) + ","
        s += str(self.fk_event_hrec_id) + ","
        s += str(self.fk_shift_id) + ","
        s += "TIMESTAMP'" + DBTIME.QDateTime2DbDateTime(self.b_time) + "',"
        s += str(self.fk_b_shift_id) + ","
        s += "INTERVAL'" + DBTIME.QTime2DbTime(self.c_time_full) + "',"
        s += "INTERVAL'" + DBTIME.QTime2DbTime(self.c_time_w_shift) + "',"
        s += "INTERVAL'" + DBTIME.QTime2DbTime(self.c_time_w_day) + "')"

        self.sql_str_1 = s

########################################################################################################################
# описание класса:
# - запись для таблицы <tbl_stat_by_mt>
########################################################################################################################

class DBREC_STAT_BY_MT():   # это запись для каждого индивидуального станка

    def __init__(self, machine_tool_id):
        pass