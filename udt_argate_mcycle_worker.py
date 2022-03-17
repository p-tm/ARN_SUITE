########################################################################################################################

# pip install pywin32
import win32com.client
import pythoncom

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate, QTime, QDateTime

from PyQt5.QtGui import QColor

########################################################################################################################

from enums import *
from sql_requests import SQL_REQUESTS
from global_functions import *
from exporter import EXPORTER

from udt_report_generation_supervisor import UDT_REPORT_GENERATION_SUPERVISOR


########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_DIS():

    def __init__(self):

        self.IN = False

        self.Q = False
        self.QR = False
        self.QF = False

        self.IN_Z0 = False
        self.IN_Z1 = False

    def update(self):

        self.IN_Z0 = self.IN

        self.Q = self.IN_Z0

        self.QR = self.IN_Z0 and not self.IN_Z1
        self.QF = self.IN_Z1 and not self.IN_Z0

        self.IN_Z1 = self.IN_Z0

########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class UDT_ARGATE_MCYCLE_WORKER(QObject):

    signal_DataReady = pyqtSignal(int)              # field data is ready (read)

    signal_DBWrite_CyclicData = pyqtSignal()        # cyclic data is ready to be written to DB
    signal_DBWrite_EOShiftData = pyqtSignal()
    signal_DBWrite_EODayData = pyqtSignal()

    signal_DBRead_GetDailyData = pyqtSignal(QDate)  #
    #signal_DBRead_TblReportT1 = pyqtSignal(int)
    #signal_DBRead_TblReportT2 = pyqtSignal(int)

    signal_TickUpdate = pyqtSignal()                #

    signal_EndOfShift = pyqtSignal()
    signal_EndOfDay = pyqtSignal()
    signal_EndOfMonth = pyqtSignal()
    signal_EndOfYear = pyqtSignal()

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        #self.end_of_shift = UDT_DIS()
        #self.end_of_day = UDT_DIS()
        #self.end_of_week = UDT_DIS()

        WRITE_SHIFT_STAT = False
        WRITE_DAILY_STAT = False
        WRITE_MONTH_STAT = False
        WRITE_YEAR_STAT = False

        SHIFT_STAT_WRITTEN = False
        DAILY_STAT_WRITTEN = False
        MONTH_STAT_WRITTEN = False

        self.end_of_shift_A = UDT_DIS()
        self.end_of_day_A = UDT_DIS()
        self.end_of_month_A= UDT_DIS()
        self.end_of_year_A = UDT_DIS()




    ####################################################################################################################

    def connectSignals(self):

        self.signal_DBWrite_CyclicData.connect(self.appData.worker_DBAccess.msgprc_OnDBWrite_CyclicData)
        self.signal_DBWrite_EODayData.connect(self.appData.worker_DBAccess.msgprc_OnDBWrite_EODayData)

        self.signal_DBRead_GetDailyData.connect(self.appData.worker_DBAccess.msgprc_OnDBRead_GetDailyData)
        #self.signal_DBRead_TblReportT1.connect(self.appData.worker_DBAccess.msgprc_OnDBRead_TblReportT1)
        #self.signal_DBRead_TblReportT2.connect(self.appData.worker_DBAccess.msgprc_OnDBRead_TblReportT2)

        self.signal_TickUpdate.connect(self.appData.widget_TabPaneMain.msgprc_OnTickUpdate)

        self.signal_EndOfShift.connect(self.msgprc_OnEndOfShift)
        self.signal_EndOfDay.connect(self.msgprc_OnEndOfDay)
        self.signal_EndOfMonth.connect(self.msgprc_OnEndOfMonth)
        self.signal_EndOfYear.connect(self.msgprc_OnEndOfYear)


    ####################################################################################################################

    def getDateTimeFromByteArray(self, arr_data, arr_pos):

        pos = arr_pos

        next_byte = arr_data.Body[pos]
        pos += 1
        year = 2000 + ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        month = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        day = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        hour = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        minute = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        second = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        next_byte = arr_data.Body[pos]
        pos += 1
        millisecond = ( ( next_byte & 0xF0 ) >> 4 ) * 100 + ( next_byte & 0x0F ) * 10
        next_byte = arr_data.Body[pos]
        pos += 1
        millisecond = millisecond + (( next_byte & 0xF0 ) >> 4)
        day_of_week = next_byte & 0x0F

        _date = QDate(year, month, day)
        _time = QTime(hour, minute, second, millisecond)

        return QDateTime(_date,_time)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnMainCycle(self):      # это получается main cycle

        print("--начало argate_mcycle--" + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))

        now = QDateTime.currentDateTime()
        date = now.date()
        #date = QDateTime(QDate(2021, 3, 25), QDateTime.currentDateTime().time()).date()  # __DEBUG__
        time = now.time()
        self.appData.CD.time = time

        # self.appData.CD.month = date.month()
        # self.appData.CD.year = date.year()

        new_shift = False
        new_day = False
        new_month = False # (!!!!)
        new_year = False  # (!!!!)

        if date != self.appData.CD.date:    # new day has come

            new_day = True

            #self.appData.CD.day_Z1 = self.appData.CD.day
            #self.appData.CD.day_big_Z1 = self.appData.CD.day_big

            self.appData.CD.date = date
            self.signal_DBRead_GetDailyData.emit(date)

        # find out what shift is now - permanent check @0.5s

        found = False

        for shift in self.appData.CD.SHIFTS:

            #if( shift.b_time < shift.e_time and( time >= shift.b_time and time < shift.e_time ))or( shift.b_time > shift.e_time and( time >= shift.b_time or time > shift.e_time )):

            if (shift.b_time < shift.e_time and (time >= shift.b_time and time < shift.e_time)) or (
                    shift.b_time > shift.e_time and (time >= shift.b_time or time < shift.e_time)):

                if self.appData.CD.shift != shift.shift_id:

                    new_shift = True

                    self.appData.CD.shift_Z1 = self.appData.CD.shift
                    self.appData.CD.shift_big_Z1 = self.appData.CD.shift_big
                    self.appData.CD.shift_w_day_Z1 = self.appData.CD.shift_w_day
                    self.appData.CD.shiftType_Z1 = self.appData.CD.shiftType
                    self.appData.CD.sh_Z1_year = self.appData.CD.sh_Z0_year
                    self.appData.CD.sh_Z1_month = self.appData.CD.sh_Z0_month
                    self.appData.CD.sh_Z1_day = self.appData.CD.sh_Z0_day

                    self.appData.CD.sh_Z0_year = self.appData.CD.year
                    self.appData.CD.sh_Z0_month = self.appData.CD.month
                    self.appData.CD.sh_Z0_day = self.appData.CD.day

                    self.appData.CD.shift = shift.shift_id
                    self.appData.CD.shift_big = shift.shift_big_id
                    self.appData.CD.shift_w_day = shift.shift_number_w_day
                    self.appData.CD.shiftType = shift.shift_type_id
                    #self.appData.CD.shiftPlan = shift.plan
                    self.appData.CD.shiftCaption = shift.shiftCaption
                    #self.appData.CD.shiftPlanCaption = shift.planCaption
                    self.appData.CD.curShiftBTime = shift.b_time
                    self.appData.CD.curShiftETime = shift.e_time
                    self.appData.CD.isNight = shift.isNight
                    #self.appData.CD.isWorkingShift = not self.appData.CD.isWeekend and not self.appData.CD.isHoliday and not shift.isNight

                found = True
                break

        if not found:
            self.appData.CD.shift = 0
            self.appData.CD.shiftCaption = "ошибка!"
        else:
            self.appData.CD.isNight = shift.isNight

        found = False
        is_dinner = False

        #for br in self.appData.CD.scheduledBreaks:
        #
        #    if time >= br.b_time and time < br.e_time:
        #
        #        self.appData.CD.scheduledBreak = br.id
        #        self.appData.CD.isScheduledBreak = True
        #        self.appData.CD.scheduledBreakCaption = br.breakCaption
        #        self.appData.CD.curScheduledBreakBTime = br.b_time
        #        self.appData.CD.curScheduledBreakETime = br.e_time
        #
        #        is_dinner = br.isDinner
        #
        #        found = True
        #        break

        for sh in self.appData.CD.SHIFTS:
            for br in sh.SCHEDULED_BREAKS:
                if time >= br.b_time and time < br.e_time:
                    self.appData.CD.scheduledBreak = br.id
                    self.appData.CD.isScheduledBreak = True
                    self.appData.CD.scheduledBreakCaption = br.breakCaption
                    self.appData.CD.curScheduledBreakBTime = br.b_time
                    self.appData.CD.curScheduledBreakETime = br.e_time

                    is_dinner = br.isDinner

                    found = True
                    break
            if found: break

        if not found:

            self.appData.CD.scheduledBreak = 0
            self.appData.CD.isScheduledBreak = False
            self.appData.CD.scheduledBreakCaption = "--"
            self.appData.CD.curScheduledBreakBTime = QTime(0, 0, 0, 0)
            self.appData.CD.curScheduledBreakETime = QTime(0, 0, 0, 0)

        self.appData.CD.isDinner = is_dinner

        for k, station in enumerate(self.appData.stations):
            self.appData.CD.MT_INFO[k].offline = not( station.DAT.alive )

        #self.appData.stations[0].DAT.alive = True # imitation
        #self.appData.CD.MT_INFO[0].alr_failure = True # imitation

        for mti in self.appData.CD.MT_INFO:
            if mti.offline:
                mti.alr_failure = False
                mti.alr_material = False
                mti.stp_failure = False
                mti.stp_material = False
                mti.stp_process = False
                mti.stp_quality = False
                mti.aux_1 = False
                mti.aux_2 = False

        self.appData.CD.isWorkingDay = not self.appData.CD.isWeekend and not self.appData.CD.isHoliday
        self.appData.CD.isWorkingShift = self.appData.CD.isWorkingDay and not self.appData.CD.isNight
        self.appData.CD.isWorkingTime = self.appData.CD.isWorkingShift and not self.appData.CD.isScheduledBreak

        for mti in self.appData.CD.MT_INFO:
            mti.cf.count_alr_time = self.appData.CD.isWorkingTime or ( not self.appData.CD.isWorkingDay and not mti.offline)
            mti.cf.count_stp_time = self.appData.CD.isWorkingTime or( not self.appData.CD.isWorkingDay and not mti.offline )


        # analyze all field staion signals - permanent check @0.5s

        for station in self.appData.stations:

            for signal in station.DAT.signals:

                # catch start time for QR/QF

                if not signal.Q_Z1 and signal.Q:
                    signal.timeQR_a = now
                    signal.timeQR_s = now
                    signal.timeQR_d = now
                else:
                    if signal.Q_Z1 and not signal.Q:
                        signal.timeQF_a = now
                        signal.timeQF_s = now
                        signal.timeQF_d = now

                if new_shift:
                    signal.timeQR_s = now
                    signal.timeQF_s = now

                    signal.msActiveElapsedTime_s = 0
                    signal.msInactiveElapsedTime_s = 0

                if new_day:
                    signal.timeQR_d = now
                    signal.timeQF_d = now

                # recalculate elapsed times

                if signal.Q:

                    ms1 = now.msecsTo(signal.timeQR_a)
                    signal.msActiveElapsedTime_a = abs(ms1)

                    ms1 = now.msecsTo(signal.timeQR_s)
                    signal.msActiveElapsedTime_s = abs(ms1)

                    ms1 = now.msecsTo(signal.timeQR_d)
                    signal.msActiveElapsedTime_d = abs(ms1)

                    signal.msInactiveElapsedTime_a = 0
                    signal.msInactiveElapsedTime_s = 0
                    signal.msInactiveElapsedTime_d = 0

                else:

                    ms2 = now.msecsTo(signal.timeQF_a)
                    signal.msInactiveElapsedTime_a = abs(ms2)

                    ms2 = now.msecsTo(signal.timeQF_s)
                    signal.msInactiveElapsedTime_s = abs(ms2)

                    ms2 = now.msecsTo(signal.timeQF_d)
                    signal.msInactiveElapsedTime_d = abs(ms2)

                    signal.msActiveElapsedTime_a = 0
                    signal.msActiveElapsedTime_s = 0
                    signal.msActiveElapsedTime_d = 0

                signal.Q_Z1 = signal.Q

        i = 0

        for group in self.appData.statistics.groups:
            for mt in group.mtools:
                j = 0
                for signal in mt.signals:

                    signal.timings_a.msCurActive = self.appData.stations[i].DAT.signals[j].msActiveElapsedTime_a
                    signal.timings_a.msCurInactive = self.appData.stations[i].DAT.signals[j].msInactiveElapsedTime_a

                    signal.timings_s.msCurActive = self.appData.stations[i].DAT.signals[j].msActiveElapsedTime_s
                    signal.timings_s.msCurInactive = self.appData.stations[i].DAT.signals[j].msInactiveElapsedTime_s

                    signal.timings_d.msCurActive = self.appData.stations[i].DAT.signals[j].msActiveElapsedTime_d
                    signal.timings_d.msCurInactive = self.appData.stations[i].DAT.signals[j].msInactiveElapsedTime_d

                    if new_shift:

                        #signal.timings_s.msCurActive = 0
                        #signal.timings_s.msCurInactive = 0
                        #
                        #signal.timings_s.msCurActive_Z1 = 0
                        #signal.timings_s.msCurInactive_Z1 = 0
                        #
                        #signal.timings_s.msActive = 0
                        #signal.timings_s.msInactive = 0

                        signal.timings_s.restart()

                    if new_day:
                        signal.timings_d.restart()


                    ## integration
                    #
                    #da = signal.msCurActive - signal.msCurActive_Z1
                    #di = signal.msCurInactive - signal.msCurInactive_Z1
                    #
                    #if da >= 0:
                    #    signal.msActive += da
                    #if di >= 0:
                    #    signal.msInactive += di
                    #
                    #signal.msCurActive_Z1 = signal.msCurActive
                    #signal.msCurInactive_Z1 = signal.msCurInactive

                    signal.tickUpdate()
                    j += 1

                mt.tickUpdate()
                i += 1

            group.tickUpdate()

        dummy = 0

        print(self.appData.statistics.groups[0].mtools[0].signals[0].timings_s.msCurActive)
        print(self.appData.statistics.groups[0].mtools[0].signals[0].timings_s.msCurActive_Z1)
        print(self.appData.statistics.groups[0].mtools[0].signals[0].timings_s.msActive)
        print("---")

        # check for times to write stat to DB (once per shift, once per day)
        # and issue relative signals

        # -- SCHEDULED SIGNALS --
        # пока для теста - хочу выдавать сигнал каждые 10 мин

        now_mmm = date.month()
        now_dd = date.day()
        days_in_current_month = date.daysInMonth()

        now_hh = time.hour()
        now_mm = time.minute()
        now_ss = time.second()
        now_ms = time.msec()

        #self.end_of_day.IN = (now_hh == 23 and now_mm == 30) # (!!!)
        #self.end_of_day.update()
        #
        #if self.end_of_day.QR:
        #    self.signal_EndOfDay.emit() # (!!!)



        print("--завершение argate_mcycle--" + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))

        # make signals to write data into <tbl_period_stat>

        #x1 = self.appData.CD.curShiftETime.hour()
        #x2 = self.appData.CD.curShiftETime.minute()
        #x3 = self.appData.CD.curShiftETime.second()

        self.end_of_shift_A.IN = ( now_hh == self.appData.CD.curShiftBTime.hour() and
                                   now_mm == self.appData.CD.curShiftBTime.minute() and
                                   now_ss == self.appData.CD.curShiftBTime.second())
        #self.end_of_shift_A.IN = new_shift   - так нельзя, т.к. при запуске программы пытается сгенерить отчёт
        self.end_of_shift_A.update()

        self.end_of_day_A.IN = ( now_hh == self.appData.settings.dailyReportTime.hour() and
                                 now_mm == self.appData.settings.dailyReportTime.minute() and
                                 now_ss == self.appData.settings.dailyReportTime.second())
        self.end_of_day_A.update()

        self.end_of_month_A.IN = ( now_dd == days_in_current_month and
                                   now_hh == self.appData.settings.monthReportTime.hour() and
                                   now_mm == self.appData.settings.monthReportTime.minute() and
                                   now_ss == self.appData.settings.monthReportTime.second())
        self.end_of_month_A.update()

        self.end_of_year_A.IN = ( now_mmm == 12 and now_dd == 31 and
                                  now_hh == self.appData.settings.yearReportTime.hour() and
                                  now_mm == self.appData.settings.yearReportTime.minute() and
                                  now_ss == self.appData.settings.yearReportTime.second())
        self.end_of_year_A.update()




        if self.end_of_shift_A.QR:
            self.signal_EndOfShift.emit()   # self.msgprc_OnEndOfShift()
        if self.end_of_day_A.QR:
            self.signal_EndOfDay.emit()
        if self.end_of_month_A.QR:
            self.signal_EndOfMonth.emit()
        if self.end_of_year_A.QR:
            self.signal_EndOfYear.emit()




        # update table view

        self.signal_TickUpdate.emit() # переименовать ! это просто update информации в окне



    ####################################################################################################################

    @pyqtSlot(int)
    def msgprc_OnFieldDataReady(self, mt_id):   # is called after field_io_connector finishes
                                                # reading data from field I/O

        station = self.appData.stations[mt_id - 1]

        arr_data = station.DAT.rawSourceArray

        fake = 0

        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # year = 2000 + ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # month = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # day = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # hour = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # minute = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # second = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # millisecond = ( ( next_byte & 0xF0 ) >> 4 ) * 100 + ( next_byte & 0x0F ) * 10
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # millisecond = millisecond + (( next_byte & 0xF0 ) >> 4)
        # day_of_week = next_byte & 0x0F
        #
        # _date = QDate(year, month, day)
        # _time = QTime(hour, minute, second, millisecond)
        # station.DAT.buttons[0].QR_Time = QDateTime(_date,_time)

        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # year = 2000 + ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # month = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # day = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # hour = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # minute = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # second = ( ( next_byte & 0xF0 ) >> 4 ) * 10 + ( next_byte & 0x0F )
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # millisecond = ( ( next_byte & 0xF0 ) >> 4 ) * 100 + ( next_byte & 0x0F ) * 10
        # next_byte = arr_data[0].Body[pos]
        # pos += 1
        # millisecond = millisecond + (( next_byte & 0xF0 ) >> 4)
        # day_of_week = next_byte & 0x0F
        #
        # _date = QDate(year, month, day)
        # _time = QTime(hour, minute, second, millisecond)
        # station.DAT.buttons[0].QF_Time = QDateTime(_date,_time)

        """
        i = 0

        for sgn in station.DAT.signals:     # при условии, что данные по кнопкам в ПЛК
                                            # лежат в том же порядке, как и в списке в классе UDT_FIELD_STATION

            pos = 0

            sgn.Q = arr_data[i].Body[pos]
            pos += 1
            sgn.QR_E = arr_data[i].Body[pos]
            pos += 5
            sgn.QR_Time = self.getDateTimeFromByteArray(arr_data[i], pos)
            pos += 8
            sgn.QR_F = arr_data[i].Body[pos]
            pos += 5
            sgn.QF_Time = self.getDateTimeFromByteArray(arr_data[i], pos)

            i += 1
        """

        # тут вопрос: что, будем делать отдельный "сигнал" - нет связи??
        # если мы хотим считать время, то видимо надо делать (!) :-(
        # либо же время простоя считать по какому то другому алгоритму??

        #self.appData.CD.arrMachineToolInfo[mt_id - 1].alr_failure = arr_data & (1 << 0)
        #self.appData.CD.arrMachineToolInfo[mt_id - 1].alr_material = arr_data & (1 << 1)

        self.appData.CD.MT_INFO[mt_id - 1].offline = not( self.appData.stations[mt_id - 1].DAT.alive )
        # в другое место, т.к. эта функция не вызывается если нет связи

        # а "кнопочные" сигналы апдейтим как раз только если есть связь

        self.appData.stations[mt_id - 1].DAT.signals[0].Q = ( arr_data & (1 << 0)) == 1
        self.appData.stations[mt_id - 1].DAT.signals[1].Q = ( arr_data & (1 << 1)) == 2
        self.appData.stations[mt_id - 1].DAT.signals[2].Q = ( arr_data & (1 << 2)) == 4
        self.appData.stations[mt_id - 1].DAT.signals[3].Q = ( arr_data & (1 << 3)) == 8
        self.appData.stations[mt_id - 1].DAT.signals[4].Q = ( arr_data & (1 << 4)) == 16
        self.appData.stations[mt_id - 1].DAT.signals[5].Q = ( arr_data & (1 << 5)) == 32
        self.appData.stations[mt_id - 1].DAT.signals[6].Q = ( arr_data & (1 << 6)) == 64
        self.appData.stations[mt_id - 1].DAT.signals[7].Q = ( arr_data & (1 << 7)) == 128

        self.appData.CD.MT_INFO[mt_id - 1].alr_failure = self.appData.stations[mt_id - 1].DAT.signals[0].Q
        self.appData.CD.MT_INFO[mt_id - 1].alr_material = self.appData.stations[mt_id - 1].DAT.signals[1].Q
        self.appData.CD.MT_INFO[mt_id - 1].stp_failure = self.appData.stations[mt_id - 1].DAT.signals[2].Q
        self.appData.CD.MT_INFO[mt_id - 1].stp_material = self.appData.stations[mt_id - 1].DAT.signals[3].Q
        self.appData.CD.MT_INFO[mt_id - 1].stp_process = self.appData.stations[mt_id - 1].DAT.signals[4].Q
        self.appData.CD.MT_INFO[mt_id - 1].stp_quality = self.appData.stations[mt_id - 1].DAT.signals[5].Q
        self.appData.CD.MT_INFO[mt_id - 1].aux_1 = self.appData.stations[mt_id - 1].DAT.signals[6].Q
        self.appData.CD.MT_INFO[mt_id - 1].aux_2 = self.appData.stations[mt_id - 1].DAT.signals[7].Q


        dummy = 0

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnPrepareDataForDB(self):

        print("подготовка данных")
        """
        for station in self.appData.stations:

            mt_id = station.PAR.id

            self.prepareDbData(mt_id) # эта функция считывает DateTime из ПК
            station.DAT.sqlstr_StatesHistory = self.convertDbDataToSqlString(mt_id)





        """
        self.signal_DBWrite_CyclicData.emit()


    ####################################################################################################################
    """
    def prepareDbData(self, mt_id):    # это по каждой станции

        station = self.appData.stations[mt_id - 1]

        for record in station.DAT.statesHistoryData:

            record.rec_time = QDateTime.currentDateTime()   # в БД пишется время из ПК
            record.fk_machine_tool_id = mt_id
            record.fk_event_hrec_id = 0
            record.fk_shift_id = self.appData.CD.shift

            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_ALARM_ON_FAILURE:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE - 1].Q == True)
            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_ALARM_ON_MATERIAL:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL - 1].Q == True)
            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_STOP_ON_FAILURE:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE - 1].Q == True)
            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_STOP_ON_MATERIAL:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL - 1].Q == True)
            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_STOP_ON_PROCESS:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS - 1].Q == True)
            if record.fk_state_type_id == ENM_STATE_TYPES.BUTTON_STOP_ON_QUALITY:
                record.state_value = int(station.DAT.signals[ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY - 1].Q == True)
    """
    ####################################################################################################################
    """
    def convertDbDataToSqlString(self, mt_id):

        station = self.appData.stations[mt_id - 1]

        # это по каждой станции и по каждому state_type_id отдельно

        for record in station.DAT.statesHistoryData:    # list of DBREC_STATES_HISTORY()

            record.MakeStatesHistoryRec()

        # и теперь "общая полная запись"

        s = "INSERT INTO tbl_states_history(rec_time, fk_machine_tool_id, fk_state_type_id, state_value, "
        s += "fk_event_hrec_id, fk_shift_id, b_time, fk_b_shift_id,c_time_full,c_time_w_shift,c_time_w_day) "
        s += "VALUES "

        for record in station.DAT.statesHistoryData:

            s += record.sql_str_1
            s += ","

        s = s[0:(len(s)-1)] + ";"

        #station.DAT.fullSqlRequest = s
        return s
    """
    ####################################################################################################################

    #@pyqtSlot()
    #def msgprc_OnProcessDailyData(self):
    #
    #    self.appData.CD.day = self.appData.DBD.day_id
    #    self.appData.CD.day_big = self.appData.DBD.day_big_id
    #    self.appData.CD.month = self.appData.DBD.month_id
    #    self.appData.CD.year = self.appData.DBD.year_id
    #    #if self.appData.DBD.weekday == 0:   # sunday (from DB)
    #    #    self.appData.CD.weekday = ENM_WEEKDAYS.SUNDAY
    #    #else:
    #    #    self.appData.CD.weekday = self.appData.DBD.weekday
    #    self.appData.CD.weekday = self.appData.DBD.weekday
    #    #self.appData.CD.isWeekend = self.appData.isWeekend(self.appData.CD.weekday) !!!
    #    self.appData.CD.isWeekend = self.appData.DBD.isWeekend
    #    self.appData.CD.weekendDay = self.appData.DBD.weekendDay
    #    self.appData.CD.isHoliday = self.appData.DBD.isHoliday
    #    self.appData.CD.holiday = self.appData.DBD.holiday
    #    self.appData.CD.isDayout = self.appData.DBD.isDayout
    #    self.appData.CD.dayout = self.appData.DBD.dayout
    #
    #    self.appData.CD.shifts = self.appData.DBD.shifts
    #    self.appData.CD.scheduledBreaks = self.appData.DBD.scheduledBreaks
    #
    #    print("ежедневные данные получены")


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnEndOfShift(self):

        self.appData.window_MainWindow.signal_DBWrite_WrShiftStat.emit()    # -> worker_DBAccess.msgprc_OnDBWriteWrShiftStat

        if self.appData.CD.shift_w_day == 1:
            self.appData.window_MainWindow.signal_RequestReportType2.emit(True,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

        #if self.appData.eod_GEN_REP_SEQ_STATE == 0 and self.appData.eos_GEN_REP_SEQ_STATE == 0:
        #    self.appData.eos_GEN_REP_SEQ_STATE = 2 # WAIT for the data is written to DB

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnEndOfDay(self):

        # prepare data for DB
        """
        for station in self.appData.stations:

            station.DAT.sqlstr_StatByMT = SQL_REQUESTS.sqlreq_DBWrite_TblStatByMt(self.appData, station)

        # data is ready - can write to DB

        self.signal_DBWrite_EODayData.emit()
        """
        self.appData.window_MainWindow.signal_DBWrite_WrDailyStat.emit()    # -> worker_DBAccess.msgprc_OnDBWriteWrDailyStat

        #if self.appData.eod_GEN_REP_SEQ_STATE == 0:
        #    if self.appData.eos_GEN_REP_SEQ_STATE == 0: # have to WAIT until REPORT_T2 is generated
        #        self.appData.eod_GEN_REP_SEQ_STATE = 2  # WAIT for the data is written to DB
        #    else:
        #        self.appData.eod_GEN_REP_SEQ_STATE = 1  # WAIT for REPORT_T2

        self.appData.window_MainWindow.signal_RequestReportType1.emit(True,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnEndOfMonth(self):

        self.appData.window_MainWindow.signal_DBWrite_WrMonthStat.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnEndOfYear(self):

        self.appData.window_MainWindow.signal_DBWrite_WrYearStat.emit()

    ####################################################################################################################

    #pyqtSlot()
    #ef msgprc_OnMakeReport_EODay(self):
    #
    #   pythoncom.CoInitialize()    # !!!!!!!!!!!!!!!!
    #
    #   excelapp = win32com.client.Dispatch("Excel.Application")
    #   #excelapp = win32com.client.gencache.EnsureDispatch("Excel.Application")
    #   excelapp.Visible = True
    #
    #   workbook = excelapp.Workbooks.Add(1)
    #   sheet = workbook.Sheets(1)
    #
    #   excelapp.ActiveWindow.Zoom = 80
    #   excelapp.ActiveWindow.DisplayGridlines = False
    #
    #   #sheet.Range("A10").Interior.Color = GF.rgbToExcelColor(255, 0, 0)
    #   #sheet.Range("B10").Interior.Color = GF.rgbToExcelColor(0, 255, 0)
    #   #sheet.Range("C10").Interior.Color = GF.rgbToExcelColor(0, 0, 255)
    #
    #
    #   sheet.Range("B4:G4").Interior.Color = GF.rgbToExcelColor(220, 220, 220)
    #
    #   sheet.Range("B4").Value = "№"
    #   sheet.Range("C4").Value = "Номер"
    #   sheet.Range("D4").Value = "Название"
    #   sheet.Range("E4").Value = "Класс"
    #   sheet.Range("F4").Value = "Авария"
    #   sheet.Range("G4").Value = "Причина"
    #
    #   record_number = len(self.appData.tbl_stat_mt_report)
    #   rec = self.appData.tbl_stat_mt_report[0]
    #
    #   first_date = rec.the_date
    #
    #   # перебираем таблицу, пока не поймаем следующую дату, при этом считаем количество станков
    #   # и составляем структуру, т.е. какие станки, классы и т.п.
    #
    #   # сделать тест, чтобы по кнопке считтывалась таблица из БД
    #   # собственно, это нужно - кнопка "Сгенерить вечерний отчет"
    #   # кнопка - отправить отчёт по email
    #
    #   #т.е. в любом случае, отчёт должен генериться как по scheduled так и принудительно по кнопке
    #   #кстати, ещё и в конце каждой смены
    #
    #
    #
    #
    #
    #
    #
    #   dummy = 0

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRequestReportType1(self):

        self.signal_DBRead_TblReportT1.emit(0)   # -> UDT_DB_CONNECTOR.msgprc_OnDBRead_TblReportT1()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRequestAndSendReportType1(self):

        self.signal_DBRead_TblReportT1.emit(1)   # -> UDT_DB_CONNECTOR.msgprc_OnDBRead_TblReportT1()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRequestReportType2(self):

        # 1. Prepare for requesting data

        #self.appData.sql_strings.dbRead_MachineToolsFullList = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList()
        #self.appData.sql_strings.dbRead_TableReportType2 = SQL_REQUESTS.sqlreq_DBRead_TblStatByMT(self.appData)

        # 2. Emit request data from DB

        self.signal_DBRead_TblReportT2.emit(0)   # -> UDT_DB_CONNECTOR.msgprc_OnDBRead_TblReportT2()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRequestAndSendReportType2(self):

        # 1. Prepare for requesting data

        #self.appData.sql_strings.dbRead_MachineToolsFullList = SQL_REQUESTS.sqlreq_DBRead_GetFullMachineToolsList()
        #self.appData.sql_strings.dbRead_TableReportType2 = SQL_REQUESTS.sqlreq_DBRead_TblStatByMT()

        # 2. Emit request data from DB

        self.signal_DBRead_TblReportT2.emit(1)   # -> UDT_DB_CONNECTOR.msgprc_OnDBRead_TblReportT2()

    ####################################################################################################################

    #@pyqtSlot()
    #def msgprc_OnGenerateReportType2(self):
    #
    #    EXPORTER.exportToExcel_ReportType2(self.appData)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionSuccess(self):

        self.appData.dbConnected = True

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionFailure(self):

        self.appData.dbConnected = False

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnInitialDataReadDone(self, success):

        if success:
            pass
        else:
            pass

    ####################################################################################################################