########################################################################################################################

from PyQt5.QtCore import QDateTime, QDate, QTime

########################################################################################################################

from enums import *
from udt_db_functions import DBTIME

########################################################################################################################

class SQL_REQUESTS():

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetFullMTClassesList():

        req = "SELECT * FROM vew_machine_tool_classes"

        return req

    @staticmethod
    def sqlreq_DBRead_GetFullMTClassesList2():

        req = "SELECT " +\
              "tbl_machine_tool_classes.pk_mt_class_id, tbl_machine_tool_classes.caption, tbl_machine_tool_classes.notes " +\
              "FROM tbl_machine_tool_classes " +\
              "WHERE tbl_machine_tool_classes.pk_mt_class_id<>0 AND tbl_machine_tool_classes.persists=True " +\
              "ORDER BY pk_mt_class_id"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetFullShiftPlansList():

        req = "SELECT tbl_shift_plan_names.* " \
              "FROM tbl_shift_plan_names " \
              "WHERE pk_shift_plan_id <> 0"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetFullShiftTypesList():
        """
        req = "SELECT " +\
              "tbl_shift_types.*,tbl_shifts.shift_number_w_day " +\
              "FROM tbl_shift_types " +\
              "LEFT JOIN tbl_shifts ON tbl_shift_types.pk_shift_type_pd = tbl_shifts.fk_shift_type_id " +\
              "WHERE tbl_shift_types.pk_shift_type_id <> 0 " +\
              "ORDER BY pk_shift_type_id"
        """
        req = "SELECT " +\
              "tbl_shift_types.pk_shift_type_id, tbl_shift_types.caption " +\
              "FROM tbl_shift_types " +\
              "WHERE tbl_shift_types.pk_shift_type_id <> 0 " +\
              "ORDER BY pk_shift_type_id"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_CurrentDay(date):

        req = "SELECT " +\
              "tbl_calender.*, tbl_shift_plan_names.tag AS plan_tag, tbl_shift_plan_names.caption AS plan_caption " +\
              "FROM tbl_calender LEFT JOIN tbl_shift_plan_names ON tbl_calender.fk_shift_plan_id = tbl_shift_plan_names.pk_shift_plan_id " +\
              "WHERE tbl_calender.the_date='" + date.toString("yyyy-MM-dd") + "'::date"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_ActiveShiftsForDay(day):

        #req = "SELECT " +\
	    #            "tbl_shifts.day_id, " + \
        #            "tbl_shifts.shift_id, " + \
	    #            "tbl_shifts.fk_shift_type_id, tbl_shift_types.caption AS shift_caption, " +\
	    #            "tbl_shifts.b_time, tbl_shifts.e_time, tbl_shifts.active, tbl_shifts.shift_number_w_day, tbl_shifts.is_night, " + \
        #            "tbl_shifts.is_working_shift " + \
        #        "FROM tbl_shifts " +\
        #        "LEFT JOIN tbl_shift_types ON tbl_shifts.fk_shift_type_id=tbl_shift_types.pk_shift_type_id " +\
        #        "WHERE tbl_shifts.day_id=" + str(day) + " " +\
        #        "AND (tbl_shifts.active=True OR tbl_shifts.is_night=True)"

        req = "WITH tmp AS( " +\
              "SELECT tbl_shifts.*, tbl_calender.fk_shift_plan_id, tbl_shift_types.caption AS shift_caption " +\
              "FROM tbl_shifts " +\
              "LEFT JOIN tbl_calender ON tbl_shifts.fk_day_id = tbl_calender.pk_day_id " +\
              "LEFT JOIN tbl_shift_types ON tbl_shifts.fk_shift_type_id = tbl_shift_types.pk_shift_type_id " +\
              "WHERE tbl_shifts.fk_day_id=" + str(day) + ") " +\
              "SELECT tmp.* FROM tmp " +\
              "WHERE (tmp.fk_shift_plan_id = 1 AND( tmp.fk_shift_type_id = 1 OR tmp.fk_shift_type_id = 2 OR tmp.fk_shift_type_id = 3 ))OR " +\
              "(tmp.fk_shift_plan_id = 2 AND( tmp.fk_shift_type_id = 4 OR tmp.fk_shift_type_id = 5))"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_ActiveBreaksForDay(day):

       #req = "SELECT " +\
	   #            "tbl_scheduled_breaks.day_id, " +\
	   #            "tbl_scheduled_breaks.fk_scheduled_break_type_id, tbl_scheduled_break_types.caption AS scheduled_break_caption, " +\
	   #            "tbl_scheduled_breaks.b_time, tbl_scheduled_breaks.e_time, tbl_scheduled_breaks.active, tbl_scheduled_breaks.is_dinner " +\
       #        "FROM tbl_scheduled_breaks " +\
       #        "LEFT JOIN tbl_scheduled_break_types ON tbl_scheduled_breaks.fk_scheduled_break_type_id=tbl_scheduled_break_types.pk_scheduled_break_type_id " +\
       #        "WHERE tbl_scheduled_breaks.day_id=" + str(day) + " AND tbl_scheduled_breaks.active=true"

        req = "SELECT tbl_scheduled_breaks.*, tbl_scheduled_break_types.caption " +\
              "FROM tbl_scheduled_breaks " +\
              "LEFT JOIN tbl_scheduled_break_types ON tbl_scheduled_breaks.fk_scheduled_break_type_id = tbl_scheduled_break_types.pk_scheduled_break_type_id " +\
              "WHERE tbl_scheduled_breaks.fk_day_id = " + str(day) + " AND tbl_scheduled_breaks.active = true"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWriteTblRtHours_0(app_data):   # это использовалось для теста

        req = "INSERT INTO tbl_rt_hours(pk_id,the_date,the_time,shift_plan_id,shift_plan_caption,shift_id,shift_caption," +\
            "is_night,break_id,break_caption,is_dinner,notes) VALUES (1,'" +\
            app_data.CD.date.toString("yyyy-MM-dd") + "'::date,'" +\
            app_data.CD.time.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.CD.shiftPlan) + ",'" + app_data.CD.shiftPlanCaption + "'," +\
            str(app_data.CD.shift) + ",'" + app_data.CD.shiftCaption + "'," + str(int(app_data.CD.isNight)) +\
            "," + str(app_data.CD.scheduledBreak) + ",'" + app_data.CD.scheduledBreakCaption + "'," +\
            str(int(app_data.CD.isDinner)) + "," + "'')"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWriteTblRtHours(app_data):

        req = ""
        test_str = app_data.CD.date.toString("yyyy-MM-dd")

        if app_data.CD.shiftCaption is not None and app_data.CD.scheduledBreakCaption is not None:

            req = "UPDATE tbl_rt_hours SET the_date='" + app_data.CD.date.toString("yyyy-MM-dd") + "'::date," +\
                "the_time='" + app_data.CD.time.toString("hh:mm:ss.zzz") + "'::time," +\
                "day_id=" + str(app_data.CD.day) + "," +\
                "day_big_id=" + str(app_data.CD.day_big) + "," +\
                "weekday=" + str(app_data.CD.weekday) + "," +\
                "shift_plan_id=" + str(app_data.CD.shiftPlan) + "," +\
                "shift_plan_caption='" + app_data.CD.shiftPlanCaption + "'," +\
                "shift_id=" + str(app_data.CD.shift) + "," +\
                "shift_caption='" + app_data.CD.shiftCaption + "'," +\
                "shift_b_time='" + app_data.CD.curShiftBTime.toString("hh:mm:ss.zzz") + "'::time," + \
                "shift_e_time='" + app_data.CD.curShiftETime.toString("hh:mm:ss.zzz") + "'::time," + \
                "is_night=" + str(app_data.CD.isNight) + "," +\
                "break_id=" + str(app_data.CD.scheduledBreak) + "," +\
                "break_caption='" + app_data.CD.scheduledBreakCaption + "'," + \
                "break_b_time='" + app_data.CD.curScheduledBreakBTime.toString("hh:mm:ss.zzz") + "'::time," + \
                "break_e_time='" + app_data.CD.curScheduledBreakETime.toString("hh:mm:ss.zzz") + "'::time," + \
                "is_dinner=" + str(app_data.CD.isDinner) + "," + \
                "is_holiday=" + str(app_data.CD.isDinner) + "," + \
                "is_working_shift=" + str(app_data.CD.isWorkingShift) + "," + \
                "is_working_time=" + str(app_data.CD.isWorkingTime) + "," + \
                "notes=" + "'' WHERE pk_id=1"     # is_working_time = is_working_shift and not is_break

        return req

    ####################################################################################################################
    """
    @staticmethod
    def sqlreq_DBWrite_TblStatByMT_0(app_data, station): # это переделываем потому что изменил формат таблицы

        tm0 = QTime(0, 0, 0, 0)

        if station.PAR.id == ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY:
            gr = 0 # добвать в тип - значения выбирать из базы при инициализации программы !!!
                    # не нужно делать никаких статтических данных в теле программы !
                    # описания станков хранятся в базе !
                    # всё должно быть динамически !
            mt = 0
        if station.PAR.id == ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN:
            gr = 0
            mt = 1

        tm1 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msAlarmOnFailure)
        tm2 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msAlarmOnMaterial)
        tm3 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msStopOnFailure)
        tm4 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msStopOnMaterial)
        tm5 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msStopOnProcess)
        tm6 = tm0.addMSecs(app_data.statistics.groups[gr].mtools[mt].cumulative_time_d.msStopOnQuality)

        req = "INSERT INTO tbl_stat_by_mt(fk_day_id,fk_mt_id,sum_alr_failure,sum_alr_material,sum_stp_failure," +\
            "sum_stp_material,sum_stp_process,sum_stp_quality) " +\
            "VALUES (" +\
            str(app_data.DBD.day_id) + "," + str(mt+1) + ",'" +\
            tm1.toString("hh:mm:ss.zzz") + "'::time,'" +\
            tm2.toString("hh:mm:ss.zzz") + "'::time,'" +\
            tm3.toString("hh:mm:ss.zzz") + "'::time,'" +\
            tm4.toString("hh:mm:ss.zzz") + "'::time,'" +\
            tm5.toString("hh:mm:ss.zzz") + "'::time,'" +\
            tm6.toString("hh:mm:ss.zzz") + "'::time" +\
            ")"

        return req

    @staticmethod
    def sqlreq_DBWrite_TblStatByMT(app_data, station):

        tm0 = QTime(0, 0, 0, 0)

        tm1 = tm0.addMSecs(app_data.statistics.groups[station.PAR.mt_class_id].mtools[station.PAR.mt_id].cumulative_time_d.msAlarmOnFailure)
        tm2 = tm0.addMSecs(app_data.statistics.groups[station.PAR.mt_class_id].mtools[station.PAR.mt_id].cumulative_time_d.msAlarmOnMaterial)
        tm3 = tm0.addMSecs(app_data.statistics.groups[station.PAR.mt_class_id].mtools[station.PAR.mt_id].cumulative_time_d.msStopOnFailure)


        req = "INSERT INTO tbl_stat_by_mt(fk_day_id,fk_mt_id,fk_data_id,the_data) " +\
            "VALUES (" +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "1" + "'" + tm1.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "2" + "'" + tm2.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "3" + "'" + tm3.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "4" + "'" + tm4.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "5" + "'" + tm5.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "6" + "'" + tm6.toString("hh:mm:ss.zzz") + "'::time," +\
            str(app_data.DBD.day_id) + "," + str(station.PAR.mt_id) + "," + "7" + "'" + tm7.toString("hh:mm:ss.zzz") + "'::time" +\
            ")"

        return req
    """
    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_TblReportT1(app_data):

        req = "SELECT * FROM fn_populate_tbl_rep_t1_v00('" + app_data.settings.reportStartDate.toString("yyyy-MM-dd") + "'::date)"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_TblStatByMT_0():    # это удалить - это неправильно - пересмотрел таблицу

        req = "WITH tmp1 AS(SELECT tbl_calender.the_date, " + \
            "tbl_calender.is_dayout, " + \
            "tbl_stat_by_mt.fk_day_id, " +\
            "tbl_stat_by_mt.fk_mt_id, " +\
            "tbl_machine_tools.uniqnum AS mt_uniqnum, " +\
            "tbl_machine_tools.tag AS mt_tag, " +\
            "tbl_machine_tools.caption AS mt_caption, " +\
            "tbl_machine_tool_classes.caption AS mt_class_caption, " +\
            "tbl_stat_by_mt.sum_alr_failure, " +\
            "tbl_stat_by_mt.sum_alr_material " +\
            "FROM tbl_stat_by_mt " +\
            "INNER JOIN tbl_calender ON tbl_calender.pk_day_id = tbl_stat_by_mt.fk_day_id " +\
            "INNER JOIN tbl_machine_tools ON tbl_machine_tools.pk_mt_id = tbl_stat_by_mt.fk_mt_id " +\
            "INNER JOIN tbl_machine_tool_classes ON tbl_machine_tool_classes.pk_class_id = tbl_machine_tools.fk_class_id) " +\
            "SELECT * FROM tmp1 " +\
            "ORDER BY the_date ASC, fk_mt_id ASC"

        return req

    @staticmethod
    def sqlreq_DBRead_TblReportT2(app_data):

        # req = "SELECT * FROM populate_tbl_rep_t2_v00()"
        req = "SELECT * FROM fn_populate_tbl_rep_t2_v00('" + app_data.settings.reportStartDate.toString("yyyy-MM-dd") + "'::date)"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetFullMachineToolsList():

        req = "SELECT * FROM vew_machine_tools"

        return req

    @staticmethod
    def sqlreq_DBRead_GetFullMachineToolsList2():

        req = "SELECT " +\
              "tbl_machine_tools.pk_mt_id AS mt_id," +\
              "tbl_machine_tools.uniqnum," +\
              "tbl_machine_tools.tag," +\
              "tbl_machine_tools.caption AS mt_caption," + \
              "tbl_machine_tools.short_cap AS mt_short_cap," + \
              "tbl_machine_tool_classes.caption AS mt_class_caption " +\
              "FROM(" +\
              "tbl_machine_tools LEFT JOIN tbl_machine_tool_classes ON (tbl_machine_tool_classes.pk_mt_class_id=tbl_machine_tools.fk_mt_class_id)) " +\
              "WHERE tbl_machine_tools.uniqnum<>0 AND tbl_machine_tools.persists=True " +\
              "ORDER BY mt_id"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetRTData_P1():

        req = "SELECT * FROM tbl_rt_hours WHERE pk_id=1"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetRTData_P2():

        req = "SELECT * FROM tbl_states_history WHERE pk_rec_id=(SELECT MAX(pk_rec_id) FROM tbl_states_history)"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetRTData_P3():

        req = "SELECT * FROM tbl_rt_stat WHERE pk_type_id=1 OR pk_type_id=2"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WrStatesHist(app_data):

        dt = QDateTime.currentDateTime()    # this is the very moment of fetching PC time to be stored in DB (!)
        year_id = app_data.CD.year
        month_id = app_data.CD.month
        day_id = app_data.CD.day
        day_big_id = app_data.CD.day_big
        shift_id = app_data.CD.shift
        shift_big_id = app_data.CD.shift_big
        fk_scheduled_break_id = app_data.CD.scheduledBreak
        is_holiday = app_data.CD.isHoliday
        is_night = app_data.CD.isNight
        is_dinner = app_data.CD.isDinner
        is_scheduled_break = app_data.CD.isScheduledBreak
        is_working_day = app_data.CD.isWorkingDay
        is_working_shift = app_data.CD.isWorkingShift
        is_working_time = app_data.CD.isWorkingTime

        mt01 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY-1].toDBField()
        mt02 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN-1].toDBField()
        mt03 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600-1].toDBField()
        mt04 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000-1].toDBField()
        mt05 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000-1].toDBField()
        mt06 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT-1].toDBField()
        mt07 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1-1].toDBField()
        mt08 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2-1].toDBField()
        mt09 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM-1].toDBField()
        mt10 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL-1].toDBField()
        mt11 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3-1].toDBField()
        mt12 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P6_TRUBEND-1].toDBField()
        mt13 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN-1].toDBField()
        mt14 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW-1].toDBField()
        mt15 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT-1].toDBField()
        mt16 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT-1].toDBField()
        mt17 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_17-1].toDBField()
        mt18 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_18-1].toDBField()
        mt19 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_19-1].toDBField()
        mt20 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_20-1].toDBField()
        mt21 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_21-1].toDBField()
        mt22 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_22-1].toDBField()
        mt23 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_23-1].toDBField()
        mt24 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_24 - 1].toDBField()
        mt25 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_25 - 1].toDBField()
        
        cf01 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY-1].cfToDBField()
        cf02 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN-1].cfToDBField()
        cf03 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600-1].cfToDBField()
        cf04 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000-1].cfToDBField()
        cf05 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000-1].cfToDBField()
        cf06 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT-1].cfToDBField()
        cf07 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1-1].cfToDBField()
        cf08 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2-1].cfToDBField()
        cf09 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM-1].cfToDBField()
        cf10 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL-1].cfToDBField()
        cf11 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3-1].cfToDBField()
        cf12 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P6_TRUBEND-1].cfToDBField()
        cf13 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN-1].cfToDBField()
        cf14 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW-1].cfToDBField()
        cf15 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT-1].cfToDBField()
        cf16 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT-1].cfToDBField()
        cf17 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_17-1].cfToDBField()
        cf18 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_18-1].cfToDBField()
        cf19 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_19-1].cfToDBField()
        cf20 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_20-1].cfToDBField()
        cf21 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_21-1].cfToDBField()
        cf22 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_22-1].cfToDBField()
        cf23 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_23-1].cfToDBField()
        cf24 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_24 - 1].cfToDBField()
        cf25 = app_data.CD.MT_INFO[ENM_MACHINE_TOOLS.MT_25 - 1].cfToDBField()


        req = "INSERT INTO tbl_states_history(dt,year_id,month_id,day_id,day_big_id,shift_id,shift_big_id,fk_scheduled_break_id,is_holiday,is_night," +\
                "is_dinner,is_scheduled_break,is_working_day,is_working_shift,is_working_time," +\
                "mt01,mt02,mt03,mt04,mt05,mt06,mt07,mt08,mt09,mt10,mt11,mt12,mt13,mt14,mt15,mt16,mt17,mt18,mt19,mt20,mt21,mt22,mt23,mt24,mt25," +\
                "cf01,cf02,cf03,cf04,cf05,cf06,cf07,cf08,cf09,cf10,cf11,cf12,cf13,cf14,cf15,cf16,cf17,cf18,cf19,cf20,cf21,cf22,cf23,cf24,cf25) "+\
                "VALUES" +\
                "('" + DBTIME.QDateTime2DbDateTime(dt) + "'::timestamp," + str(year_id) + "," + str(month_id) + "," + str(day_id) + "," + str(day_big_id) + "," + str(shift_id) + "," + str(shift_big_id) + "," +\
                str(fk_scheduled_break_id) + "," + str(is_holiday) + "," + str(is_night) + "," + str(is_dinner) + "," +\
                str(is_scheduled_break) + ","  + str(is_working_day) + ","  + str(is_working_shift) + "," + str(is_working_time) + ",'" +\
                mt01 + "','" + mt02 + "','" + mt03 + "','" + mt04 + "','" + mt05 + "','" + mt06 + "','" + mt07 + "','" + mt08 + "','" + mt09 + "','" + mt10 + "','" + \
                mt11 + "','" + mt12 + "','" + mt13 + "','" + mt14 + "','" + mt15 + "','" + mt16 + "','" + mt17 + "','" + mt18 + "','" + mt19 + "','" + mt20 + "','" + \
                mt21 + "','" + mt22 + "','" + mt23 + "','" + mt24 + "','" + mt25 + "','" + \
                cf01 + "','" + cf02 + "','" + cf03 + "','" + cf04 + "','" + cf05 + "','" + cf06 + "','" + cf07 + "','" + cf08 + "','" + cf09 + "','" + cf10 + "','" + \
                cf11 + "','" + cf12 + "','" + cf13 + "','" + cf14 + "','" + cf15 + "','" + cf16 + "','" + cf17 + "','" + cf18 + "','" + cf19 + "','" + cf20 + "','" + \
                cf21 + "','" + cf22 + "','" + cf23 + "','" + cf24 + "','" + cf25 + "'" + \
                ")"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WrShiftStat(app_data):

        ctime = QTime.currentTime()  # PC time stored with this data in DB

        req = "SELECT * FROM fn_cs_shift(" +\
              "'" + str(DBTIME.QTime2DbTime(ctime)) + "'::time," +\
              'CAST(' + str(app_data.CD.sh_Z1_year) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.sh_Z1_month) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.sh_Z1_day) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift_Z1) + " AS integer)," + \
              'CAST(' + str(app_data.CD.shiftType_Z1) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift_w_day_Z1) + " AS smallint))"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WrDailyStat(app_data):

        ctime = QTime.currentTime()  # PC time stored with this data in DB

        req = "SELECT * FROM fn_cs_day(" +\
              "'" + str(DBTIME.QTime2DbTime(ctime)) + "'::time," +\
              'CAST(' + str(app_data.CD.year) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.month) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.day) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift) + " AS integer)," + \
              'CAST(' + str(app_data.CD.shiftType) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift_w_day) + " AS smallint))"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WrMonthStat(app_data):

        ctime = QTime.currentTime()  # PC time stored with this data in DB

        req = "SELECT * FROM fn_cs_month(" +\
              "'" + str(DBTIME.QTime2DbTime(ctime)) + "'::time," +\
              'CAST(' + str(app_data.CD.year) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.month) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.day) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift) + " AS integer)," + \
              'CAST(' + str(app_data.CD.shiftType) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift_w_day) + " AS smallint))"


        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WrYearStat(app_data):

        ctime = QTime.currentTime()  # PC time stored with this data in DB

        req = "SELECT * FROM fn_cs_year(" +\
              "'" + str(DBTIME.QTime2DbTime(ctime)) + "'::time," +\
              'CAST(' + str(app_data.CD.year) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.month) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.day) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift) + " AS integer)," + \
              'CAST(' + str(app_data.CD.shiftType) + " AS smallint)," + \
              'CAST(' + str(app_data.CD.shift_w_day) + " AS smallint))"


        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetDataForSelectedDay_R1(date):

        req = "SELECT " +\
              "tbl_calender.*, tbl_shift_plan_names.tag AS plan_tag, tbl_shift_plan_names.caption AS plan_caption " +\
              "FROM tbl_calender LEFT JOIN tbl_shift_plan_names ON tbl_calender.fk_shift_plan_id = tbl_shift_plan_names.pk_shift_plan_id " +\
              "WHERE tbl_calender.the_date='" + date.toString("yyyy-MM-dd") + "'::date"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetDataForSelectedDay_R2(day):    # list of shifts

        #req = "WITH tmp AS( " +\
        #      "SELECT tbl_shifts.*, tbl_calender.fk_shift_plan_id, tbl_shift_types.caption AS shift_caption " +\
        #      "FROM tbl_shifts " +\
        #      "LEFT JOIN tbl_calender ON tbl_shifts.fk_day_id = tbl_calender.pk_day_id " +\
        #      "LEFT JOIN tbl_shift_types ON tbl_shifts.fk_shift_type_id = tbl_shift_types.pk_shift_type_id " +\
        #      "WHERE tbl_shifts.fk_day_id=" + str(day) + ") " +\
        #      "SELECT tmp.* FROM tmp " +\
        #      "WHERE (tmp.fk_shift_plan_id = 1 AND( tmp.fk_shift_type_id = 1 OR tmp.fk_shift_type_id = 2 OR tmp.fk_shift_type_id = 3 ))OR " +\
        #      "(tmp.fk_shift_plan_id = 2 AND( tmp.fk_shift_type_id = 4 OR tmp.fk_shift_type_id = 5))"

        req = "SELECT tbl_shifts.*, tbl_calender.fk_shift_plan_id, tbl_shift_types.caption AS shift_caption " +\
              "FROM tbl_shifts " +\
              "LEFT JOIN tbl_calender ON tbl_shifts.fk_day_id = tbl_calender.pk_day_id " +\
              "LEFT JOIN tbl_shift_types ON tbl_shifts.fk_shift_type_id = tbl_shift_types.pk_shift_type_id " +\
              "WHERE tbl_shifts.fk_day_id=" + str(day) + " " +\
              "ORDER BY fk_shift_type_id"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_GetDataForSelectedDay_R3(day):    # list of scheduled breaks

        #req = "SELECT tbl_scheduled_breaks.*, tbl_scheduled_break_types.caption " +\
        #      "FROM tbl_scheduled_breaks " +\
        #      "LEFT JOIN tbl_scheduled_break_types ON tbl_scheduled_breaks.fk_scheduled_break_type_id = tbl_scheduled_break_types.pk_scheduled_break_type_id " +\
        #      "WHERE tbl_scheduled_breaks.fk_day_id = " + str(day) + " AND tbl_scheduled_breaks.active = true"

        req = "SELECT tbl_scheduled_breaks.*, tbl_scheduled_break_types.caption " +\
              "FROM tbl_scheduled_breaks " +\
              "LEFT JOIN tbl_scheduled_break_types ON tbl_scheduled_breaks.fk_scheduled_break_type_id = tbl_scheduled_break_types.pk_scheduled_break_type_id " +\
              "WHERE tbl_scheduled_breaks.fk_day_id = " + str(day) + " " +\
              "ORDER BY fk_shift_type_id,fk_scheduled_break_type_id"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_WriteDataForSelectedDay(viewer_day):

        _str = "("

        dy = viewer_day
        day1 = str(dy.day_id) + "::smallint," + str(dy.day_big_id) + "," + str(dy.is_holiday) + "," + str(dy.plan_id) + "::smallint"

        _str += day1
        _str += ", "
        _str += "ARRAY["

        for sh in viewer_day.SHIFTS:
            shift1 = "(" + str(sh.shift_id) + "::smallint," + str(sh.shift_big_id) + ",'" + sh.b_time.toString(
                "hh:mm:ss.000") + "'::time,'" + sh.e_time.toString("hh:mm:ss.000") + "'::time," + str(sh.isNight)
            _str += shift1
            _str += ", "
            _str += "ARRAY["
            for br in sh.SCHEDULED_BREAKS:
                break1 = "(" + str(br.id) + ",'" + br.b_time.toString("hh:mm:ss.000") + "'::time,'" + br.e_time.toString(
                    "hh:mm:ss.000") + "'::time," + str(br.active) + "," + str(br.isDinner) + ")::udt_scheduled_break,"
                _str += break1
            _str = _str[:-1] + "])::udt_shift,"

        _str = _str[:-1] + "])::udt_day"



        req = "SELECT * FROM fn_write_day_data(" + _str + ")"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_ARBMON_SETTINGS():

        req = "SELECT * FROM tbl_arbmon_settings"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBWrite_ARBMON_SETTINGS(app_data):

        req = "UPDATE tbl_arbmon_settings SET " +\
              "ms_change_alarm_panel=" + str(app_data.settings.ms_CHANGE_ALARM_WIDGET) + "," + \
              "ms_running_string_step=" + str(app_data.settings.ms_RUNNING_CAPTION_TICK) + "," + \
              "ms_workshop_pane=" + str(app_data.settings.ms_SHOW_WORKSHOP) + "," + \
              "ms_diagram_pane=" + str(app_data.settings.ms_SHOW_DIAGRAMS)


        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_Credentials():

        req = "SELECT * FROM tbl_users"

        return req

    ####################################################################################################################

    @staticmethod
    def sqlreq_DBRead_TblDetailedRep(app_data, sorting):

        if sorting == 1:    # by time

            req = "SELECT * FROM fn_populate_tbl_det_t1_v00(" +\
                "'" + app_data.settings.date_ReportBeginDate.toString("yyyy-MM-dd") + " " + app_data.settings.time_ReportBeginTime.toString("hh:mm:ss.000") + "'::timestamp," + \
                "'" + app_data.settings.date_ReportEndDate.toString("yyyy-MM-dd") + " " + app_data.settings.time_ReportEndTime.toString("hh:mm:ss.000") + "'::timestamp)" +\
                "ORDER BY b_rec_id ASC, e_rec_id ASC, state_id ASC"

        elif sorting == 2:  # by machine tool id

            req = "SELECT * FROM fn_populate_tbl_det_t1_v00(" +\
                "'" + app_data.settings.date_ReportBeginDate.toString("yyyy-MM-dd") + " " + app_data.settings.time_ReportBeginTime.toString("hh:mm:ss.000") + "'::timestamp," + \
                "'" + app_data.settings.date_ReportEndDate.toString("yyyy-MM-dd") + " " + app_data.settings.time_ReportEndTime.toString("hh:mm:ss.000") + "'::timestamp)" + \
                "ORDER BY mt_id ASC, b_rec_id ASC, e_rec_id ASC, state_id ASC"

        return req

    ####################################################################################################################


