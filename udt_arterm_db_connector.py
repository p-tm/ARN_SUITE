########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtSql import QSqlQuery

from copy import copy

########################################################################################################################

from udt_user import UDT_USER
from udt_machine_tool import UDT_MACHINE_TOOL
from udt_mt_info import UDT_MT_INFO
from udt_mt_stat_info import UDT_MT_STAT_INFO
from udt_cl_stat_info import UDT_CL_STAT_INFO
from udt_shift import UDT_SHIFT
from udt_scheduled_break import UDT_SCHEDULED_BREAK
from udt_shifts_plan import UDT_SHIFTS_PLAN
from udt_details_t1_v00_record import UDT_DETAILS_T1_V00_RECORD

from sql_requests import *

from udt_interval import UDT_INTERVAL

########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_ARTERM_DB_CONNECTOR(QObject):

    #signal_DBReadSuccess = pyqtSignal() # убираем
    #signal_DBReadFailure = pyqtSignal() # убираем

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data

        super().__init__()

    ####################################################################################################################

    #def connectSignals(self): # убираем
    #
    #   self.signal_DBReadSuccess.connect(self.appData.worker_MCycle.msgprc_OnDbConnOK)

    ####################################################################################################################

    def decoder1(self, src_string, mt_inf):

        res_str = src_string.lstrip("(")
        res_str = res_str.rstrip(")")
        res_tpl = res_str.split(",")

        # mt_id is already filled-up at init()

        mt_inf.offline = res_tpl[0] == "t"
        mt_inf.alr_failure = res_tpl[1] == "t"
        mt_inf.alr_material = res_tpl[2] == "t"
        mt_inf.stp_failure = res_tpl[3] == "t"
        mt_inf.stp_material = res_tpl[4] == "t"
        mt_inf.stp_process = res_tpl[5] == "t"
        mt_inf.stp_quality = res_tpl[6] == "t"
        mt_inf.aux_1 = res_tpl[7] == "t"
        mt_inf.aux_2 = res_tpl[8] == "t"

    ####################################################################################################################

    def decoder2(self, src_string, mt_st):

        fix = lambda x: 0 if x == "" else int(x)

        xTime = UDT_INTERVAL.s_fromHMS(23, 59, 59)

        res_str = src_string.lstrip("(")
        res_str = res_str.rstrip(")")
        res_tpl = res_str.split(",")

        # mt_id and class_id is already filled-up at init()

        if res_tpl[0] == "" or res_tpl[0].find("days") != -1 or res_tpl[0].find("day") != -1:
            mt_st.offline = xTime
        else:
            hms_tpl = res_tpl[0].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.offline.fromHMS(hh,mm,ss)

        if res_tpl[1] == "" or res_tpl[1].find("days") != -1 or res_tpl[1].find("day") != -1:
            mt_st.alr_failure = xTime
        else:
            hms_tpl = res_tpl[1].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.alr_failure.fromHMS(hh,mm,ss)

        if res_tpl[2] == "" or res_tpl[2].find("days") != -1 or res_tpl[2].find("day") != -1:
            mt_st.alr_material = xTime
        else:
            hms_tpl = res_tpl[2].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.alr_material.fromHMS(hh,mm,ss)

        if res_tpl[3] == "" or res_tpl[3].find("days") != -1 or res_tpl[3].find("day") != -1:
            mt_st.stp_failure = xTime
        else:
            hms_tpl = res_tpl[3].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.stp_failure.fromHMS(hh,mm,ss)

        if res_tpl[4] == "" or res_tpl[4].find("days") != -1 or res_tpl[4].find("day") != -1:
            mt_st.stp_material = xTime
        else:
            hms_tpl = res_tpl[4].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.stp_material.fromHMS(hh,mm,ss)

        if res_tpl[5] == "" or res_tpl[5].find("days") != -1 or res_tpl[5].find("day") != -1:
            mt_st.stp_process = xTime
        else:
            hms_tpl = res_tpl[5].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.stp_process.fromHMS(hh,mm,ss)

        if res_tpl[6] == "" or res_tpl[6].find("days") != -1 or res_tpl[6].find("day") != -1:
            mt_st.stp_quality = xTime
        else:
            hms_tpl = res_tpl[6].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.stp_quality.fromHMS(hh,mm,ss)

        if res_tpl[7] == "" or res_tpl[7].find("days") != -1 or res_tpl[7].find("day") != -1:
            mt_st.aux_1 = xTime
        else:
            hms_tpl = res_tpl[7].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.aux_1.fromHMS(hh,mm,ss)

        if res_tpl[8] == "" or res_tpl[8].find("days") != -1 or res_tpl[8].find("day") != -1:
            mt_st.aux_2 = xTime
        else:
            hms_tpl = res_tpl[8].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.aux_2.fromHMS(hh,mm,ss)

        if res_tpl[9] == "" or res_tpl[9].find("days") != -1 or res_tpl[9].find("day") != -1:
            mt_st.alr_sum = xTime
        else:
            hms_tpl = res_tpl[9].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.alr_sum.fromHMS(hh,mm,ss)

        if res_tpl[10] == "" or res_tpl[10].find("days") != -1 or res_tpl[10].find("day") != -1:
            mt_st.stp_sum = xTime
        else:
            hms_tpl = res_tpl[10].split(":")
            hh = fix(hms_tpl[0])
            mm = fix(hms_tpl[1])
            ss = fix(hms_tpl[2][0:2])
            mt_st.stp_sum.fromHMS(hh,mm,ss)


    ####################################################################################################################

    def TRACK(self, track_msg):

        self.appData.model_DBAccessTrackerBack.append(track_msg)
        if self.appData.window_DBAccessTracker is None:
            self.appData.model_DBAccessTrackerView.append(track_msg)
        else:
            if not self.appData.window_DBAccessTracker.paused:
                self.appData.model_DBAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_ConnectToDb(self):

        print("connect to DB")

        self.appData.db = QSqlDatabase().addDatabase("QPSQL")
        self.appData.db.setHostName("172.31.100.183")
        #self.appData.db.setHostName("localhost")
        self.appData.db.setDatabaseName("DB_10")
        self.appData.db.setUserName("pdbs_adm")
        self.appData.db.setPassword("esms_dbsu")

        #self.appData.query = QSqlQuery(self.appData.db)

        b_res = q_res = False

        b_res = self.appData.db.open()

        if b_res:

            self.appData.window_MainWindow.signal_DBConnectionSuccess.emit()    # -> worker_MCycle::
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - OK")


            q_res = self.ReadInitialData_req1()
            if q_res:
                q_res = self.ReadInitialData_req2()
                if q_res:
                    q_res = self.ReadInitialData_req3()
                    if q_res:
                        q_res = self.ReadInitialData_req4()

            self.appData.window_MainWindow.signal_InitialDataReadDone.emit(q_res)    # -> worker_MCycle::

        else:

            err = self.appData.db.lastError()
            err_text1 = err.databaseText()
            err_text2 = err.driverText()

            self.appData.window_MainWindow.signal_DBConnectionFailure.emit()    # -> worker_MCycle::
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - failed")


        # тут же заправшиваем данные по станкам

        #query = QSqlQuery(self.appData.db)

        #q_res = False
        #
        #req1 = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList2()
        #q_res = query.exec(req1)
        #
        #if q_res:
        #
        #    if query.isActive():
        #
        #        record_number = query.size()
        #        if not (record_number == -1 or record_number == 0):
        #
        #            b_res = query.first()
        #            i = 0
        #            while query.isValid():
        #
        #                rec = UDT_MACHINE_TOOL()
        #
        #                rec.id = query.value("mt_id")
        #                rec.uniqnum = query.value("uniqnum")
        #                rec.tag = query.value("tag")
        #                rec.caption = query.value("mt_caption")
        #                rec.short_cap = ""
        #                rec.mt_class = query.value("mt_class_caption")
        #                rec.persists = query.value("persists")
        #
        #                self.appData.MACHINE_TOOLS.append(rec)
        #
        #                b_res = query.next()
        #
        #        query.finish()

        # ещё по планам смен

        #req2 = SQL_REQUESTS.sqlreq_DBRead_GetFullShiftPlansList()
        #q_res = query.exec(req2)
        #
        #if q_res:
        #
        #    if query.isActive():
        #
        #        record_number = query.size()
        #        if not (record_number == -1 or record_number == 0):
        #
        #            b_res = query.first()
        #            while query.isValid():
        #
        #                rec = UDT_SHIFTS_PLAN()
        #
        #                rec.plan_id = query.value("pk_shift_plan_id")
        #                rec.plan_tag = query.value("tag")
        #                rec.plan_caption = query.value("caption")
        #
        #                self.appData.SHIFTS_PLANS.append(rec)
        #
        #                b_res = query.next()
        #
        #        query.finish()

        #req3 = SQL_REQUESTS.sqlreq_DBRead_ARBMON_SETTINGS()
        #q_res = query.exec(req3)
        #
        #if q_res:
        #
        #    if query.isActive():
        #
        #        record_number = query.size()
        #        if not (record_number == -1 or record_number == 0):
        #
        #            b_res = query.first()
        #            while query.isValid():
        #
        #                self.appData.settings.ms_CHANGE_ALARM_WIDGET = query.value("ms_change_alarm_panel")
        #                self.appData.settings.ms_RUNNING_CAPTION_TICK = query.value("ms_running_string_step")
        #                self.appData.settings.ms_SHOW_WORKSHOP = query.value("ms_workshop_pane")
        #                self.appData.settings.ms_SHOW_DIAGRAMS = query.value("ms_diagram_pane")
        #
        #                b_res = query.next()
        #
        #        query.finish()

        #if q_res:
        #    self.appData.window_MainWindow.signal_GetInitialDataReady.emit(True)
        #else:
        #    self.appData.window_MainWindow.signal_GetInitialDataReady.emit(False)


        # можно ли так делать?

        self.msgprc_OnGetDataForSelectedDay(QDate.currentDate())



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_ReadRTData(self):

        #print("get RT data from DB " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))

        q_res = False

        q_res = self.ReadRTData_req1()
        if q_res:
            q_res = self.ReadRTData_req2()
            if q_res:
                q_res = self.ReadRTData_req3()

        self.appData.window_MainWindow.signal_RTDataReadDone.emit(q_res)    # --> worker_MCycle.msgprc_OnRTDataReadDone



#        query = QSqlQuery(self.appData.db)



#        q_res = False

#        req1 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P1()
#        q_res = query.exec(req1)
#
#        if q_res:
#
#            if query.isActive():
#
#                record_number = query.size()
#                if not (record_number == -1 or record_number == 0):
#
#                    b_res = query.first()
#                    while query.isValid():
#
#                        self.appData.CD.date = query.value("the_date")
#                        self.appData.CD.time = query.value("the_time")
#                        self.appData.CD.day = query.value("day_id")
#                        self.appData.CD.day_big = query.value("day_big_id")
#                        self.appData.CD.weekday = query.value("weekday")
#                        self.appData.CD.shiftPlan = query.value("shift_plan_id")
#                        self.appData.CD.shiftPlanCaption = query.value("shift_plan_caption")
#                        self.appData.CD.shift = query.value("shift_id")
#                        self.appData.CD.shiftCaption = query.value("shift_caption")
#                        self.appData.CD.curShiftBTime = query.value("shift_b_time")
#                        self.appData.CD.curShiftETime = query.value("shift_e_time")
#                        self.appData.CD.isNight = query.value("is_night")
#                        self.appData.CD.scheduledBreak = query.value("break_id")
#                        self.appData.CD.scheduledBreakCaption = query.value("break_caption")
#                        self.appData.CD.curScheduledBreakBTime = query.value("break_b_time")
#                        self.appData.CD.curScheduledBreakETime = query.value("break_e_time")
#                        self.appData.CD.isDinner = query.value("is_dinner")
#                        self.appData.CD.isHoliday = query.value("is_holiday")
#                        self.appData.CD.isWorkingShift = query.value("is_working_shift")
#                        self.appData.CD.isWorkingTime = query.value("is_working_time")
#
#                        b_res = query.next()
#
#                query.finish()

#        req2 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P2()
#
#        q_res = q_res and query.exec(req2)
#
#        mt_inf = UDT_MT_INFO()
#
#        if q_res:
#
#            if query.isActive():
#
#                record_number = query.size()
#                if not (record_number == -1 or record_number == 0):
#
#                    b_res = query.first()
#                    while query.isValid():
#
#                        k = 0
#
#                        self.decoder1( query.value("mt01"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        #mt_inf.offline = False
#                        #mt_inf.alr_failure = True
#                        #mt_inf.stp_failure = True
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt02"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        #mt_inf.offline = False
#                        #mt_inf.alr_failure = True
#                        #mt_inf.alr_material = True
#                        #mt_inf.stp_failure = True
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt03"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt04"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt05"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt06"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt07"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt08"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt09"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt10"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt11"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt12"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt13"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt14"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt15"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt16"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt17"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt18"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt19"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt20"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt21"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt22"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        self.decoder1( query.value("mt23"), mt_inf )
#                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
#                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
#                        k += 1
#
#                        b_res = query.next()
#
#                query.finish()

#        req3 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P3()
#
#        q_res = q_res and query.exec(req3)
#
#        mt_st = UDT_MT_STAT_INFO()
#        cl_st = UDT_CL_STAT_INFO()
#
#        if q_res:
#
#            if query.isActive():
#
#                record_number = query.size()
#                if not (record_number == -1 or record_number == 0):
#
#                    b_res = query.first()
#                    while query.isValid():
#
#                        pk_type_id = query.value("pk_type_id")  # 0 = время с начала нажатия кнопки
#                                                                # 1 = суммарное время за смену
#
#                        k = 0
#
#                        self.decoder2( query.value("mt01"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_sum = copy(mt_st.alr_sum)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_sum = copy(mt_st.stp_sum)
#                        k += 1
#
#                        self.decoder2( query.value("mt02"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt03"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt04"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt05"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt06"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt07"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt08"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt09"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt10"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt11"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt12"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt13"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt14"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt15"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt16"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt17"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt18"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt19"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt20"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt21"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt22"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        self.decoder2( query.value("mt23"), mt_st )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
#                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
#                        k += 1
#
#                        if pk_type_id == 2:
#
#                            self.decoder2( query.value("cl1"), cl_st )
#                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
#                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
#                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
#                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
#                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
#                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
#                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
#                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
#                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
#                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
#                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
#                            k += 1
#
#                            self.decoder2( query.value("cl2"), cl_st )
#                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
#                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
#                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
#                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
#                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
#                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
#                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
#                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
#                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
#                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
#                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
#                            k += 1
#
#                            self.decoder2( query.value("cl3"), cl_st )
#                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
#                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
#                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
#                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
#                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
#                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
#                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
#                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
#                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
#                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
#                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
#                            k += 1
#
#                            self.decoder2( query.value("cl4"), cl_st )
#                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
#                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
#                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
#                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
#                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
#                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
#                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
#                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
#                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
#                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
#                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
#                            k += 1
#
#                            self.decoder2( query.value("cl5"), cl_st )
#                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
#                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
#                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
#                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
#                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
#                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
#                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
#                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
#                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
#                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
#                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
#                            k += 1
#
#                        b_res = query.next()
#
#                    query.finish()




        if not self.appData.db is None:
            err = self.appData.db.lastError()
            if err.isValid():
                err_text1 = err.databaseText()
                err_text2 = err.driverText()


        #if q_res:
        #    print("RT data received " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
        #    self.signal_DBReadSuccess.emit()    # -> worker_MCycle::msgprc_OnDBConnOK
        #else:
        #    print("RT data failed " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
        #    self.signal_DBReadFailure.emit()    # опа.. никуда не подключен


    ####################################################################################################################

    @pyqtSlot(QDate)
    def msgprc_OnGetDataForSelectedDay(self, _date):

        query = QSqlQuery(self.appData.db)

        print("get data for selected date " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBRead_GetDataForSelectedDay_R1(_date)
        q_res = query.exec(req1)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        self.appData.buffer_DAY.day_id = query.value("pk_day_id")
                        self.appData.buffer_DAY.day_big_id = query.value("day_big_id")
                        self.appData.buffer_DAY.date = query.value("the_date")
                        self.appData.buffer_DAY.is_weekend = query.value("is_weekend")
                        self.appData.buffer_DAY.is_holiday = query.value("is_holiday")
                        self.appData.buffer_DAY.plan_id = query.value("fk_shift_plan_id")
                        self.appData.buffer_DAY.plan_tag = query.value("plan_tag")
                        self.appData.buffer_DAY.plan_caption = query.value("plan_caption")

                        b_res = query.next()

                    query.finish()

        req2 = SQL_REQUESTS.sqlreq_DBRead_GetDataForSelectedDay_R2(self.appData.buffer_DAY.day_id)
        if q_res:
            q_res = q_res and query.exec(req2)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.buffer_DAY.SHIFTS.clear()
                    b_res = query.first()

                    while query.isValid():

                        sh = UDT_SHIFT()

                        sh.shift_id = query.value("shift_id")
                        sh.shift_big_id = query.value("shift_big_id")
                        sh.shift_type_id = query.value("fk_shift_type_id")
                        sh.shift_number_w_day = query.value("shift_number_w_day")
                        sh.isNight = query.value("is_night")

                        sh.b_time = query.value("b_time")
                        sh.e_time = query.value("e_time")

                        sh.shiftCaption = query.value("shift_caption")

                        self.appData.buffer_DAY.SHIFTS.append(sh)

                        b_res = query.next()

                    query.finish()



        req3 = SQL_REQUESTS.sqlreq_DBRead_GetDataForSelectedDay_R3(self.appData.buffer_DAY.day_id)
        if q_res:
            q_res = q_res and query.exec(req3)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        br = UDT_SCHEDULED_BREAK()

                        br.id = query.value("scheduled_break_big_id")
                        br.active = query.value("active")
                        br.b_time = query.value("b_time")
                        br.e_time = query.value("e_time")
                        br.isDinner = query.value("is_dinner")
                        br.breakCaption = query.value("caption")

                        break_parent_shift = query.value("shift_big_id")

                        for sh in self.appData.buffer_DAY.SHIFTS:
                            if sh.shift_big_id == break_parent_shift:
                                sh.SCHEDULED_BREAKS.append(br)
                                break

                        b_res = query.next()

                    query.finish()

        if not self.appData.db is None:
            err = self.appData.db.lastError()
            if err.isValid():
                err_text1 = err.databaseText()
                err_text2 = err.driverText()


        if q_res:
            print("data for selected date received " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.window_MainWindow.signal_GetDataForSelectedDayReady.emit(True)
        else:
            print("data for selected date failed " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.window_MainWindow.signal_GetDataForSelectedDayReady.emit(False)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnWriteDataForSelectedDay(self):

        query = QSqlQuery(self.appData.db)

        print("write data for selected date " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBWrite_WriteDataForSelectedDay(self.appData.viewer_DAY)
        q_res = query.exec(req1)

        query.finish()

        dummy = 0

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnWriteArbmonSettings(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBWrite_ARBMON_SETTINGS(self.appData)
        q_res = query.exec(req1)

        if q_res:
            self.appData.window_MainWindow.signal_WriteArbmonSettingsDone.emit(True)    # tpane_ARBMON.msgprc_OnWriteArbmonSettingsDone
        else:
            self.appData.window_MainWindow.signal_WriteArbmonSettingsDone.emit(False)   # tpane_ARBMON.msgprc_OnWriteArbmonSettingsDone

    ####################################################################################################################

    def ReadInitialData_req1(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList2()
        q_res = query.exec(req1)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    i = 0
                    while query.isValid():

                        rec = UDT_MACHINE_TOOL()

                        rec.id = query.value("mt_id")
                        rec.uniqnum = query.value("uniqnum")
                        rec.tag = query.value("tag")
                        rec.caption = query.value("mt_caption")
                        rec.short_cap = ""
                        rec.mt_class = query.value("mt_class_caption")
                        rec.persists = query.value("persists")

                        self.appData.MACHINE_TOOLS.append(rec)

                        b_res = query.next()

                query.finish()

        if q_res:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <machine_tools> - OK")
        else:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <machine_tools> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadInitialData_req2(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req2 = SQL_REQUESTS.sqlreq_DBRead_GetFullShiftPlansList()
        q_res = query.exec(req2)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_SHIFTS_PLAN()

                        rec.plan_id = query.value("pk_shift_plan_id")
                        rec.plan_tag = query.value("tag")
                        rec.plan_caption = query.value("caption")

                        self.appData.SHIFTS_PLANS.append(rec)

                        b_res = query.next()

                query.finish()

        if q_res:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <shift_plans> - OK")
        else:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <shift_plans> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWondow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadInitialData_req3(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req3 = SQL_REQUESTS.sqlreq_DBRead_ARBMON_SETTINGS()
        q_res = query.exec(req3)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        self.appData.settings.ms_CHANGE_ALARM_WIDGET = query.value("ms_change_alarm_panel")
                        self.appData.settings.ms_RUNNING_CAPTION_TICK = query.value("ms_running_string_step")
                        self.appData.settings.ms_SHOW_WORKSHOP = query.value("ms_workshop_pane")
                        self.appData.settings.ms_SHOW_DIAGRAMS = query.value("ms_diagram_pane")

                        b_res = query.next()

                query.finish()

        if q_res:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <arbmon_settings> - OK")
        else:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <arbmon_settings> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadInitialData_req4(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req4 = SQL_REQUESTS.sqlreq_DBRead_Credentials()
        q_res = query.exec(req4)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        usr = UDT_USER()

                        usr.id = query.value("pk_user_id")
                        usr.login = query.value("user_login")
                        usr.password = query.value("user_password")
                        usr.caption = query.value("user_caption")
                        usr.permission_view = query.value("permission_view")
                        usr.permission_edit = query.value("permission_edit")

                        self.appData.USERS.append(usr)

                        b_res = query.next()

                query.finish()

        if q_res:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <credentials> - OK")
        else:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() <credentials> - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadRTData_req1(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P1()
        q_res = query.exec(req1)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        self.appData.CD.date = query.value("the_date")
                        self.appData.CD.time = query.value("the_time")
                        self.appData.CD.day = query.value("day_id")
                        self.appData.CD.day_big = query.value("day_big_id")
                        self.appData.CD.weekday = query.value("weekday")
                        self.appData.CD.shiftPlan = query.value("shift_plan_id")
                        self.appData.CD.shiftPlanCaption = query.value("shift_plan_caption")
                        self.appData.CD.shift = query.value("shift_id")
                        self.appData.CD.shiftCaption = query.value("shift_caption")
                        self.appData.CD.curShiftBTime = query.value("shift_b_time")
                        self.appData.CD.curShiftETime = query.value("shift_e_time")
                        self.appData.CD.isNight = query.value("is_night")
                        self.appData.CD.scheduledBreak = query.value("break_id")
                        self.appData.CD.scheduledBreakCaption = query.value("break_caption")
                        self.appData.CD.curScheduledBreakBTime = query.value("break_b_time")
                        self.appData.CD.curScheduledBreakETime = query.value("break_e_time")
                        self.appData.CD.isDinner = query.value("is_dinner")
                        self.appData.CD.isHoliday = query.value("is_holiday")
                        self.appData.CD.isWorkingShift = query.value("is_working_shift")
                        self.appData.CD.isWorkingTime = query.value("is_working_time")

                        b_res = query.next()

                query.finish()

        if q_res:
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <tbl_rt_hours> - OK")
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <tbl_rt_hours> - OK")
        else:
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <tbl_rt_hours> - failed")
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <tbl_rt_hours> - failed")

        #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadRTData_req2(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req2 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P2()
        q_res = query.exec(req2)

        mt_inf = UDT_MT_INFO()

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        k = 0

                        self.decoder1( query.value("mt01"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        #mt_inf.offline = False
                        #mt_inf.alr_failure = True
                        #mt_inf.stp_failure = True
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt02"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        #mt_inf.offline = False
                        #mt_inf.alr_failure = True
                        #mt_inf.alr_material = True
                        #mt_inf.stp_failure = True
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt03"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt04"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt05"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt06"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt07"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt08"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt09"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt10"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt11"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt12"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt13"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt14"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt15"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt16"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt17"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt18"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt19"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt20"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt21"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt22"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        self.decoder1( query.value("mt23"), mt_inf )
                        mt_inf.mt_id = copy( self.appData.CD.MT_INFO[k].mt_id )
                        self.appData.CD.MT_INFO[k] = copy(mt_inf)
                        k += 1

                        b_res = query.next()

                query.finish()

        if q_res:
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_info> - OK")
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_info> - OK")
        else:
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_info> - failed")
            self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_info> - OK")

        #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

        return q_res

    ####################################################################################################################

    def ReadRTData_req3(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req3 = SQL_REQUESTS.sqlreq_DBRead_GetRTData_P3()
        q_res = query.exec(req3)

        mt_st = UDT_MT_STAT_INFO()
        cl_st = UDT_CL_STAT_INFO()

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    b_res = query.first()
                    while query.isValid():

                        pk_type_id = query.value("pk_type_id")  # 0 = время с начала нажатия кнопки
                                                                # 1 = суммарное время за смену

                        k = 0

                        self.decoder2( query.value("mt01"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_sum = copy(mt_st.alr_sum)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_sum = copy(mt_st.stp_sum)
                        k += 1

                        xxx = query.value("mt02")
                        self.decoder2( query.value("mt02"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt03"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt04"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt05"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt06"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt07"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt08"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt09"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt10"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt11"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt12"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt13"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt14"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt15"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt16"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt17"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt18"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt19"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt20"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt21"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt22"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        self.decoder2( query.value("mt23"), mt_st )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].offline = copy( mt_st.offline )
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_failure = copy(mt_st.alr_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].alr_material = copy(mt_st.alr_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_failure = copy(mt_st.stp_failure)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_material = copy(mt_st.stp_material)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_process = copy(mt_st.stp_process)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].stp_quality = copy(mt_st.stp_quality)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_1 = copy(mt_st.aux_1)
                        self.appData.CD.MT_STAT[pk_type_id - 1][k].aux_2 = copy(mt_st.aux_2)
                        k += 1

                        if pk_type_id == 2:

                            self.decoder2( query.value("cl01"), cl_st )
                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
                            k += 1

                            self.decoder2( query.value("cl02"), cl_st )
                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
                            k += 1

                            self.decoder2( query.value("cl03"), cl_st )
                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
                            k += 1

                            self.decoder2( query.value("cl04"), cl_st )
                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
                            k += 1

                            self.decoder2( query.value("cl05"), cl_st )
                            self.appData.CD.MT_STAT[1][k].offline = copy( cl_st.offline )
                            self.appData.CD.MT_STAT[1][k].alr_failure = copy(cl_st.alr_failure)
                            self.appData.CD.MT_STAT[1][k].alr_material = copy(cl_st.alr_material)
                            self.appData.CD.MT_STAT[1][k].stp_failure = copy(cl_st.stp_failure)
                            self.appData.CD.MT_STAT[1][k].stp_material = copy(cl_st.stp_material)
                            self.appData.CD.MT_STAT[1][k].stp_process = copy(cl_st.stp_process)
                            self.appData.CD.MT_STAT[1][k].stp_quality = copy(cl_st.stp_quality)
                            self.appData.CD.MT_STAT[1][k].aux_1 = copy(cl_st.aux_1)
                            self.appData.CD.MT_STAT[1][k].aux_2 = copy(cl_st.aux_2)
                            self.appData.CD.MT_STAT[1][k].alr_sum = copy(cl_st.alr_sum)
                            self.appData.CD.MT_STAT[1][k].stp_sum = copy(cl_st.stp_sum)
                            k += 1

                        b_res = query.next()

                    query.finish()

            if q_res:
                #self.appData.model_DBAccessTrackerBack.append(
                #    QDateTime.currentDateTime().toString(
                #        "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_stat> - OK")
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_stat> - OK")
            else:
                #self.appData.model_DBAccessTrackerBack.append(
                #    QDateTime.currentDateTime().toString(
                #        "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_stat> - failed")
                self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() <mt_stat> - failed")

            #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateDBAccessTracker

            return q_res

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReadTableDetailedReport(self):

        query = QSqlQuery(self.appData.db)

        q_res = False

        req1 = SQL_REQUESTS.sqlreq_DBRead_TblDetailedRep(self.appData,self.appData.settings.enum_ReportSortBy)
        q_res = query.exec(req1)

        if q_res:

            if query.isActive():

                record_number = query.size()
                if not (record_number == -1 or record_number == 0):

                    self.appData.DETAILED_REP_ARR.clear()

                    b_res = query.first()
                    while query.isValid():

                        rec = UDT_DETAILS_T1_V00_RECORD()

                        rec.rec_id = query.value("rec_id")
                        rec.mt_class_id = query.value("mt_class_id")
                        rec.mt_class_caption = query.value("mt_class_caption")
                        rec.mt_id = query.value("mt_id")
                        rec.mt_tag = query.value("mt_tag")
                        rec.mt_caption = query.value("mt_caption")
                        rec.state_cap1 = query.value("state_cap1")
                        rec.state_cap2 = query.value("state_cap2")
                        rec.b_dt = query.value("b_dt")
                        rec.e_dt = query.value("e_dt")
                        rec.full_time = query.value("full_time")
                        rec.act_time = query.value("act_time")
                        rec.b_rec_id = query.value("b_rec_id")
                        rec.e_rec_id = query.value("e_rec_id")
                        rec.state_id = query.value("state_id")


                        self.appData.DETAILED_REP_ARR.append(rec)

                        b_res = query.next()

                query.finish()


        self.appData.window_MainWindow.signal_DBRead_TblDetailedRep_Done.emit(q_res)