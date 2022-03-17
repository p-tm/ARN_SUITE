########################################################################################################################


########################################################################################################################

from udt_arterm_app_settings import UDT_ARTERM_APP_SETTINGS
from udt_pulsegen import UDT_PULSEGEN

from enums import *
from global_functions import *
from udt_table_model_classes import *
from udt_arr import UDT_ARR
from udt_mt_info import UDT_MT_INFO
from udt_mt_stat_info import UDT_MT_STAT_INFO
from udt_cl_stat_info import UDT_CL_STAT_INFO
from udt_pulsegen import UDT_PULSEGEN
from udt_day_schedule_data import UDT_DAY_SCHEDULE_DATA
from udt_db_conn_supervisor import UDT_DB_CONN_SUPERVISOR
from udt_user import UDT_USER
from udt_tracker_list import UDT_TRACKER_LIST
from udt_arterm_detailed_rep_supervisor import UDT_ARTERM_DETAILED_REP_SUPERVISOR

########################################################################################################################
# описание класса:
# - текущие данные
########################################################################################################################

class UDT_ARTERM_CURRENT_DATA():

    def __init__(self):

        self.date = None            #
        self.time = None            #
        self.day = None                # day_id
        self.day_big = None            # day_big_id
        self.year = None            # year_id
        self.month = None           # month_id
        self.weekday = None         #
        self.isWeekend = None       #
        self.weekendDay = None      # weekend_day_id
        self.isHoliday = None       #
        self.holiday = None         # holiday_id
        self.isDayout = None        #
        self.dayout = None          # dayout_id
        self.shift = None
        self.shift_w_day = None

        self.shiftPlan = None          # shift_plan_id
        self.shiftType = None          # shift_type_id
        self.isNight = False           #
        self.scheduledBreak = None     # scheduled_break_id
        self.isScheduledBreak = None   #
        self.isDinner = False          #

        self.shiftPlanCaption = None
        self.shiftCaption = None                # current shift
        self.scheduledBreakCaption = None       # current scheduled break


        self.shifts = UDT_ARR()             # shifts schedule for current day
        self.scheduledBreaks = UDT_ARR()    # scheduled brakes for current day

        self.curShiftBTime = None
        self.curShiftETime = None
        self.curScheduledBreakBTime = None
        self.curScheduledBreakETime = None

        self.isWorkingShift = None    # read from DB
        self.isWorkingTime = None     # = isWorkingShift and not isScheduledBreak

        self.MT_INFO = UDT_ARR()    # текущее состояние станков
        self.MT_STAT = UDT_ARR()

        self.LAMP_WORKSHOP_YELLOW = None
        self.LAMP_WORKSHOP_RED = None


########################################################################################################################
# описание класса:
# - набор данных "приложения"
# - эта структура является контейнером для вообще всех данных приложения
########################################################################################################################

class UDT_ARTERM_APP_DATA():

    def __init__(self):

        # all application objects references - for convinience
        # aux

        self.programVersion = "v1.0 Beta"
        self.programDescription = "ARTERM " + self.programVersion

        # main app

        self.application_TheApp = None
        self.window_MainWindow = None
        self.str_AppDir = ""
        self.str_ResDir = ""
        self.icon_MainWindowIcon = None

        # app settings

        self.settings = UDT_ARTERM_APP_SETTINGS()
        self.settingsFileName = ""
        self.settingsKeeper = None  # QSettings

        # threads

        self.thread_Dispatcher = None
        self.thread_DBAccess = None
        self.thread_MCycle = None

        # core thread functions (workers)

        self.worker_Dispatcher = None
        self.worker_DBAccess = None
        self.worker_MCycle = None

        # UI

        self.tpane_Basic = None
        self.tpane_FieldMonitor = None
        self.tpane_DayViewer = None
        self.tpane_DetailedRep = None
        self.tpane_Settings = None
        self.tpane_ARBMON = None

        # DB

        self.DB_CONN_SUPERVISOR = UDT_DB_CONN_SUPERVISOR()


        # DATA

        #PyQt5 models

        self.model_ComDataTable = UDT_TABLE_MODEL()

        # operational data

        self.USERS = UDT_ARR()                  # list<UDT_USER>
        self.MACHINE_TOOL_CLASSES = UDT_ARR()   #
        self.MACHINE_TOOLS = UDT_ARR()          #
        self.SHIFTS_PLANS = UDT_ARR()           #


        self.LOGGED_IN = False
        self.ACTIVE_USER = UDT_USER()
        self.CD = UDT_ARTERM_CURRENT_DATA()

        #self.CD.date = QDateTime.currentDateTime().date()
        #self.CD.time = QDateTime.currentDateTime().time()
        #self.CD.weekday = self.CD.date.dayOfWeek()
        #self.CD.isWeekend = None
        #self.CD.shift = 0

        # data for reflexing in DAY_VIEWER

        self.buffer_DAY = UDT_DAY_SCHEDULE_DATA()
        self.viewer_DAY = UDT_DAY_SCHEDULE_DATA()
        self.editor_DAY = UDT_DAY_SCHEDULE_DATA()
        self.updateDayViewer = False



        #

        self.LAMP_BLINKER = UDT_PULSEGEN()

        #

        self.model_DBAccessTrackerBack = UDT_TRACKER_LIST()
        self.model_DBAccessTrackerView = UDT_TRACKER_LIST(cap=1000)
        self.window_DBAccessTracker = None

        #

        self.DETAILED_REP_ARR = UDT_ARR()   # list of UDT_DETAILS_T1_V00_RECORD()

        self.DETAILED_REP_SUPERVISOR = UDT_ARTERM_DETAILED_REP_SUPERVISOR(self)

        self.model_DetailedRepTrackerBack = UDT_TRACKER_LIST()
        self.model_DetailedRepTrackerView = UDT_TRACKER_LIST(cap=200)

        #

        self.init()

    ########################################################################################################################

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
                # self.CD.MT_STAT.append(mts)
                row.append(mts)

            for j in range(5):
                mts = UDT_CL_STAT_INFO()
                mts.class_id = j + 1
                # self.CD.MT_STAT.append(mts)
                row.append(mts)

            self.CD.MT_STAT.append(row)

        #

        self.LAMP_BLINKER.ms_RTx_CALL = 200.0
        self.LAMP_BLINKER.ms_TIME_ON = 1000.0
        self.LAMP_BLINKER.ms_TIME_OFF = 1000.0

    ####################################################################################################################

    #def prefillComDataTable(self):
    #
    #    # <header>
    #
    #    self.model_ComDataTable.header.append("")
    #    self.model_ComDataTable.header.append("")
    #
    #    # <body>
    #    # current date
    #
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущая дата")
    #    rec.append(UDT_TABLE_CELL(0, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.DATE, self.CD.date)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(0, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current weekday
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущий день недели")
    #    rec.append(UDT_TABLE_CELL(1, 0, dat))
    #
    #    str = "" # GF.weekdayIdToString(self.CD.weekday)
    #
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, str)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(1, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # weekday features
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "День недели: свойство")
    #    rec.append(UDT_TABLE_CELL(2, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, GF.isWeekendToString(self.CD.isWeekend))
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(2, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current time
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущее время")
    #    rec.append(UDT_TABLE_CELL(3, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.time)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(3, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # shift format
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "План смен")
    #    rec.append(UDT_TABLE_CELL(4, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.shiftPlanCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(4, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current shift
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущая смена")
    #    rec.append(UDT_TABLE_CELL(5, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.shiftCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(5, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current shift - begin
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Начало смены")
    #    rec.append(UDT_TABLE_CELL(6, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.curShiftBTime)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(6, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current shift - end
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Конец смены")
    #    rec.append(UDT_TABLE_CELL(7, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.curShiftETime)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(7, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current scheduled brake
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущий плановый перерыв")
    #    rec.append(UDT_TABLE_CELL(8, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.scheduledBreakCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(8, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current scheduled break - begin
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Начало перерыва")
    #    rec.append(UDT_TABLE_CELL(9, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.curScheduledBreakBTime)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(9, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current scheduled break - end
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Конец перерыва")
    #    rec.append(UDT_TABLE_CELL(10, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.curScheduledBreakBTime)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(10, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # is dinner
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Обеденный перерыв")
    #    rec.append(UDT_TABLE_CELL(11, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.isDinnerCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(11, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    cc = self.model_ComDataTable.columnCount(0)
    #    rr = self.model_ComDataTable.rowCount(0)
    #
    #    dummy = 0

    ####################################################################################################################




