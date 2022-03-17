########################################################################################################################

from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal


########################################################################################################################

from udt_tracker_list import UDT_TRACKER_LIST

from udt_field_station import UDT_FIELD_STATION

from enums import *
from global_functions import *
from udt_table_model_classes import *

from udt_arr import UDT_ARR
from udt_mt_info import UDT_MT_INFO
from udt_statistics import UDT_WORKSHOP_STAT
from udt_argate_app_settings import UDT_ARGATE_APP_SETTINGS
from udt_report_generation_supervisor import UDT_REPORT_GENERATION_SUPERVISOR


from sql_requests import *



########################################################################################################################
# описание класса:
# - текущие данные
########################################################################################################################

class UDT_ARGATE_CURRENT_DATA():

    def __init__(self):

        self.date = QDate.currentDate()            #
        self.time = QTime.currentTime()            #
        self.day = None             # day_id
        self.day_big = None         # day_big_id
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
        self.shift_big = None       # shift_big_id
        self.shift_w_day = None

        self.sh_Z0_year = None      # начало текущей смены - год
        self.sh_Z0_month = None     # начало текущей смены - месяц
        self.sh_Z0_day = None       # начало текущей смены - день

        self.sh_Z1_year = None      # начало предыдущей смены - год
        self.sh_Z1_month = None     # начало предыдущей смены - месяц
        self.sh_Z1_day = None       # начало предыдущей смены - день

        #self.day_Z1 = None
        #self.day_big_Z1 = None
        self.shift_Z1 = None
        self.shift_big_Z1 = None
        self.shift_w_day_Z1 = None


        self.shiftPlan = None          # shift_plan_id
        self.shiftType = None          # shift_type_id
        self.isNight = False           #
        self.scheduledBreak = None     # scheduled_break_id
        self.isScheduledBreak = None   #
        self.isDinner = None           #

        self.shiftType_Z1 = None

        self.shiftPlanTag = None
        self.shiftPlanCaption = None
        self.shiftCaption = None            # current shift
        self.scheduledBreakCaption = None   # current scheduled break

        self.SHIFTS = UDT_ARR()             # shifts schedule for current day
        #self.scheduledBreaks = UDT_ARR()    # scheduled brakes for current day

        self.curShiftBTime = QTime()
        self.curShiftETime = QTime()
        self.curScheduledBreakBTime = QTime()
        self.curScheduledBreakETime = QTime()

        self.isWorkingDay = None      # calc in argate
        self.isWorkingShift = None    # calc in argate
        self.isWorkingTime = None     # calc in argate

        self.MT_INFO = UDT_ARR()    # текущее состояние станков


########################################################################################################################
# описание класса:
# - данные, выбранные из БД
########################################################################################################################

#class UDT_DB_DATA():
#
#    def __init__(self):
#
#        self.day_id = None             # as persists in DB
#        self.day_big_id = None         # as persists in DB
#        self.month_id = None
#        self.year_id = None
#        self.weekday = None         # as persists in DB
#        self.isWeekend = None       # as persists in DB
#        self.weekendDay = None      # as persists in DB
#        self.isHoliday = None       # as persists in DB
#        self.holiday = None         # as persists in DB
#        self.isDayout = None        # as persists in DB
#        self.dayout = None          # as persists in DB
#
#        self.shifts = UDT_ARR() # UDT_SHIFTS()
#        self.scheduledBreaks = UDT_ARR() # UDT_SCHEDULED_BREAKS()

########################################################################################################################
# описание класса:
# - для хранения строк-запросов
########################################################################################################################

#class SQL_STRINGS():

    #dbRead_MTClassesFullList = SQL_REQUESTS.sqlreq_DBRead_GetFullMTClassesList()    # только тогда нет смысла проверять на пустоту
#    dbRead_MachineToolsFullList = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList()
#    dbRead_TableReportType2 = ""


########################################################################################################################
# описание класса:
# - набор данных приложения
########################################################################################################################

#class UDT_ARGATE_APP_SETTINGS():
#
#    def __init__(self):
#
#        self.writeRtDataToDB                = 0
#        self.writeStatesHistoryToDB         = 0
#
#        self.reportStartDate                = QDate().currentDate()
#        self.dailyReportTime                = QTime(23, 59, 59)
#        self.monthReportTime                = QTime(23, 59, 59)
#        self.yearReportTime                 = QTime(23, 59, 59)
#
#        self.keepCopyOfReportFileOnServer   = 0
#        self.dirForReportFiles              = ""
#        self.destEmail                      = ""



########################################################################################################################
# описание класса:
# - набор данных "приложения"
# - эта структура является контейнером для вообще всех данных приложения
########################################################################################################################

class UDT_ARGATE_APP_DATA():

    def __init__(self):

        # all application objects references - for convinience
        # aux

        self.programVersion = "v1.0 Beta"
        self.programDescription = "ARGATE " + self.programVersion

        # main app

        self.application_TheApp = None
        self.window_MainWindow = None
        self.str_AppDir = ""
        self.str_ResDir = ""
        self.icon_MainWindowIcon = None

        # app settings

        self.settings = UDT_ARGATE_APP_SETTINGS()
        self.settingsFileName = ""
        self.settingsKeeper = None      # QSettings

        # threads

        self.thread_Dispatcher = None
        self.thread_CheckNetwork = None
        self.thread_FieldAccess = None
        self.thread_DBAccess = None
        self.thread_MCycle = None
        #self.thread_ExcelExporter = None
        #self.thread_MailSender = None

        # core thread functions (workers)

        self.worker_Dispatcher = None
        self.worker_CheckNetwork = None
        self.worker_FieldAccess = None
        self.worker_DBAccess = None
        self.worker_MCycle = None
        #self.worker_ExcelExporter = None
        #self.worker_MailSender = None

        # data

        self.model_OutputWindow = UDT_TRACKER_LIST(cap=100)

        self.model_AppTrackerBack = UDT_TRACKER_LIST()
        self.model_AppTrackerView = UDT_TRACKER_LIST(cap=200)

        self.model_FieldAccessTrackerBack = UDT_TRACKER_LIST()
        self.model_FieldAccessTrackerView = UDT_TRACKER_LIST(cap=200)

        self.model_DBAccessTrackerBack = UDT_TRACKER_LIST()
        self.model_DBAccessTrackerView = UDT_TRACKER_LIST(cap=200)

        self.model_RepGenTrackerBack = UDT_TRACKER_LIST()
        self.model_RepGenTrackerView = UDT_TRACKER_LIST(cap=200)

        self.model_ComDataTable = UDT_TABLE_MODEL()

        # UI

        self.widget_TabPaneMain = None
        self.widget_TabSettings = None
        self.widget_TabPaneTests = None
        self.widget_TabPaneAppTracker = None
        self.widget_TabPaneFieldAccessTracker = None
        self.widget_TabPaneDBAccessTracker = None
        self.widget_TabPaneReportsGenerationTracker = None

        # field stations

        # ??? заменить на UDT_ARR ???
        self.stations = list([])    # это основной массив, который содержит данные
                                    # по станциям, можно сказать, сырые данные из ПЛК
                                    # list<UDT_FIELD_STATION>

        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P6_TRUBEND))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_17))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_18))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_19))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_20))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_21))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_22))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_23))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_24))
        self.stations.append(UDT_FIELD_STATION(ENM_MACHINE_TOOLS.MT_25))

        # вероятно, это надо заполнять динамически, на основании информации, считанной из БД ?
        # это если мы хотим иметь возможность менять число станков
        # или же это не предусмотрено? - НЕ ПРЕДУСМОТРЕНО, ВСЕГО 23 СТАНКА

        self.numberOfStations = len(self.stations)

        # DB

        self.db = None
        self.dbConnected = False

        # data

        self.MACHINE_TOOL_CLASSES = UDT_ARR()   # перечень
        self.MACHINE_TOOLS = UDT_ARR()          # перечень
        self.SHIFT_TYPES = UDT_ARR()            # перечень



        #self.DBD = UDT_DB_DATA()

        self.CD = UDT_ARGATE_CURRENT_DATA()

        self.CD.date = QDateTime.currentDateTime().date()
        #self.CD.date = QDateTime(QDate(2021, 3, 25), QDateTime.currentDateTime().time()).date()     #__DEBUG__
        self.CD.time = QDateTime.currentDateTime().time()
        #self.CD.weekday = self.CD.date.dayOfWeek()
        #self.CD.weekday = None
        #self.CD.isWeekend = None
        #self.CD.shift = None

        # statistics

        self.statistics = UDT_WORKSHOP_STAT()

        # reports


        # big tables for report

        #self.tbl_stat_mt_report = UDT_TBL_STAT_MT_REPORT()


        self.T1_REPORT_ARR = UDT_ARR()  # list of UDT_T1_V00_REPORT_RECORD()
        self.T2_REPORT_ARR = UDT_ARR()  # list of UDT_T2_V00_REPORT_RECORD()

        #

        #self.eos_ReportT2Requested = False
        #self.eos_ReportT2Done = False
        #self.eod_ReportT2Requested = False
        #self.eod_ReportT2Done = False
        #self.eod_ReportT1Reauested = False
        #self.eod_ReportT1Done = False

        #self.eos_GEN_REP_SEQ_STATE = 0      # end-of-shift
        #self.eod_GEN_REP_SEQ_STATE = 0      # end-of-day

        self.REPORT_T1_SUPERVISOR = UDT_REPORT_GENERATION_SUPERVISOR(self, UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1)
        self.REPORT_T2_SUPERVISOR = UDT_REPORT_GENERATION_SUPERVISOR(self, UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T2)


        self.init()

    ####################################################################################################################

    def init(self):     # вот это странная штука
                    # почему другие массивы так же не инициализируем ???

        for i in range(25):
            mti = UDT_MT_INFO()
            mti.mt_id = i + 1
            self.CD.MT_INFO.append(mti)


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
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Текущая дата")
    #    rec.append(UDT_TABLE_CELL(0, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.DATE, self.CD.date)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(0, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current weekday
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Текущий день недели")
    #    rec.append(UDT_TABLE_CELL(1, 0, dat))
    #
    #    str = GF.weekdayIdToString(self.CD.weekday)
    #
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, str)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(1, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # weekday features
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"День недели: свойство")
    #    rec.append(UDT_TABLE_CELL(2, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, GF.isWeekendToString(self.CD.isWeekend))
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(2, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #
    #    # current time
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Текущее время")
    #    rec.append(UDT_TABLE_CELL(3, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.CD.time)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(3, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # shift format
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"План смен")
    #    rec.append(UDT_TABLE_CELL(4, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.shiftPlanCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(4, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #    # current shift
    #    rec = UDT_TABLE_RECORD()
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Текущая смена")
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
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Текущий плановый перерыв")
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
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING,"Обеденный перерыв")
    #    rec.append(UDT_TABLE_CELL(11, 0, dat))
    #    dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.CD.isDinnerCaption)
    #    dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
    #    rec.append(UDT_TABLE_CELL(11, 1, dat))
    #
    #    self.model_ComDataTable.body.append(rec)
    #
    #
    #
    #
    #
    #
    #
    #
    #    cc = self.model_ComDataTable.columnCount(0)
    #    rr = self.model_ComDataTable.rowCount(0)
    #
    #    dummy = 0

    ####################################################################################################################
