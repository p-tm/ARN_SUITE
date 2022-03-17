########################################################################################################################


from PyQt5.QtCore import QDate, QTime

########################################################################################################################

from enums import *
from udt_arr import UDT_ARR
from udt_mt_info import UDT_MT_INFO
from udt_mt_stat_info import UDT_MT_STAT_INFO
from udt_cl_stat_info import UDT_CL_STAT_INFO
from udt_pulsegen import UDT_PULSEGEN

from udt_interval import UDT_INTERVAL
from udt_piechart_wedge import UDT_PIECHART_WEDGE
from udt_piechart_data import UDT_PIECHART_DATA
from udt_arbmon_app_settings import UDT_ARBMON_APP_SETTINGS
from udt_db_conn_supervisor import UDT_DB_CONN_SUPERVISOR

########################################################################################################################
# описание класса:
# - текущие данные
########################################################################################################################

class UDT_ARBMON_CURRENT_DATA():

    def __init__(self):

        self.date = QDate(0,0,0)
        self.time = QTime(0,0,0)
        self.weekday = None
        self.isWeekend = None
        self.weekendDay = None

        self.day = 0                        # day_id
        self.day_big = 0                    # day_big_id
        self.shiftPlan = 0
        self.shift = 0
        self.isNight = False
        self.scheduledBreak = 0
        self.isDinner = False
        self.shift_number = 0

        self.shiftPlanCaption = ""
        self.shiftCaption = ""                # current shift
        #self.isNightCaption = ""
        self.scheduledBreakCaption = ""       # current scheduled break
        #self.isDinnerCaption = ""


        self.curShiftBTime = QTime()
        self.curShiftETime = QTime()
        self.curScheduledBreakBTime = QTime()
        self.curScheduledBreakETime = QTime()

        self.MT_INFO = UDT_ARR() # list<UDT_MT_INFO>
        self.MT_STAT = UDT_ARR() # две строки
                                 # каждая строка - list<UDT_MT_STAT_INFO (23 записи) + UDT_CL_STAT_INFO (5 записей)>
        #for i in range(17):
        #    mti = UDT_MT_INFO()
        #    mti.mt_id = i + 1
        #    self.MT_INFO.append(mti)





########################################################################################################################
# описание класса:
# - набор данных "приложения"
# - эта структура является контейнером для вообще всех данных приложения
########################################################################################################################

class UDT_ARBMON_APP_DATA():

    ####################################################################################################################

    def __init__(self):

        # all application objects references - for convinience

        # main app

        self.application_TheApp = None
        self.window_MainWindow = None
        self.str_AppDir = ""
        self.str_ResDir = ""

        # app settings

        self.settings = UDT_ARBMON_APP_SETTINGS()
        self.settings_Z1 = UDT_ARBMON_APP_SETTINGS()
        self.settingsFileName = ""
        self.settingsKeeper = None      # QSettings

        # threads

        self.thread_Dispatcher = None
        self.thread_DBAccess = None
        self.thread_MCycle = None

        # core thread functions

        self.worker_Dispatcher = None
        self.worker_DBAccess = None
        self.worker_MCycle = None

        # main GUI objects

        self.pane_Workshop = None
        self.pane_Diagrams = None

        self.currentScreen = 1  # 1 = workshop, 2 = diagrams








        # DB

        self.db = None
        self.dbConnected = False
        self.DB_CONN_SUPERVISOR = UDT_DB_CONN_SUPERVISOR()

        # data

        self.MACHINE_TOOL_CLASSES = UDT_ARR()
        self.MACHINE_TOOLS = UDT_ARR()          # array of <UDT_MACHINE_TOOL>
        self.CD = UDT_ARBMON_CURRENT_DATA()

        #

        self.PIECHART_1_DATA = UDT_PIECHART_DATA()
        self.PIECHART_2_DATA = UDT_PIECHART_DATA()

        #

        self.FOOTPRINT_BLINKER = UDT_PULSEGEN()

        #

        self.init()


    ####################################################################################################################

    def init(self):

        # MT_INFO array has 1 row

        for i in range(23):
            mti = UDT_MT_INFO()
            mti.mt_id = i + 1
            self.CD.MT_INFO.append(mti)

         # MT_STAT array has 2 rows
         # [row 0] - tbl_rt_stat[row 0]
         # [row 1] - tbl_rt_stat[row 1]



        for i in range(2):

            row = UDT_ARR()

            for j in range(23):
                mts = UDT_MT_STAT_INFO()
                mts.mt_id = j + 1
                #self.CD.MT_STAT.append(mts)
                row.append(mts)

            for j in range(5):
                mts = UDT_CL_STAT_INFO()
                mts.class_id = j + 1
                #self.CD.MT_STAT.append(mts)
                row.append(mts)

            self.CD.MT_STAT.append(row)

        #

        self.FOOTPRINT_BLINKER.ms_RTx_CALL = 200
        self.FOOTPRINT_BLINKER.ms_TIME_ON = 1000
        self.FOOTPRINT_BLINKER.ms_TIME_OFF = 1000

        #

        for k in range(5):
            self.PIECHART_1_DATA.WEDGES.append(UDT_PIECHART_WEDGE())
        for l in range(9):
            self.PIECHART_2_DATA.WEDGES.append(UDT_PIECHART_WEDGE())