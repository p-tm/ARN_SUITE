########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import QSqlQuery

########################################################################################################################

from udt_argate_app_data import *
from udt_db_functions import DBTIME
from sql_requests import *

from udt_machine_tool_class import UDT_MACHINE_TOOL_CLASS
from udt_machine_tool import UDT_MACHINE_TOOL
from udt_shift_type import UDT_SHIFT_TYPE
from udt_shift import UDT_SHIFT
from udt_scheduled_break import UDT_SCHEDULED_BREAK
from udt_t2_v00_report_record import UDT_T2_V00_REPORT_RECORD
from udt_t1_v00_report_record import UDT_T1_V00_REPORT_RECORD


########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_ARGATE_DB_CONNECTOR(QObject):

    #signal_DBConnected = pyqtSignal(str)
    #signal_DBConnectionFailed = pyqtSignal(str)

    #signal_DBGetStartupData = pyqtSignal()
    #signal_ProcessDailyData = pyqtSignal()

    #signal_DBWriteSuccessful = pyqtSignal(str)
    #signal_DBWriteFailed = pyqtSignal(str)
    #signal_DBReadSuccessful = pyqtSignal(str)
    #signal_DBReadFailed = pyqtSignal(str)

    #signal_MakeReport_EODay = pyqtSignal()
    #signal_GenerateReportType1 = pyqtSignal(int)
    #signal_GenerateReportType2 = pyqtSignal(int)

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data

        super().__init__()

        self.ccc = 0
        self.ddd = 0

    ####################################################################################################################

    #def connectSignals(self):

        #self.signal_DBConnected.connect(self.appData.widget_TabPaneAppTracker.msgprc_OnDBConnected)
        #self.signal_DBConnected.connect(self.appData.widget_TabPaneDBAccessTracker.msgprc_OnDBConnected)
        #self.signal_DBConnected.connect(self.appData.window_MainWindow.msgprc_OnDBConnected)  # MainWindow создаётся позже

        #self.signal_DBConnectionFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBConnectionFailed)

        #self.signal_DBWriteSuccessful.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBWriteSuccessful)
        #self.signal_DBWriteFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBWriteFailed)
        #self.signal_DBReadSuccessful.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBReadSuccessful)
        #self.signal_DBReadFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBReadFailed)

        #self.signal_DBGetStartupData.connect(self.msgprc_OnDBRead_GetDailyData)
        #self.signal_ProcessDailyData.connect(self.appData.worker_MCycle.msgprc_OnProcessDailyData)

       # self.signal_MakeReport_EODay.connect(self.appData.worker_T1.msgprc_OnMakeReport_EODay)
        #self.signal_GenerateReportType2.connect(self.appData.worker_T1.msgprc_OnGenerateReportType2)
        #self.signal_GenerateReportType1.connect(self.appData.worker_ExcelExporter.msgprc_OnGenerateReportType1)
        #self.signal_GenerateReportType2.connect(self.appData.worker_ExcelExporter.msgprc_OnGenerateReportType2)

    ####################################################################################################################

    def TRACK(self,track_msg):

        self.appData.model_DBAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneDBAccessTracker.paused:
            self.appData.model_DBAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_ConnectToDb(self):

        #print("connect to DB")

        self.appData.db = QSqlDatabase().addDatabase("QPSQL")
        self.appData.db.setHostName("localhost")
        #self.appData.db.setHostName("172.31.100.183")
        self.appData.db.setDatabaseName("DB_10")
        self.appData.db.setUserName("pdbs_adm")
        self.appData.db.setPassword("esms_dbsu")

        #self.appData.query = QSqlQuery(self.appData.db)

        b_res = q_res = False

        b_res = self.appData.db.open()

        if b_res:

            #self.appData.dbConnected = True

            self.appData.window_MainWindow.signal_DBConnectionSuccess.emit()    # ->

            #track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - OK"
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - OK")

            #self.appData.model_DBAccessTrackerBack.append(track_msg)
            #if not self.appData.widget_TabPaneDBAccessTracker.paused:
            #    self.appData.model_DBAccessTrackerView.append(track_msg)
            #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

            #tr_msg = "связь с БД установлена @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBConnected.emit(tr_msg)
            #self.signal_DBGetStartupData.emit()

            q_res, day_id = self.ReadInitialData_req1()
            if q_res:
                q_res = self.ReadInitialData_req2(day_id)
                if q_res:
                    q_res = self.ReadInitialData_req3(day_id)

            self.appData.window_MainWindow.signal_InitialDataReadDone.emit(q_res)    # ->

        else:

            #self.appData.dbConnected = False

            err = self.appData.db.lastError()
            err_text1 = err.databaseText()
            err_text2 = err.driverText()

            self.appData.window_MainWindow.signal_DBConnectionFailure.emit()    # ->

            #track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - failed"
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - failed")

            #self.appData.model_DBAccessTrackerBack.append(track_msg)
            #if not self.appData.widget_TabPaneDBAccessTracker.paused:
            #    self.appData.model_DBAccessTrackerView.append(track_msg)
            #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker


            #tr_msg = "подключение к БД неудачно @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBConnectionFailed.emit(tr_msg)
            #tr_msg = err_text1
            #self.signal_DBConnectionFailed.emit(tr_msg)



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWrite_CyclicData(self):

        q_res = False

        q_res = self.WriteRTData_req1()
        if q_res:
            q_res = self.WriteRTData_req2()

        self.appData.window_MainWindow.signal_RTDataWriteDone.emit(q_res)

        dummy = 0

    #    query = QSqlQuery(self.appData.db)
    #
    #    q_res = False
    #
    #    if self.appData.settings.writeRtDataToDB == 1:
    #
    #        print("write RT data to DB")
    #
    #
    #
    #        #req1 = SQL_REQUESTS.sqlreq_DBWriteTblRtHours(self.appData)
    #        #req2 = "INSERT INTO tbl_rt_hours(pk_id,the_date,the_time,shift_plan_id,shift_plan_caption,shift_id,shift_caption,is_night,break_id,break_caption,is_dinner,notes) VALUES (1,'2019-04-08'::date,'14:00:00.020'::time,1,'8H',1,'1-я смена /8H',0,0,'--',0,'');"
    #        req3 = SQL_REQUESTS.sqlreq_DBWriteTblRtHours(self.appData)
    #        q_res = query.exec(req3)
    #
    #        err = self.appData.db.lastError()
    #        if err.isValid():
    #            err_text1 = err.databaseText()
    #            err_text2 = err.driverText()
    #
    #        #if q_res:
    #        #    tr_msg = "запись в tbl_rt_hours успешна @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
    #        #    self.signal_DBWriteSuccessful.emit(tr_msg)
    #        #else:
    #        #    tr_msg = "запись в tbl_rt_hours невозможна @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
    #        #    self.signal_DBWriteFailed.emit(tr_msg)
    #
    #        if q_res:
    #            self.appData.model_DBAccessTrackerBack.append(
    #                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <...> - OK")
    #        else:
    #            self.appData.model_DBAccessTrackerBack.append(
    #                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <...> - failed")
    #
    #        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker
    #
    #    else:
    #
    #        tr_msg = "запись в tbl_rt_hours заблокирована настройками"
    #        self.signal_DBWriteFailed.emit(tr_msg)



    #    if self.appData.settings.writeStatesHistoryToDB == 1:
    #
    #        print("write state_history to DB")
    #
    #        q_res = True
    #
    #        #for station in self.appData.stations:
    #
    #        #self.appData.query = QSqlQuery()
    #
    #        #q_res = q_res and query.exec(station.DAT.sqlstr_StatesHistory)
    #        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrStatesHist(self.appData)
    #        q_res = q_res and query.exec(req4)
    #
    #        #q_res = self.appData.query.exec("select * from vew_machine_tools")
    #        #query_size = self.appData.query.size()
    #        #q_res = self.appData.query.exec("CREATE TABLE tbl_a(pk_id integer, PRIMARY KEY(pk_id));")
    #        #q_res = self.appData.query.exec("INSERT INTO tbl_machine_tool_classes(pk_id, caption) VALUES (5, 'ert');")
    #        #q_res = self.appData.query.exec("INSERT INTO tbl_states_history(rec_time, fk_machine_tool_id, fk_state_type_id, state_value, fk_event_hrec_id, fk_shift_id, b_time, fk_b_shift_id,c_time_full,c_time_w_shift,c_time_w_day) VALUES (TIMESTAMP'2021-03-01 09:10:00.000',1,1,0,0,1,TIMESTAMP'2021-03-01 00:00:00.000',1,INTERVAL'00:00:00.000',INTERVAL'00:00:00.000',INTERVAL'00:00:00.000'),(TIMESTAMP'2021-03-01 09:10:00.000',1,1,0,0,1,TIMESTAMP'2021-03-01 00:00:00.000',1,INTERVAL'00:00:00.000',INTERVAL'00:00:00.000',INTERVAL'00:00:00.000');")
    #
    #        #print(station.DAT.sqlstr_StatesHistory)
    #
    #        if q_res:
    #            tr_msg = "запись в tbl_states_history успешна @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
    #            self.signal_DBWriteSuccessful.emit(tr_msg)
    #        else:
    #            tr_msg = "запись в tbl_states_history невозможна @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
    #            self.signal_DBWriteFailed.emit(tr_msg)
    #
    #    else:
    #
    #        tr_msg = "запись в tbl_states_history заблокирована настройками"
    #        self.signal_DBWriteFailed.emit(tr_msg)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBRead_GetDailyData__(self):

        date = self.appData.CD.date
        next_query = True
        query_no = 1

        query = QSqlQuery(self.appData.db)

        # to get "DailyData" we must make 3 sequential requests
        # I assume that QSqlQuery::exec() can be considered as synchronous
        # in terms of one thread
        # so assume, that I can just issue 3 sequential requests

        # REQ 1

        query_no = 1

        #self.appData.sqlRequest = "SELECT * FROM tbl_calender WHERE tbl_calender.the_date='" + date.toString("yyyy-MM-dd") + "'::date"
        req1 = SQL_REQUESTS.sqlreq_DBRead_CurrentDay(date)
        q_res = query.exec(req1)

        day_id = 0

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        day_id = query.value("pk_day_id")
                        self.appData.CD.day = query.value("pk_day_id")
                        self.appData.CD.day_big = query.value("day_big_id")
                        self.appData.CD.month = query.value("month_id")
                        self.appData.CD.year = query.value("year_id")
                        self.appData.CD.weekday = query.value("weekday")
                        self.appData.CD.isWeekend = query.value("is_weekend")
                        self.appData.CD.weekendDay = query.value("fk_wendday_id")
                        self.appData.CD.isHoliday = query.value("is_holiday")
                        self.appData.CD.holiday = query.value("fk_holiday_id")
                        self.appData.CD.isDayout = query.value("is_dayout")
                        self.appData.CD.dayout = query.value("fk_dayout_id")
                        self.appData.CD.shiftPlan = query.value("fk_shift_plan_id")
                        self.appData.CD.shiftPlanTag = query.value("plan_tag")
                        self.appData.CD.shiftPlanCaption = query.value("plan_caption")

                        b_res = query.next()

                query.finish()

        if q_res:
            tr_msg = "чтение из tbl_calender успешно @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadSuccessful.emit(tr_msg)
            #self.signal_ProcessDailyData.emit()
            next_query = True
        else:
            tr_msg = "чтение из tbl_calender невозможно @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadFailed.emit(tr_msg)
            next_query = False

        # REQ 2

        query_no = 2

        #self.appData.sqlRequest = "SELECT * FROM tbl_shifts LEFT JOIN tbl_shift_names ON tbl_shifts.pk_id = tbl_shift_names.fk_shift_id WHERE tbl_shifts.day_id=" + str(day_id)
        req2 = SQL_REQUESTS.sqlreq_DBRead_ActiveShiftsForDay(day_id)
        q_res = query.exec(req2)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        #if self.appData.query.value("active"):

                        shift = UDT_SHIFT()
                        #shift.active = True # this list only contains active shifts
                        shift.shift_id = query.value("shift_id")
                        shift.shift_big_id = query.value("shift_big_id")
                        shift.shift_type_id = query.value("fk_shift_type_id")
                        shift.shift_number_w_day = query.value("shift_number_w_day")
                        shift.shiftCaption = query.value("shift_caption")
                        #shift.plan = query.value("fk_shift_plan_id")
                        #shift.planCaption = query.value("shift_plan_caption")
                        shift.b_time = query.value("b_time")
                        shift.e_time = query.value("e_time")
                        shift.isNight = query.value("is_night")

                        self.appData.CD.SHIFTS.append(shift)

                        b_res = query.next()

                query.finish()

        if q_res:
            tr_msg = "чтение из tbl_shifts успешно @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadSuccessful.emit(tr_msg)
            #self.signal_ProcessDailyData.emit()
            next_query = True
        else:
            tr_msg = "чтение из tbl_shifts невозможно @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadFailed.emit(tr_msg)
            next_query = False

        # REQ 3

        query_no = 3

        req3 = SQL_REQUESTS.sqlreq_DBRead_ActiveBreaksForDay(day_id)
        q_res = query.exec(req3)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        br = UDT_SCHEDULED_BREAK()

                        br.id = query.value("fk_scheduled_break_type_id")
                        br.b_time = query.value("b_time")
                        br.e_time = query.value("e_time")
                        br.isDinner = query.value("is_dinner")
                        br.breakCaption = query.value("caption")

                        break_parent_shift = query.value("shift_big_id")

                        for sh in self.appData.CD.SHIFTS:
                            if sh.shift_big_id == break_parent_shift:
                                sh.SCHEDULED_BREAKS.append(br)
                                break

                        #self.appData.CD.scheduledBreaks.append(br)

                        b_res = query.next()

                query.finish()

        if q_res:
            tr_msg = "чтение из tbl_scheduled_breaks успешно @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadSuccessful.emit(tr_msg)
            #self.signal_ProcessDailyData.emit()     # worker_T1.msgprc_OnProcessDailyData
            next_query = True
        else:
            tr_msg = "чтение из tbl_scheduled_breaks невозможно @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBReadFailed.emit(tr_msg)
            next_query = False





    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBRead_GetDailyData(self):

        q_res, day_id = self.ReadInitialData_req1()
        if q_res:
            q_res = self.ReadInitialData_req2(day_id)
            if q_res:
                q_res = self.ReadInitialData_req3(day_id)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWrite_EODayData(self):

        # запись очередной записи в общую таблицу

        query = QSqlQuery(self.appData.db)

        q_res = True

        for station in self.appData.stations:
            q_res = q_res and query.exec(station.DAT.sqlstr_StatByMT)

        dummy = 0

        if q_res:
            tr_msg = "запись в tbl_stat_by_mt успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBWriteSuccessful.emit(tr_msg)
        else:
            tr_msg = "чтение из tbl_scheduled_breaks невозможно @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            self.signal_DBWriteFailed.emit(tr_msg)

        # потом сюда добавить - чтобы сразу запускать процесс получения таблицы для отчёта

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBRead_TblReportT1(self):

        query = QSqlQuery(self.appData.db)

        q_res = False
        req1 = SQL_REQUESTS.sqlreq_DBRead_GetFullMTClassesList2()
        q_res = query.exec(req1)

        if q_res:
            tr_msg = "выборка перечня классов станков успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка перечня классов станков невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.MACHINE_TOOL_CLASSES.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_MACHINE_TOOL_CLASS()

                        rec.id = query.value("pk_mt_class_id")
                        rec.caption = query.value("caption")

                        self.appData.MACHINE_TOOL_CLASSES.append(rec)

                        b_res = query.next()

                query.finish()

        # следующий

        q_res = False
        req2 = SQL_REQUESTS.sqlreq_DBRead_GetFullShiftTypesList()
        q_res = query.exec(req2)

        if q_res:
            tr_msg = "выборка перечня типов смен успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка перечня типов смен невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.SHIFT_TYPES.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_SHIFT_TYPE()

                        rec.id = query.value("pk_shift_type_id")
                        rec.caption = query.value("caption")

                        self.appData.SHIFT_TYPES.append(rec)

                        b_res = query.next()

                query.finish()

        # следующий

        q_res = False
        req3 = SQL_REQUESTS.sqlreq_DBRead_TblReportT1(self.appData)
        q_res = query.exec(req3)

        if q_res:
            tr_msg = "выборка полной таблицы успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка полной таблицы невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка - принимаем такую концепцию, что рашифровка производится в этом же потоке

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.T1_REPORT_ARR.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_T1_V00_REPORT_RECORD()

                        rec.rec_id              = query.value("rec_id")
                        rec.day_id              = query.value("day_id")
                        rec.month_id            = query.value("month_id")
                        rec.month_w_year        = query.value("month_w_year")
                        rec.year_id             = query.value("year_id")
                        rec.the_date            = query.value("the_date")
                        rec.is_dayout           = query.value("is_dayout")
                        rec.rec_type            = query.value("rec_type")

                        if rec.day_id == 324:
                            dummm = 0

                        rec.s1_b_time           = query.value("s1_b_time")
                        rec.s1_e_time           = query.value("s1_e_time")
                        rec.s2_b_time           = query.value("s2_b_time")
                        rec.s2_e_time           = query.value("s2_e_time")
                        rec.s3_b_time           = query.value("s3_b_time")
                        rec.s3_e_time           = query.value("s3_e_time")
                        rec.s4_b_time           = query.value("s4_b_time")
                        rec.s4_e_time           = query.value("s4_e_time")
                        rec.s5_b_time           = query.value("s5_b_time")
                        rec.s5_e_time           = query.value("s5_e_time")

                        rec.s1_data_exists      = query.value("s1_data_exists")
                        rec.s2_data_exists      = query.value("s2_data_exists")
                        rec.s3_data_exists      = query.value("s3_data_exists")
                        rec.s4_data_exists      = query.value("s4_data_exists")
                        rec.s5_data_exists      = query.value("s5_data_exists")

                        #

                        rec.cl1_s1_stp_failure  = query.value("cl1_s1_stp_failure")
                        rec.cl1_s1_stp_material = query.value("cl1_s1_stp_material")
                        rec.cl1_s1_stp_process  = query.value("cl1_s1_stp_process")
                        rec.cl1_s1_stp_quality  = query.value("cl1_s1_stp_quality")
                        rec.cl1_s1_stp_offline  = query.value("cl1_s1_stp_offline")
                        rec.cl1_s1_alr_failure  = query.value("cl1_s1_alr_failure")
                        rec.cl1_s1_alr_material = query.value("cl1_s1_alr_material")
                        rec.cl1_s1_stp_sum      = query.value("cl1_s1_stp_sum")
                        rec.cl1_s1_alr_sum      = query.value("cl1_s1_alr_sum")

                        rec.cl1_s2_stp_failure  = query.value("cl1_s2_stp_failure")
                        rec.cl1_s2_stp_material = query.value("cl1_s2_stp_material")
                        rec.cl1_s2_stp_process  = query.value("cl1_s2_stp_process")
                        rec.cl1_s2_stp_quality  = query.value("cl1_s2_stp_quality")
                        rec.cl1_s2_stp_offline  = query.value("cl1_s2_stp_offline")
                        rec.cl1_s2_alr_failure  = query.value("cl1_s2_alr_failure")
                        rec.cl1_s2_alr_material = query.value("cl1_s2_alr_material")
                        rec.cl1_s2_stp_sum      = query.value("cl1_s2_stp_sum")
                        rec.cl1_s2_alr_sum      = query.value("cl1_s2_alr_sum")

                        rec.cl1_s3_stp_failure  = query.value("cl1_s3_stp_failure")
                        rec.cl1_s3_stp_material = query.value("cl1_s3_stp_material")
                        rec.cl1_s3_stp_process  = query.value("cl1_s3_stp_process")
                        rec.cl1_s3_stp_quality  = query.value("cl1_s3_stp_quality")
                        rec.cl1_s3_stp_offline  = query.value("cl1_s3_stp_offline")
                        rec.cl1_s3_alr_failure  = query.value("cl1_s3_alr_failure")
                        rec.cl1_s3_alr_material = query.value("cl1_s3_alr_material")
                        rec.cl1_s3_stp_sum      = query.value("cl1_s3_stp_sum")
                        rec.cl1_s3_alr_sum      = query.value("cl1_s3_alr_sum")

                        rec.cl1_s4_stp_failure  = query.value("cl1_s4_stp_failure")
                        rec.cl1_s4_stp_material = query.value("cl1_s4_stp_material")
                        rec.cl1_s4_stp_process  = query.value("cl1_s4_stp_process")
                        rec.cl1_s4_stp_quality  = query.value("cl1_s4_stp_quality")
                        rec.cl1_s4_stp_offline  = query.value("cl1_s4_stp_offline")
                        rec.cl1_s4_alr_failure  = query.value("cl1_s4_alr_failure")
                        rec.cl1_s4_alr_material = query.value("cl1_s4_alr_material")
                        rec.cl1_s4_stp_sum      = query.value("cl1_s4_stp_sum")
                        rec.cl1_s4_alr_sum      = query.value("cl1_s4_alr_sum")

                        rec.cl1_s5_stp_failure  = query.value("cl1_s5_stp_failure")
                        rec.cl1_s5_stp_material = query.value("cl1_s5_stp_material")
                        rec.cl1_s5_stp_process  = query.value("cl1_s5_stp_process")
                        rec.cl1_s5_stp_quality  = query.value("cl1_s5_stp_quality")
                        rec.cl1_s5_stp_offline  = query.value("cl1_s5_stp_offline")
                        rec.cl1_s5_alr_failure  = query.value("cl1_s5_alr_failure")
                        rec.cl1_s5_alr_material = query.value("cl1_s5_alr_material")
                        rec.cl1_s5_stp_sum      = query.value("cl1_s5_stp_sum")
                        rec.cl1_s5_alr_sum      = query.value("cl1_s5_alr_sum")

                        #rec.cl1_s6_stp_failure  = query.value("cl1_s6_stp_failure")
                        #rec.cl1_s6_stp_material = query.value("cl1_s6_stp_material")
                        #rec.cl1_s6_stp_process  = query.value("cl1_s6_stp_process")
                        #rec.cl1_s6_stp_quality  = query.value("cl1_s6_stp_quality")
                        #rec.cl1_s6_stp_offline  = query.value("cl1_s6_stp_offline")
                        #rec.cl1_s6_alr_failure  = query.value("cl1_s6_alr_failure")
                        #rec.cl1_s6_alr_material = query.value("cl1_s6_alr_material")
                        #rec.cl1_s6_stp_sum      = query.value("cl1_s6_stp_sum")
                        #rec.cl1_s6_alr_sum      = query.value("cl1_s6_alr_sum")
                        #
                        #rec.cl1_s7_stp_failure  = query.value("cl1_s7_stp_failure")
                        #rec.cl1_s7_stp_material = query.value("cl1_s7_stp_material")
                        #rec.cl1_s7_stp_process  = query.value("cl1_s7_stp_process")
                        #rec.cl1_s7_stp_quality  = query.value("cl1_s7_stp_quality")
                        #rec.cl1_s7_stp_offline  = query.value("cl1_s7_stp_offline")
                        #rec.cl1_s7_alr_failure  = query.value("cl1_s7_alr_failure")
                        #rec.cl1_s7_alr_material = query.value("cl1_s7_alr_material")
                        #rec.cl1_s7_stp_sum      = query.value("cl1_s7_stp_sum")
                        #rec.cl1_s7_alr_sum      = query.value("cl1_s7_alr_sum")

                        #

                        rec.cl2_s1_stp_failure  = query.value("cl2_s1_stp_failure")
                        rec.cl2_s1_stp_material = query.value("cl2_s1_stp_material")
                        rec.cl2_s1_stp_process  = query.value("cl2_s1_stp_process")
                        rec.cl2_s1_stp_quality  = query.value("cl2_s1_stp_quality")
                        rec.cl2_s1_stp_offline  = query.value("cl2_s1_stp_offline")
                        rec.cl2_s1_alr_failure  = query.value("cl2_s1_alr_failure")
                        rec.cl2_s1_alr_material = query.value("cl2_s1_alr_material")
                        rec.cl2_s1_stp_sum      = query.value("cl2_s1_stp_sum")
                        rec.cl2_s1_alr_sum      = query.value("cl2_s1_alr_sum")

                        rec.cl2_s2_stp_failure  = query.value("cl2_s2_stp_failure")
                        rec.cl2_s2_stp_material = query.value("cl2_s2_stp_material")
                        rec.cl2_s2_stp_process  = query.value("cl2_s2_stp_process")
                        rec.cl2_s2_stp_quality  = query.value("cl2_s2_stp_quality")
                        rec.cl2_s2_stp_offline  = query.value("cl2_s2_stp_offline")
                        rec.cl2_s2_alr_failure  = query.value("cl2_s2_alr_failure")
                        rec.cl2_s2_alr_material = query.value("cl2_s2_alr_material")
                        rec.cl2_s2_stp_sum      = query.value("cl2_s2_stp_sum")
                        rec.cl2_s2_alr_sum      = query.value("cl2_s2_alr_sum")

                        rec.cl2_s3_stp_failure  = query.value("cl2_s3_stp_failure")
                        rec.cl2_s3_stp_material = query.value("cl2_s3_stp_material")
                        rec.cl2_s3_stp_process  = query.value("cl2_s3_stp_process")
                        rec.cl2_s3_stp_quality  = query.value("cl2_s3_stp_quality")
                        rec.cl2_s3_stp_offline  = query.value("cl2_s3_stp_offline")
                        rec.cl2_s3_alr_failure  = query.value("cl2_s3_alr_failure")
                        rec.cl2_s3_alr_material = query.value("cl2_s3_alr_material")
                        rec.cl2_s3_stp_sum      = query.value("cl2_s3_stp_sum")
                        rec.cl2_s3_alr_sum      = query.value("cl2_s3_alr_sum")

                        rec.cl2_s4_stp_failure  = query.value("cl2_s4_stp_failure")
                        rec.cl2_s4_stp_material = query.value("cl2_s4_stp_material")
                        rec.cl2_s4_stp_process  = query.value("cl2_s4_stp_process")
                        rec.cl2_s4_stp_quality  = query.value("cl2_s4_stp_quality")
                        rec.cl2_s4_stp_offline  = query.value("cl2_s4_stp_offline")
                        rec.cl2_s4_alr_failure  = query.value("cl2_s4_alr_failure")
                        rec.cl2_s4_alr_material = query.value("cl2_s4_alr_material")
                        rec.cl2_s4_stp_sum      = query.value("cl2_s4_stp_sum")
                        rec.cl2_s4_alr_sum      = query.value("cl2_s4_alr_sum")

                        rec.cl2_s5_stp_failure  = query.value("cl2_s5_stp_failure")
                        rec.cl2_s5_stp_material = query.value("cl2_s5_stp_material")
                        rec.cl2_s5_stp_process  = query.value("cl2_s5_stp_process")
                        rec.cl2_s5_stp_quality  = query.value("cl2_s5_stp_quality")
                        rec.cl2_s5_stp_offline  = query.value("cl2_s5_stp_offline")
                        rec.cl2_s5_alr_failure  = query.value("cl2_s5_alr_failure")
                        rec.cl2_s5_alr_material = query.value("cl2_s5_alr_material")
                        rec.cl2_s5_stp_sum      = query.value("cl2_s5_stp_sum")
                        rec.cl2_s5_alr_sum      = query.value("cl2_s5_alr_sum")

                        #rec.cl2_s6_stp_failure  = query.value("cl2_s6_stp_failure")
                        #rec.cl2_s6_stp_material = query.value("cl2_s6_stp_material")
                        #rec.cl2_s6_stp_process  = query.value("cl2_s6_stp_process")
                        #rec.cl2_s6_stp_quality  = query.value("cl2_s6_stp_quality")
                        #rec.cl2_s6_stp_offline  = query.value("cl2_s6_stp_offline")
                        #rec.cl2_s6_alr_failure  = query.value("cl2_s6_alr_failure")
                        #rec.cl2_s6_alr_material = query.value("cl2_s6_alr_material")
                        #rec.cl2_s6_stp_sum      = query.value("cl2_s6_stp_sum")
                        #rec.cl2_s6_alr_sum      = query.value("cl2_s6_alr_sum")
                        #
                        #rec.cl2_s7_stp_failure  = query.value("cl2_s7_stp_failure")
                        #rec.cl2_s7_stp_material = query.value("cl2_s7_stp_material")
                        #rec.cl2_s7_stp_process  = query.value("cl2_s7_stp_process")
                        #rec.cl2_s7_stp_quality  = query.value("cl2_s7_stp_quality")
                        #rec.cl2_s7_stp_offline  = query.value("cl2_s7_stp_offline")
                        #rec.cl2_s7_alr_failure  = query.value("cl2_s7_alr_failure")
                        #rec.cl2_s7_alr_material = query.value("cl2_s7_alr_material")
                        #rec.cl2_s7_stp_sum      = query.value("cl2_s7_stp_sum")
                        #rec.cl2_s7_alr_sum      = query.value("cl2_s7_alr_sum")

                        #

                        rec.cl3_s1_stp_failure  = query.value("cl3_s1_stp_failure")
                        rec.cl3_s1_stp_material = query.value("cl3_s1_stp_material")
                        rec.cl3_s1_stp_process  = query.value("cl3_s1_stp_process")
                        rec.cl3_s1_stp_quality  = query.value("cl3_s1_stp_quality")
                        rec.cl3_s1_stp_offline  = query.value("cl3_s1_stp_offline")
                        rec.cl3_s1_alr_failure  = query.value("cl3_s1_alr_failure")
                        rec.cl3_s1_alr_material = query.value("cl3_s1_alr_material")
                        rec.cl3_s1_stp_sum      = query.value("cl3_s1_stp_sum")
                        rec.cl3_s1_alr_sum      = query.value("cl3_s1_alr_sum")

                        rec.cl3_s2_stp_failure  = query.value("cl3_s2_stp_failure")
                        rec.cl3_s2_stp_material = query.value("cl3_s2_stp_material")
                        rec.cl3_s2_stp_process  = query.value("cl3_s2_stp_process")
                        rec.cl3_s2_stp_quality  = query.value("cl3_s2_stp_quality")
                        rec.cl3_s2_stp_offline  = query.value("cl3_s2_stp_offline")
                        rec.cl3_s2_alr_failure  = query.value("cl3_s2_alr_failure")
                        rec.cl3_s2_alr_material = query.value("cl3_s2_alr_material")
                        rec.cl3_s2_stp_sum      = query.value("cl3_s2_stp_sum")
                        rec.cl3_s2_alr_sum      = query.value("cl3_s2_alr_sum")

                        rec.cl3_s3_stp_failure  = query.value("cl3_s3_stp_failure")
                        rec.cl3_s3_stp_material = query.value("cl3_s3_stp_material")
                        rec.cl3_s3_stp_process  = query.value("cl3_s3_stp_process")
                        rec.cl3_s3_stp_quality  = query.value("cl3_s3_stp_quality")
                        rec.cl3_s3_stp_offline  = query.value("cl3_s3_stp_offline")
                        rec.cl3_s3_alr_failure  = query.value("cl3_s3_alr_failure")
                        rec.cl3_s3_alr_material = query.value("cl3_s3_alr_material")
                        rec.cl3_s3_stp_sum      = query.value("cl3_s3_stp_sum")
                        rec.cl3_s3_alr_sum      = query.value("cl3_s3_alr_sum")

                        rec.cl3_s4_stp_failure  = query.value("cl3_s4_stp_failure")
                        rec.cl3_s4_stp_material = query.value("cl3_s4_stp_material")
                        rec.cl3_s4_stp_process  = query.value("cl3_s4_stp_process")
                        rec.cl3_s4_stp_quality  = query.value("cl3_s4_stp_quality")
                        rec.cl3_s4_stp_offline  = query.value("cl3_s4_stp_offline")
                        rec.cl3_s4_alr_failure  = query.value("cl3_s4_alr_failure")
                        rec.cl3_s4_alr_material = query.value("cl3_s4_alr_material")
                        rec.cl3_s4_stp_sum      = query.value("cl3_s4_stp_sum")
                        rec.cl3_s4_alr_sum      = query.value("cl3_s4_alr_sum")

                        rec.cl3_s5_stp_failure  = query.value("cl3_s5_stp_failure")
                        rec.cl3_s5_stp_material = query.value("cl3_s5_stp_material")
                        rec.cl3_s5_stp_process  = query.value("cl3_s5_stp_process")
                        rec.cl3_s5_stp_quality  = query.value("cl3_s5_stp_quality")
                        rec.cl3_s5_stp_offline  = query.value("cl3_s5_stp_offline")
                        rec.cl3_s5_alr_failure  = query.value("cl3_s5_alr_failure")
                        rec.cl3_s5_alr_material = query.value("cl3_s5_alr_material")
                        rec.cl3_s5_stp_sum      = query.value("cl3_s5_stp_sum")
                        rec.cl3_s5_alr_sum      = query.value("cl3_s5_alr_sum")

                        #rec.cl3_s6_stp_failure  = query.value("cl3_s6_stp_failure")
                        #rec.cl3_s6_stp_material = query.value("cl3_s6_stp_material")
                        #rec.cl3_s6_stp_process  = query.value("cl3_s6_stp_process")
                        #rec.cl3_s6_stp_quality  = query.value("cl3_s6_stp_quality")
                        #rec.cl3_s6_stp_offline  = query.value("cl3_s6_stp_offline")
                        #rec.cl3_s6_alr_failure  = query.value("cl3_s6_alr_failure")
                        #rec.cl3_s6_alr_material = query.value("cl3_s6_alr_material")
                        #rec.cl3_s6_stp_sum      = query.value("cl3_s6_stp_sum")
                        #rec.cl3_s6_alr_sum      = query.value("cl3_s6_alr_sum")
                        #
                        #rec.cl3_s7_stp_failure  = query.value("cl3_s7_stp_failure")
                        #rec.cl3_s7_stp_material = query.value("cl3_s7_stp_material")
                        #rec.cl3_s7_stp_process  = query.value("cl3_s7_stp_process")
                        #rec.cl3_s7_stp_quality  = query.value("cl3_s7_stp_quality")
                        #rec.cl3_s7_stp_offline  = query.value("cl3_s7_stp_offline")
                        #rec.cl3_s7_alr_failure  = query.value("cl3_s7_alr_failure")
                        #rec.cl3_s7_alr_material = query.value("cl3_s7_alr_material")
                        #rec.cl3_s7_stp_sum      = query.value("cl3_s7_stp_sum")
                        #rec.cl3_s7_alr_sum      = query.value("cl3_s7_alr_sum")

                        #

                        rec.cl4_s1_stp_failure = query.value("cl4_s1_stp_failure")
                        rec.cl4_s1_stp_material = query.value("cl4_s1_stp_material")
                        rec.cl4_s1_stp_process = query.value("cl4_s1_stp_process")
                        rec.cl4_s1_stp_quality = query.value("cl4_s1_stp_quality")
                        rec.cl4_s1_stp_offline = query.value("cl4_s1_stp_offline")
                        rec.cl4_s1_alr_failure = query.value("cl4_s1_alr_failure")
                        rec.cl4_s1_alr_material = query.value("cl4_s1_alr_material")
                        rec.cl4_s1_stp_sum = query.value("cl4_s1_stp_sum")
                        rec.cl4_s1_alr_sum = query.value("cl4_s1_alr_sum")

                        rec.cl4_s2_stp_failure = query.value("cl4_s2_stp_failure")
                        rec.cl4_s2_stp_material = query.value("cl4_s2_stp_material")
                        rec.cl4_s2_stp_process = query.value("cl4_s2_stp_process")
                        rec.cl4_s2_stp_quality = query.value("cl4_s2_stp_quality")
                        rec.cl4_s2_stp_offline = query.value("cl4_s2_stp_offline")
                        rec.cl4_s2_alr_failure = query.value("cl4_s2_alr_failure")
                        rec.cl4_s2_alr_material = query.value("cl4_s2_alr_material")
                        rec.cl4_s2_stp_sum = query.value("cl4_s2_stp_sum")
                        rec.cl4_s2_alr_sum = query.value("cl4_s2_alr_sum")

                        rec.cl4_s3_stp_failure = query.value("cl4_s3_stp_failure")
                        rec.cl4_s3_stp_material = query.value("cl4_s3_stp_material")
                        rec.cl4_s3_stp_process = query.value("cl4_s3_stp_process")
                        rec.cl4_s3_stp_quality = query.value("cl4_s3_stp_quality")
                        rec.cl4_s3_stp_offline = query.value("cl4_s3_stp_offline")
                        rec.cl4_s3_alr_failure = query.value("cl4_s3_alr_failure")
                        rec.cl4_s3_alr_material = query.value("cl4_s3_alr_material")
                        rec.cl4_s3_stp_sum = query.value("cl4_s3_stp_sum")
                        rec.cl4_s3_alr_sum = query.value("cl4_s3_alr_sum")

                        rec.cl4_s4_stp_failure = query.value("cl4_s4_stp_failure")
                        rec.cl4_s4_stp_material = query.value("cl4_s4_stp_material")
                        rec.cl4_s4_stp_process = query.value("cl4_s4_stp_process")
                        rec.cl4_s4_stp_quality = query.value("cl4_s4_stp_quality")
                        rec.cl4_s4_stp_offline = query.value("cl4_s4_stp_offline")
                        rec.cl4_s4_alr_failure = query.value("cl4_s4_alr_failure")
                        rec.cl4_s4_alr_material = query.value("cl4_s4_alr_material")
                        rec.cl4_s4_stp_sum = query.value("cl4_s4_stp_sum")
                        rec.cl4_s4_alr_sum = query.value("cl4_s4_alr_sum")

                        rec.cl4_s5_stp_failure = query.value("cl4_s5_stp_failure")
                        rec.cl4_s5_stp_material = query.value("cl4_s5_stp_material")
                        rec.cl4_s5_stp_process = query.value("cl4_s5_stp_process")
                        rec.cl4_s5_stp_quality = query.value("cl4_s5_stp_quality")
                        rec.cl4_s5_stp_offline = query.value("cl4_s5_stp_offline")
                        rec.cl4_s5_alr_failure = query.value("cl4_s5_alr_failure")
                        rec.cl4_s5_alr_material = query.value("cl4_s5_alr_material")
                        rec.cl4_s5_stp_sum = query.value("cl4_s5_stp_sum")
                        rec.cl4_s5_alr_sum = query.value("cl4_s5_alr_sum")

                        #rec.cl4_s6_stp_failure = query.value("cl4_s6_stp_failure")
                        #rec.cl4_s6_stp_material = query.value("cl4_s6_stp_material")
                        #rec.cl4_s6_stp_process = query.value("cl4_s6_stp_process")
                        #rec.cl4_s6_stp_quality = query.value("cl4_s6_stp_quality")
                        #rec.cl4_s6_stp_offline = query.value("cl4_s6_stp_offline")
                        #rec.cl4_s6_alr_failure = query.value("cl4_s6_alr_failure")
                        #rec.cl4_s6_alr_material = query.value("cl4_s6_alr_material")
                        #rec.cl4_s6_stp_sum = query.value("cl4_s6_stp_sum")
                        #rec.cl4_s6_alr_sum = query.value("cl4_s6_alr_sum")
                        #
                        #rec.cl4_s7_stp_failure = query.value("cl4_s7_stp_failure")
                        #rec.cl4_s7_stp_material = query.value("cl4_s7_stp_material")
                        #rec.cl4_s7_stp_process = query.value("cl4_s7_stp_process")
                        #rec.cl4_s7_stp_quality = query.value("cl4_s7_stp_quality")
                        #rec.cl4_s7_stp_offline = query.value("cl4_s7_stp_offline")
                        #rec.cl4_s7_alr_failure = query.value("cl4_s7_alr_failure")
                        #rec.cl4_s7_alr_material = query.value("cl4_s7_alr_material")
                        #rec.cl4_s7_stp_sum = query.value("cl4_s7_stp_sum")
                        #rec.cl4_s7_alr_sum = query.value("cl4_s7_alr_sum")







                        rec.is_valid            = query.value("is_valid")


                        self.appData.T1_REPORT_ARR.append(rec)

                        b_res = query.next()

                query.finish()

        #self.signal_GenerateReportType1.emit(send_email)  # -> UDT_EXCEL_EXPORTER.msgprc_OnGenerateReportType1
        self.appData.window_MainWindow.signal_DBRead_TblReportT1_Done.emit(q_res)    # -> SUPERVISOR.msgprc_OnTableReceived


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBRead_TblReportT2(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        #req1 = self.appData.sql_strings.dbRead_MTClassesFullList
        req1 = SQL_REQUESTS.sqlreq_DBRead_GetFullMTClassesList2()
        q_res = query.exec(req1)

        if q_res:
            tr_msg = "выборка перечня классов станков успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка перечня классов станков невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.MACHINE_TOOL_CLASSES.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_MACHINE_TOOL_CLASS()

                        rec.id = query.value("pk_mt_class_id")
                        rec.caption = query.value("caption")

                        self.appData.MACHINE_TOOL_CLASSES.append(rec)

                        b_res = query.next()

                query.finish()

        # следующий

        #req2 = self.appData.sql_strings.dbRead_MachineToolsFullList
        #q_res = query.exec(self.appData.sql_strings.dbRead_MachineToolsFullList)
        req2 = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList2()
        q_res = query.exec(req2)

        if q_res:
            tr_msg = "выборка перечня станков успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка перечня станков невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.MACHINE_TOOLS.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_MACHINE_TOOL()

                        rec.id = query.value("mt_id")
                        rec.uniqnum = query.value("uniqnum")
                        rec.tag = query.value("tag")
                        rec.caption = query.value("mt_caption")
                        rec.short_cap = ""
                        rec.mt_class = query.value("mt_class_caption")

                        self.appData.MACHINE_TOOLS.append(rec)

                        b_res = query.next()

                query.finish()

        # следующий

        #eq3 = self.appData.sql_strings.dbRead_TableReportType2
        #q_res = query.exec(self.appData.sql_strings.dbRead_TableReportType2)
        req3 = SQL_REQUESTS.sqlreq_DBRead_TblReportT2(self.appData)
        q_res = query.exec(req3)

        dummy = 0

        if q_res:
            tr_msg = "выборка полной таблицы успешна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadSuccessful.emit(tr_msg)
        else:
            tr_msg = "выборка полной таблицы невозможна @" + QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz")
            #self.signal_DBReadFailed.emit(tr_msg)

        # расшифровка - принимаем такую концепцию, что рашифровка производится в этом же потоке

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.T2_REPORT_ARR.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_T2_V00_REPORT_RECORD()

                        rec.rec_id = query.value("rec_id")
                        rec.day_id = query.value("day_id")
                        rec.month_id = query.value("month_id")
                        rec.month_w_year = query.value("month_w_year")
                        rec.year_id = query.value("year_id")
                        rec.the_date = query.value("the_date")
                        rec.is_dayout = query.value("is_dayout")
                        rec.rec_type = query.value("rec_type")
                        rec.day_cl1_mt1_stp_time = query.value("day_cl1_mt1_stp_time")
                        rec.day_cl1_mt2_stp_time = query.value("day_cl1_mt2_stp_time")
                        rec.day_cl1_mt3_stp_time = query.value("day_cl1_mt3_stp_time")
                        rec.day_cl1_mt4_stp_time = query.value("day_cl1_mt4_stp_time")
                        rec.day_cl1_mt5_stp_time = query.value("day_cl1_mt5_stp_time")
                        rec.day_cl1_stp_sum = query.value("day_cl1_stp_sum")
                        rec.day_cl1_stp_sum_prc = query.value("day_cl1_stp_sum_prc")
                        rec.day_cl1_reference_time = query.value("day_cl1_reference_time")

                        rec.day_cl2_mt6_stp_time = query.value("day_cl2_mt6_stp_time")
                        rec.day_cl2_mt7_stp_time = query.value("day_cl2_mt7_stp_time")
                        rec.day_cl2_mt8_stp_time = query.value("day_cl2_mt8_stp_time")
                        rec.day_cl2_mt9_stp_time = query.value("day_cl2_mt9_stp_time")
                        rec.day_cl2_mt10_stp_time = query.value("day_cl2_mt10_stp_time")
                        rec.day_cl2_mt11_stp_time = query.value("day_cl2_mt11_stp_time")
                        rec.day_cl2_mt12_stp_time = query.value("day_cl2_mt12_stp_time")
                        rec.day_cl2_mt13_stp_time = query.value("day_cl2_mt13_stp_time")
                        rec.day_cl2_mt14_stp_time = query.value("day_cl2_mt14_stp_time")
                        rec.day_cl2_stp_sum = query.value("day_cl2_stp_sum")
                        rec.day_cl2_stp_sum_prc = query.value("day_cl2_stp_sum_prc")
                        rec.day_cl2_reference_time = query.value("day_cl2_reference_time")

                        rec.day_cl3_mt15_stp_time = query.value("day_cl3_mt15_stp_time")
                        rec.day_cl3_stp_sum = query.value("day_cl3_stp_sum")
                        rec.day_cl3_stp_sum_prc = query.value("day_cl3_stp_sum_prc")
                        rec.day_cl3_reference_time = query.value("day_cl3_reference_time")

                        rec.day_cl4_mt16_stp_time = query.value("day_cl4_mt16_stp_time")
                        rec.day_cl4_stp_sum = query.value("day_cl4_stp_sum")
                        rec.day_cl4_stp_sum_prc = query.value("day_cl4_stp_sum_prc")
                        rec.day_cl4_reference_time = query.value("day_cl4_reference_time")

                        rec.day_mt1_stp_failure = query.value("day_mt1_stp_failure")
                        rec.day_mt1_stp_material = query.value("day_mt1_stp_material")
                        rec.day_mt1_stp_process = query.value("day_mt1_stp_process")
                        rec.day_mt1_stp_quality = query.value("day_mt1_stp_quality")
                        rec.day_mt1_stp_offline = query.value("day_mt1_stp_offline")
                        rec.day_mt1_alr_failure = query.value("day_mt1_alr_failure")
                        rec.day_mt1_alr_material = query.value("day_mt1_alr_material")
                        rec.day_mt1_stp_sum = query.value("day_mt1_stp_sum")
                        rec.day_mt1_alr_sum = query.value("day_mt1_alr_sum")

                        rec.day_mt2_stp_failure = query.value("day_mt2_stp_failure")
                        rec.day_mt2_stp_material = query.value("day_mt2_stp_material")
                        rec.day_mt2_stp_process = query.value("day_mt2_stp_process")
                        rec.day_mt2_stp_quality = query.value("day_mt2_stp_quality")
                        rec.day_mt2_stp_offline = query.value("day_mt2_stp_offline")
                        rec.day_mt2_alr_failure = query.value("day_mt2_alr_failure")
                        rec.day_mt2_alr_material = query.value("day_mt2_alr_material")
                        rec.day_mt2_stp_sum = query.value("day_mt2_stp_sum")
                        rec.day_mt2_alr_sum = query.value("day_mt2_alr_sum")

                        rec.day_mt3_stp_failure = query.value("day_mt3_stp_failure")
                        rec.day_mt3_stp_material = query.value("day_mt3_stp_material")
                        rec.day_mt3_stp_process = query.value("day_mt3_stp_process")
                        rec.day_mt3_stp_quality = query.value("day_mt3_stp_quality")
                        rec.day_mt3_stp_offline = query.value("day_mt3_stp_offline")
                        rec.day_mt3_alr_failure = query.value("day_mt3_alr_failure")
                        rec.day_mt3_alr_material = query.value("day_mt3_alr_material")
                        rec.day_mt3_stp_sum = query.value("day_mt3_stp_sum")
                        rec.day_mt3_alr_sum = query.value("day_mt3_alr_sum")
                        
                        rec.day_mt4_stp_failure = query.value("day_mt4_stp_failure")
                        rec.day_mt4_stp_material = query.value("day_mt4_stp_material")
                        rec.day_mt4_stp_process = query.value("day_mt4_stp_process")
                        rec.day_mt4_stp_quality = query.value("day_mt4_stp_quality")
                        rec.day_mt4_stp_offline = query.value("day_mt4_stp_offline")
                        rec.day_mt4_alr_failure = query.value("day_mt4_alr_failure")
                        rec.day_mt4_alr_material = query.value("day_mt4_alr_material")
                        rec.day_mt4_stp_sum = query.value("day_mt4_stp_sum")
                        rec.day_mt4_alr_sum = query.value("day_mt4_alr_sum")
                        
                        rec.day_mt5_stp_failure = query.value("day_mt5_stp_failure")
                        rec.day_mt5_stp_material = query.value("day_mt5_stp_material")
                        rec.day_mt5_stp_process = query.value("day_mt5_stp_process")
                        rec.day_mt5_stp_quality = query.value("day_mt5_stp_quality")
                        rec.day_mt5_stp_offline = query.value("day_mt5_stp_offline")
                        rec.day_mt5_alr_failure = query.value("day_mt5_alr_failure")
                        rec.day_mt5_alr_material = query.value("day_mt5_alr_material")
                        rec.day_mt5_stp_sum = query.value("day_mt5_stp_sum")
                        rec.day_mt5_alr_sum = query.value("day_mt5_alr_sum")
                        
                        rec.day_mt6_stp_failure = query.value("day_mt6_stp_failure")
                        rec.day_mt6_stp_material = query.value("day_mt6_stp_material")
                        rec.day_mt6_stp_process = query.value("day_mt6_stp_process")
                        rec.day_mt6_stp_quality = query.value("day_mt6_stp_quality")
                        rec.day_mt6_stp_offline = query.value("day_mt6_stp_offline")
                        rec.day_mt6_alr_failure = query.value("day_mt6_alr_failure")
                        rec.day_mt6_alr_material = query.value("day_mt6_alr_material")
                        rec.day_mt6_stp_sum = query.value("day_mt6_stp_sum")
                        rec.day_mt6_alr_sum = query.value("day_mt6_alr_sum")
                        
                        rec.day_mt7_stp_failure = query.value("day_mt7_stp_failure")
                        rec.day_mt7_stp_material = query.value("day_mt7_stp_material")
                        rec.day_mt7_stp_process = query.value("day_mt7_stp_process")
                        rec.day_mt7_stp_quality = query.value("day_mt7_stp_quality")
                        rec.day_mt7_stp_offline = query.value("day_mt7_stp_offline")
                        rec.day_mt7_alr_failure = query.value("day_mt7_alr_failure")
                        rec.day_mt7_alr_material = query.value("day_mt7_alr_material")
                        rec.day_mt7_stp_sum = query.value("day_mt7_stp_sum")
                        rec.day_mt7_alr_sum = query.value("day_mt7_alr_sum")
                        
                        rec.day_mt8_stp_failure = query.value("day_mt8_stp_failure")
                        rec.day_mt8_stp_material = query.value("day_mt8_stp_material")
                        rec.day_mt8_stp_process = query.value("day_mt8_stp_process")
                        rec.day_mt8_stp_quality = query.value("day_mt8_stp_quality")
                        rec.day_mt8_stp_offline = query.value("day_mt8_stp_offline")
                        rec.day_mt8_alr_failure = query.value("day_mt8_alr_failure")
                        rec.day_mt8_alr_material = query.value("day_mt8_alr_material")
                        rec.day_mt8_stp_sum = query.value("day_mt8_stp_sum")
                        rec.day_mt8_alr_sum = query.value("day_mt8_alr_sum")
                        
                        rec.day_mt9_stp_failure = query.value("day_mt9_stp_failure")
                        rec.day_mt9_stp_material = query.value("day_mt9_stp_material")
                        rec.day_mt9_stp_process = query.value("day_mt9_stp_process")
                        rec.day_mt9_stp_quality = query.value("day_mt9_stp_quality")
                        rec.day_mt9_stp_offline = query.value("day_mt9_stp_offline")
                        rec.day_mt9_alr_failure = query.value("day_mt9_alr_failure")
                        rec.day_mt9_alr_material = query.value("day_mt9_alr_material")
                        rec.day_mt9_stp_sum = query.value("day_mt9_stp_sum")
                        rec.day_mt9_alr_sum = query.value("day_mt9_alr_sum")
                        
                        rec.day_mt10_stp_failure = query.value("day_mt10_stp_failure")
                        rec.day_mt10_stp_material = query.value("day_mt10_stp_material")
                        rec.day_mt10_stp_process = query.value("day_mt10_stp_process")
                        rec.day_mt10_stp_quality = query.value("day_mt10_stp_quality")
                        rec.day_mt10_stp_offline = query.value("day_mt10_stp_offline")
                        rec.day_mt10_alr_failure = query.value("day_mt10_alr_failure")
                        rec.day_mt10_alr_material = query.value("day_mt10_alr_material")
                        rec.day_mt10_stp_sum = query.value("day_mt10_stp_sum")
                        rec.day_mt10_alr_sum = query.value("day_mt10_alr_sum")
                        
                        rec.day_mt11_stp_failure = query.value("day_mt11_stp_failure")
                        rec.day_mt11_stp_material = query.value("day_mt11_stp_material")
                        rec.day_mt11_stp_process = query.value("day_mt11_stp_process")
                        rec.day_mt11_stp_quality = query.value("day_mt11_stp_quality")
                        rec.day_mt11_stp_offline = query.value("day_mt11_stp_offline")
                        rec.day_mt11_alr_failure = query.value("day_mt11_alr_failure")
                        rec.day_mt11_alr_material = query.value("day_mt11_alr_material")
                        rec.day_mt11_stp_sum = query.value("day_mt11_stp_sum")
                        rec.day_mt11_alr_sum = query.value("day_mt11_alr_sum")
                        
                        rec.day_mt12_stp_failure = query.value("day_mt12_stp_failure")
                        rec.day_mt12_stp_material = query.value("day_mt12_stp_material")
                        rec.day_mt12_stp_process = query.value("day_mt12_stp_process")
                        rec.day_mt12_stp_quality = query.value("day_mt12_stp_quality")
                        rec.day_mt12_stp_offline = query.value("day_mt12_stp_offline")
                        rec.day_mt12_alr_failure = query.value("day_mt12_alr_failure")
                        rec.day_mt12_alr_material = query.value("day_mt12_alr_material")
                        rec.day_mt12_stp_sum = query.value("day_mt12_stp_sum")
                        rec.day_mt12_alr_sum = query.value("day_mt12_alr_sum")
                        
                        rec.day_mt13_stp_failure = query.value("day_mt13_stp_failure")
                        rec.day_mt13_stp_material = query.value("day_mt13_stp_material")
                        rec.day_mt13_stp_process = query.value("day_mt13_stp_process")
                        rec.day_mt13_stp_quality = query.value("day_mt13_stp_quality")
                        rec.day_mt13_stp_offline = query.value("day_mt13_stp_offline")
                        rec.day_mt13_alr_failure = query.value("day_mt13_alr_failure")
                        rec.day_mt13_alr_material = query.value("day_mt13_alr_material")
                        rec.day_mt13_stp_sum = query.value("day_mt13_stp_sum")
                        rec.day_mt13_alr_sum = query.value("day_mt13_alr_sum")
                        
                        rec.day_mt14_stp_failure = query.value("day_mt14_stp_failure")
                        rec.day_mt14_stp_material = query.value("day_mt14_stp_material")
                        rec.day_mt14_stp_process = query.value("day_mt14_stp_process")
                        rec.day_mt14_stp_quality = query.value("day_mt14_stp_quality")
                        rec.day_mt14_stp_offline = query.value("day_mt14_stp_offline")
                        rec.day_mt14_alr_failure = query.value("day_mt14_alr_failure")
                        rec.day_mt14_alr_material = query.value("day_mt14_alr_material")
                        rec.day_mt14_stp_sum = query.value("day_mt14_stp_sum")
                        rec.day_mt14_alr_sum = query.value("day_mt14_alr_sum")
                        
                        rec.day_mt15_stp_failure = query.value("day_mt15_stp_failure")
                        rec.day_mt15_stp_material = query.value("day_mt15_stp_material")
                        rec.day_mt15_stp_process = query.value("day_mt15_stp_process")
                        rec.day_mt15_stp_quality = query.value("day_mt15_stp_quality")
                        rec.day_mt15_stp_offline = query.value("day_mt15_stp_offline")
                        rec.day_mt15_alr_failure = query.value("day_mt15_alr_failure")
                        rec.day_mt15_alr_material = query.value("day_mt15_alr_material")
                        rec.day_mt15_stp_sum = query.value("day_mt15_stp_sum")
                        rec.day_mt15_alr_sum = query.value("day_mt15_alr_sum")
                        
                        rec.day_mt16_stp_failure = query.value("day_mt16_stp_failure")
                        rec.day_mt16_stp_material = query.value("day_mt16_stp_material")
                        rec.day_mt16_stp_process = query.value("day_mt16_stp_process")
                        rec.day_mt16_stp_quality = query.value("day_mt16_stp_quality")
                        rec.day_mt16_stp_offline = query.value("day_mt16_stp_offline")
                        rec.day_mt16_alr_failure = query.value("day_mt16_alr_failure")
                        rec.day_mt16_alr_material = query.value("day_mt16_alr_material")
                        rec.day_mt16_stp_sum = query.value("day_mt16_stp_sum")
                        rec.day_mt16_alr_sum = query.value("day_mt16_alr_sum")

                        rec.is_valid = query.value("is_valid")

                        self.appData.T2_REPORT_ARR.append(rec)

                        b_res = query.next()

                query.finish()

        #self.signal_GenerateReportType2.emit()  # -> UDT_WORKER_T1.msgprc_OnGenerateReportType2
        #self.signal_GenerateReportType2.emit(send_email)  # -> UDT_EXCEL_EXPORTER.msgprc_OnGenerateReportType2
        self.appData.window_MainWindow.signal_DBRead_TblReportT2_Done.emit(q_res)  # -> SUPERVISOR.msgprc_OnTableReceived

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWriteWrStatesHist(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrStatesHist(self.appData)
        q_res = query.exec(SQL_REQUESTS.sqlreq_DBWrite_WrStatesHist(self.appData))

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <tbl_states_history> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <tbl_states_history> - failed")

        query.finish()



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWriteWrShiftStat(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrShiftStat(self.appData)
        q_res = query.exec(req4)

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <shift_stat> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <shift_stat> - failed")

        #if self.appData.eos_GEN_REP_SEQ_STATE == 2: # WAITS
        #    self.appData.worker_MCycle.signal_DBRead_TblReportT2.emit(1)
        #    self.appData.eos_GEN_REP_SEQ_STATE = 3  # WAIT for REPORT_TYPE_2 is generated and sent

        query.finish()


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWriteWrDailyStat(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrDailyStat(self.appData)
        q_res = query.exec(req4)

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <daily_stat> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <daily_stat> - failed")

        #if self.appData.eod_GEN_REP_SEQ_STATE == 2: # WAITS
        #    self.appData.worker_MCycle.signal_DBRead_TblReportT1.emit(1)
        #    self.appData.eod_GEN_REP_SEQ_STATE = 3  # WAIT for REPORT_TYPE_1 is generated and sent

        query.finish()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWriteWrMonthStat(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrMonthStat(self.appData)
        q_res = query.exec(SQL_REQUESTS.sqlreq_DBWrite_WrMonthStat(self.appData))

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <monthly_stat> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <monthly_stat> - failed")

        query.finish()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBWriteWrYearStat(self):

        query = QSqlQuery(self.appData.db)

        q_res =  False

        req4 = SQL_REQUESTS.sqlreq_DBWrite_WrYearStat(self.appData)
        q_res = query.exec(SQL_REQUESTS.sqlreq_DBWrite_WrYearStat(self.appData))

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <yearly_stat> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write() <yearly_stat> - failed")

        query.finish()

    ####################################################################################################################

    def ReadInitialData_req1(self):

        date = self.appData.CD.date

        query = QSqlQuery(self.appData.db)

        req1 = SQL_REQUESTS.sqlreq_DBRead_CurrentDay(date)
        q_res = query.exec(req1)

        day_id = 0 # следующий запрос на основании day_id

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        day_id = query.value("pk_day_id")
                        self.appData.CD.day = query.value("pk_day_id")
                        self.appData.CD.day_big = query.value("day_big_id")
                        self.appData.CD.month = query.value("month_id")
                        self.appData.CD.year = query.value("year_id")
                        self.appData.CD.weekday = query.value("weekday")
                        self.appData.CD.isWeekend = query.value("is_weekend")
                        self.appData.CD.weekendDay = query.value("fk_wendday_id")
                        self.appData.CD.isHoliday = query.value("is_holiday")
                        self.appData.CD.holiday = query.value("fk_holiday_id")
                        self.appData.CD.isDayout = query.value("is_dayout")
                        self.appData.CD.dayout = query.value("fk_dayout_id")
                        self.appData.CD.shiftPlan = query.value("fk_shift_plan_id")
                        self.appData.CD.shiftPlanTag = query.value("plan_tag")
                        self.appData.CD.shiftPlanCaption = query.value("plan_caption")

                        b_res = query.next()

                query.finish()

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <machine_tools> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString(
                "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <machine_tools> - failed")

        return q_res, day_id

    ####################################################################################################################

    def ReadInitialData_req2(self, day_id):

        query = QSqlQuery(self.appData.db)

        req2 = SQL_REQUESTS.sqlreq_DBRead_ActiveShiftsForDay(day_id)
        q_res = query.exec(req2)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        #if self.appData.query.value("active"):

                        shift = UDT_SHIFT()
                        #shift.active = True # this list only contains active shifts
                        shift.shift_id = query.value("shift_id")
                        shift.shift_big_id = query.value("shift_big_id")
                        shift.shift_type_id = query.value("fk_shift_type_id")
                        shift.shift_number_w_day = query.value("shift_number_w_day")
                        shift.shiftCaption = query.value("shift_caption")
                        #shift.plan = query.value("fk_shift_plan_id")
                        #shift.planCaption = query.value("shift_plan_caption")
                        shift.b_time = query.value("b_time")
                        shift.e_time = query.value("e_time")
                        shift.isNight = query.value("is_night")

                        self.appData.CD.SHIFTS.append(shift)

                        b_res = query.next()

                query.finish()

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString(
                    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <shifts> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString(
                    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <shifts> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadInitialData_req3(self, day_id):

        query = QSqlQuery(self.appData.db)

        req3 = SQL_REQUESTS.sqlreq_DBRead_ActiveBreaksForDay(day_id)
        q_res = query.exec(req3)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        br = UDT_SCHEDULED_BREAK()

                        br.id = query.value("fk_scheduled_break_type_id")
                        br.b_time = query.value("b_time")
                        br.e_time = query.value("e_time")
                        br.isDinner = query.value("is_dinner")
                        br.breakCaption = query.value("caption")

                        break_parent_shift = query.value("shift_big_id")

                        for sh in self.appData.CD.SHIFTS:
                            if sh.shift_big_id == break_parent_shift:
                                sh.SCHEDULED_BREAKS.append(br)
                                break

                        #self.appData.CD.scheduledBreaks.append(br)

                        b_res = query.next()

                query.finish()

        if q_res:
            self.TRACK(QDateTime.currentDateTime().toString(
                    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <breaks> - OK")
        else:
            self.TRACK(QDateTime.currentDateTime().toString(
                    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <breaks> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def WriteRTData_req1(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        if self.appData.settings.writeRtDataToDB == 1:

            #print("write RT data to DB")

            req1 = SQL_REQUESTS.sqlreq_DBWriteTblRtHours(self.appData)
            q_res = query.exec(req1)

            err = self.appData.db.lastError()
            if err.isValid():
                err_text1 = err.databaseText()
                err_text2 = err.driverText()

            self.ccc += 1

            if q_res:
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <tbl_rt_hours> - OK")
            else:
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <tbl_rt_hours> - failed")

        else:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "запись в tbl_rt_hours заблокирована настройками")

        return q_res

    ####################################################################################################################

    def WriteRTData_req2(self):

        query = QSqlQuery(self.appData.db)

        q_res = False


        if self.appData.settings.writeStatesHistoryToDB == 1:

            #print("write state_history to DB")

            #for station in self.appData.stations:

            #self.appData.query = QSqlQuery()

            #q_res = q_res and query.exec(station.DAT.sqlstr_StatesHistory)
            req2 = SQL_REQUESTS.sqlreq_DBWrite_WrStatesHist(self.appData)
            q_res = query.exec(req2)

            self.ddd += 1

            #q_res = self.appData.query.exec("select * from vew_machine_tools")
            #query_size = self.appData.query.size()
            #q_res = self.appData.query.exec("CREATE TABLE tbl_a(pk_id integer, PRIMARY KEY(pk_id));")
            #q_res = self.appData.query.exec("INSERT INTO tbl_machine_tool_classes(pk_id, caption) VALUES (5, 'ert');")
            #q_res = self.appData.query.exec("INSERT INTO tbl_states_history(rec_time, fk_machine_tool_id, fk_state_type_id, state_value, fk_event_hrec_id, fk_shift_id, b_time, fk_b_shift_id,c_time_full,c_time_w_shift,c_time_w_day) VALUES (TIMESTAMP'2021-03-01 09:10:00.000',1,1,0,0,1,TIMESTAMP'2021-03-01 00:00:00.000',1,INTERVAL'00:00:00.000',INTERVAL'00:00:00.000',INTERVAL'00:00:00.000'),(TIMESTAMP'2021-03-01 09:10:00.000',1,1,0,0,1,TIMESTAMP'2021-03-01 00:00:00.000',1,INTERVAL'00:00:00.000',INTERVAL'00:00:00.000',INTERVAL'00:00:00.000');")

            #print(station.DAT.sqlstr_StatesHistory)

            if q_res:
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <tbl_states_history> - OK")
            else:
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_rt_data() <tbl_states_history> - failed")

        else:
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "запись в tbl_rt_hours заблокирована настройками")


        return q_res

    ####################################################################################################################









