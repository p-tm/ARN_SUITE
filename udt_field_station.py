########################################################################################################################

from udt_field_station_signal import UDT_FIELD_STATION_SIGNAL


from enums import *
from udt_db_functions import DBREC_STATES_HISTORY


########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_FIELD_STATION_PAR():

    def __init__(self, machine_tool_id):

        self.port = 4840
        #self.string_Port = "4840"

        self.id = machine_tool_id   # совпадает с ID в БД
        self.mt_class_id = 0        # совпадает с ID в БД

        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY:
            self.string_IP = "172.31.90.6" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN:
            self.string_IP = "172.31.90.7" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600:
            self.string_IP = "172.31.90.8" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000:
            self.string_IP = "172.31.90.9" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000:
            self.string_IP = "172.31.90.10" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT:
            self.string_IP = "172.31.90.11" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1:
            self.string_IP = "172.31.90.12" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2:
            self.string_IP = "172.31.90.13" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM:
            self.string_IP = "172.31.90.14" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL:
            self.string_IP = "172.31.90.15" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3:
            self.string_IP = "172.31.90.16" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P6_TRUBEND:
            self.string_IP = "172.31.90.17" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN:
            self.string_IP = "172.31.90.18" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW:
            self.string_IP = "172.31.90.19" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT:
            self.string_IP = "172.31.90.20" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT:
            self.string_IP = "172.31.90.21" ; self.persists = True
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_17:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_18:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_19:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_20:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_21:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_22:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_23:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_24:
            self.string_IP = "0.0.0.0" ; self.persists = False
        if machine_tool_id == ENM_MACHINE_TOOLS.MT_25:
            self.string_IP = "0.0.0.0" ; self.persists = False

        self.string_Socket = self.string_IP + ":" + str(self.port)

########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_FIELD_STATION_DAT():

    def __init__(self, machine_tool_id):

        self.alive = False

        self.signals = list([])     # list<UDT_FIELD_STATION_SIGNAL>

        self.rawSourceArray = None  # "сырой" неразобранный массив данных из ПЛК

        #

        self.sock = None
        self.socket_error = True
        self.opc_ua_client = None
        self.ouc_connected = False  # opc_ua_client is connected
        self.ouc_node = None  # opc_ua_client "node" (data node)

        #

        self.statesHistoryData = list([])   # list<DBREC_STATES_HISTORY> - данные для подготовки
                                            # для записи в БД

        #

        #self.fullSqlRequest = ""  # это запрос на запись группы строк (по всем сигналам) в <tbl_states_history>
        self.sqlstr_StatesHistory = "" # это запрос на запись группы строк (по всем сигналам) в <tbl_states_history>
        self.sqlstr_StatByMT = "" # это запрос на запись строки в <tbl_stat_by_mt>

        #

        if machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY or \
           machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN or \
           machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600 or \
           machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000 or \
           machine_tool_id == ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000 or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1 or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2 or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3 or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P6_TRUBEND or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN or \
           machine_tool_id == ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW or \
           machine_tool_id == ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT or \
           machine_tool_id == ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_17 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_18 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_19 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_20 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_21 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_22 or \
           machine_tool_id == ENM_MACHINE_TOOLS.MT_23 :

            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.AUX_1))
            self.signals.append(UDT_FIELD_STATION_SIGNAL(ENM_FIELD_STATION_SIGNALS.AUX_2))

            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_ALARM_ON_FAILURE))  # кнопка
            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_ALARM_ON_MATERIAL))  # кнопка
            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_STOP_ON_FAILURE))  # кнопка
            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_STOP_ON_MATERIAL))  # кнопка
            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_STOP_ON_PROCESS))  # кнопка
            #self.statesHistoryData.append(DBREC_STATES_HISTORY(machine_tool_id, ENM_STATE_TYPES.BUTTON_STOP_ON_QUALITY))  # кнопка

########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_FIELD_STATION():

    def __init__(self, machine_tool_id):

        self.PAR = UDT_FIELD_STATION_PAR(machine_tool_id)
        self.DAT = UDT_FIELD_STATION_DAT(machine_tool_id)




