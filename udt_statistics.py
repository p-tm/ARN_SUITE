########################################################################################################################

from PyQt5.QtCore import QDateTime, QTime

########################################################################################################################

from enums import *

########################################################################################################################
# описание класса:
# - это кумулятивное время по каждому конкретному сигналу
########################################################################################################################

class UDT_SIGNAL_STAT():

    class TIMINGS():

        def __init__(self):

            self.msCurActive = 0            # текущее состояние
            self.msCurInactive = 0          # текущее состояние

            self.msCurActive_Z1 = 0
            self.msCurInactive_Z1 = 0

            self.msActive = 0               # кумулятивное время за период
            self.msInactive = 0             # кумулятивное время за период

            self.timeActive = QTime()       # кумулятивное время за период
            self.timeInactive = QTime()     # кумулятивное время за период

        def tickUpdate(self):

            # integration

            #сюда добваить ???
            #интегрируем только если рабочий день, и рабочая смена, и не штатный перерыв ???
            #
            #а мы что-то обсуждали такое, что если в нерабочий день станок включен, но нажата кнопка - то тоже
            #считаем простой
            #
            #т.е.
            #
            #- если в рабочий день станок просто влкючен - это норма
            #- если в рабочий день станок отключен - это простой
            #- если в нерабочее время (ночью) станок выключен - это норма
            #
            #т.е. получается так:
            #- в нерабочее время станок должен быть выключен - это норма
            #- если в нерабочее время станок включен - то считается что он работает
            #и нажатые кнопки означают простой
            #т.е. разница получается только если станок выключен (offline)
            #- если выключен в рабочее время - это простой
            #- если выключен в нерабочее время - это норма

            da = self.msCurActive - self.msCurActive_Z1
            di = self.msCurInactive - self.msCurInactive_Z1

            if da >= 0:
                self.msActive += da
            if di >= 0:
                self.msInactive += di

            self.msCurActive_Z1 = self.msCurActive
            self.msCurInactive_Z1 = self.msCurInactive

        def restart(self):

            self.msCurActive = 0
            self.msCurInactive = 0

            self.msCurActive_Z1 = 0
            self.msCurInactive_Z1 = 0

            self.msActive = 0
            self.msInactive = 0


    def __init__(self, sgn_id):

        self.id = sgn_id
        self.isAlarm = False
        self.isStop = False
        self.isOutOfOperation = False

        self.timings_a = self.TIMINGS()      # absolute (type = 1)
        self.timings_s = self.TIMINGS()      # relative to current shift (type = 2)
        self.timings_d = self.TIMINGS()      # relative to current day (type = 3)

        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE:
            self.isAlarm = True
            self.isStop = False
            self.isOutOfOperation = False
        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL:
            self.isAlarm = True
            self.isStop = False
            self.isOutOfOperation = False
        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE:
            self.isAlarm = False
            self.isStop = True
            self.isOutOfOperation = True
        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL:
            self.isAlarm = False
            self.isStop = True
            self.isOutOfOperation = True
        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS:
            self.isAlarm = False
            self.isStop = True
            self.isOutOfOperation = True
        if self.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY:
            self.isAlarm = False
            self.isStop = True
            self.isOutOfOperation = True


        # ???
        # if self.id == ENM_FIELD_STATION_SIGNALS.STATE_OFFLINE:
        #    self.isAlarm = False
        #    self.isStop = True
        #    self.isOutOfOperation = True

        #!!!! вот, что забыл
        #простои не считаются простоями, если сейчас
        #- нерабочая смена
        #- или штатный перерыв

    ####################################################################################################################

    def tickUpdate(self):

        # integration
        #
        #da = self.msCurActive - self.msCurActive_Z1
        #di = self.msCurInactive - self.msCurInactive_Z1
        #
        #if da >= 0:
        #    self.msActive += da
        #if di >= 0:
        #    self.msInactive += di
        #
        #self.msCurActive_Z1 = self.msCurActive
        #self.msCurInactive_Z1 = self.msCurInactive

        self.timings_a.tickUpdate()
        self.timings_s.tickUpdate()
        self.timings_d.tickUpdate()


########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_MT_STAT():

    class CUMULATIVE_TIME():

        def __init__(self, type):

            self.type = type    # 1 = aboslut, 2 = within shift, 3 = within day

            self.msAlarmOnFailure = 0
            self.msAlarmOnMaterial = 0
            self.msStopOnFailure = 0
            self.msStopOnMaterial = 0
            self.msStopOnProcess = 0
            self.msStopOnQuality = 0

            self.msAlarm = 0
            self.msStop = 0
            self.msOutOfOperation = 0

            self.timeAlarm = 0
            self.timeStop = 0
            self.timeOutOfOperation = 0


        def tickUpdate(self, parent):

            ms_time_alarm = 0
            ms_time_stop = 0
            ms_time_out_of_operation = 0

            for signal in parent.signals:

                if signal.isAlarm:
                    if self.type == 1:
                        ms_time_alarm += signal.timings_a.msActive
                    if self.type == 2:
                        ms_time_alarm += signal.timings_s.msActive
                    if self.type == 3:
                        ms_time_alarm += signal.timings_d.msActive

                if signal.isStop:
                    if self.type == 1:
                        ms_time_stop += signal.timings_a.msActive
                    if self.type == 2:
                        ms_time_stop += signal.timings_s.msActive
                    if self.type == 3:
                        ms_time_stop += signal.timings_d.msActive

                if signal.isOutOfOperation:
                    if self.type == 1:
                        ms_time_out_of_operation += signal.timings_a.msActive
                    if self.type == 2:
                        ms_time_out_of_operation += signal.timings_s.msActive
                    if self.type == 3:
                        ms_time_out_of_operation += signal.timings_d.msActive

            if self.type == 1:
                self.msAlarmOnFailure = parent.signals[0].timings_a.msActive
            if self.type == 2:
                self.msAlarmOnFailure = parent.signals[0].timings_s.msActive
            if self.type == 3:
                self.msAlarmOnFailure = parent.signals[0].timings_d.msActive

            if self.type == 1:
                self.msAlarmOnMaterial = parent.signals[1].timings_a.msActive
            if self.type == 2:
                self.msAlarmOnMaterial = parent.signals[1].timings_s.msActive
            if self.type == 3:
                self.msAlarmOnMaterial = parent.signals[1].timings_d.msActive

            if self.type == 1:
                self.msStopOnFailure = parent.signals[2].timings_a.msActive
            if self.type == 2:
                self.msStopOnFailure = parent.signals[2].timings_s.msActive
            if self.type == 3:
                self.msStopOnFailure = parent.signals[2].timings_d.msActive

            if self.type == 1:
                self.msStopOnMaterial = parent.signals[3].timings_a.msActive
            if self.type == 2:
                self.msStopOnMaterial = parent.signals[3].timings_s.msActive
            if self.type == 3:
                self.msStopOnMaterial = parent.signals[3].timings_d.msActive

            if self.type == 1:
                self.msStopOnProcess = parent.signals[4].timings_a.msActive
            if self.type == 2:
                self.msStopOnProcess = parent.signals[4].timings_s.msActive
            if self.type == 3:
                self.msStopOnProcess = parent.signals[4].timings_d.msActive

            if self.type == 1:
                self.msStopOnQuality = parent.signals[5].timings_a.msActive
            if self.type == 2:
                self.msStopOnQuality = parent.signals[5].timings_s.msActive
            if self.type == 3:
                self.msStopOnQuality = parent.signals[5].timings_d.msActive

            self.msAlarm = ms_time_alarm        # кумулятивное время состояния "Тревога"
            self.msStop = ms_time_stop          # кумулятивное время состояния "Остановка"
            self.msOutOfOperation = ms_time_out_of_operation    # кумулятивное время - станок offline


    def __init__(self, mt_id):

        self.id = mt_id

        self.signals = list([])

        if self.id == ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY:
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY))
        if self.id == ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN:
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS))
            self.signals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY))

        self.cumulative_time_a = self.CUMULATIVE_TIME(1)    # absolute
        self.cumulative_time_s = self.CUMULATIVE_TIME(2)    # shift
        self.cumulative_time_d = self.CUMULATIVE_TIME(3)    # day

    ####################################################################################################################

    def tickUpdate(self):

        self.cumulative_time_a.tickUpdate(self)
        self.cumulative_time_s.tickUpdate(self)
        self.cumulative_time_d.tickUpdate(self)



########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_MTCLASS_STAT():

    class CUMULATIVE_TIME():

        def __init__(self, type):

            self.type = type

            self.msAlarmOnFailure = 0
            self.msAlarmOnMaterial = 0
            self.msStopOnFailure = 0
            self.msStopOnMaterial = 0
            self.msStopOnProcess = 0
            self.msStopOnQuality = 0

            self.msAlarm = 0
            self.msStop = 0
            self.msOutOfOperation = 0

        def tickUpdate(self, parent):

            ms_alarm_on_failure = 0
            ms_alarm_on_material = 0
            ms_stop_on_failure = 0
            ms_stop_on_material = 0
            ms_stop_on_process = 0
            ms_stop_on_quality = 0

            ms_alarm = 0
            ms_stop = 0
            ms_out_of_operation = 0

            for mt in parent.mtools:

                for signal in mt.signals:

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE:
                        if self.type == 1:
                            ms_alarm_on_failure += signal.timings_a.msActive
                        if self.type == 2:
                            ms_alarm_on_failure += signal.timings_s.msActive
                        if self.type == 3:
                            ms_alarm_on_failure += signal.timings_d.msActive

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL:
                        if self.type == 1:
                            ms_alarm_on_material += signal.timings_a.msActive
                        if self.type == 2:
                            ms_alarm_on_material += signal.timings_s.msActive
                        if self.type == 3:
                            ms_alarm_on_material += signal.timings_d.msActive

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE:
                        if self.type == 1:
                            ms_stop_on_failure += signal.timings_a.msActive
                        if self.type == 2:
                            ms_stop_on_failure += signal.timings_s.msActive
                        if self.type == 3:
                            ms_stop_on_failure += signal.timings_d.msActive

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL:
                        if self.type == 1:
                            ms_stop_on_material += signal.timings_a.msActive
                        if self.type == 2:
                            ms_stop_on_material += signal.timings_s.msActive
                        if self.type == 3:
                            ms_stop_on_material += signal.timings_d.msActive

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS:
                        if self.type == 1:
                            ms_stop_on_process += signal.timings_a.msActive
                        if self.type == 2:
                            ms_stop_on_process += signal.timings_s.msActive
                        if self.type == 3:
                            ms_stop_on_process += signal.timings_d.msActive

                    if signal.id == ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY:
                        if self.type == 1:
                            ms_stop_on_quality += signal.timings_a.msActive
                        if self.type == 2:
                            ms_stop_on_quality += signal.timings_s.msActive
                        if self.type == 3:
                            ms_stop_on_quality += signal.timings_d.msActive

                if self.type == 1:
                    ms_alarm += mt.cumulative_time_a.msAlarm
                    ms_stop += mt.cumulative_time_a.msStop
                    ms_out_of_operation += mt.cumulative_time_a.msOutOfOperation
                if self.type == 2:
                    ms_alarm += mt.cumulative_time_s.msAlarm
                    ms_stop += mt.cumulative_time_s.msStop
                    ms_out_of_operation += mt.cumulative_time_s.msOutOfOperation
                if self.type == 3:
                    ms_alarm += mt.cumulative_time_d.msAlarm
                    ms_stop += mt.cumulative_time_d.msStop
                    ms_out_of_operation += mt.cumulative_time_d.msOutOfOperation

            self.msAlarmOnFailure = ms_alarm_on_failure
            self.msAlarmOnMaterial = ms_alarm_on_material
            self.msStopOnFailure = ms_stop_on_failure
            self.msStopOnMaterial = ms_stop_on_material
            self.msStopOnProcess = ms_stop_on_process
            self.msStopOnQuality = ms_stop_on_quality

            self.msAlarm = ms_alarm
            self.msStop = ms_stop
            self.msOutOfOperation = ms_out_of_operation


    def __init__(self, class_id):

        self.id = class_id

        self.mtools = list([]) # list<UDT_MT_STAT>

        if self.id == ENM_MACHINE_TOOL_CLASSES.PUNCH:

            self.mtools.append(UDT_MT_STAT(ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY))
            self.mtools.append(UDT_MT_STAT(ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN))

            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_FAILURE))
            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_ALARM_ON_MATERIAL))
            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_FAILURE))
            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_MATERIAL))
            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_PROCESS))
            #self.grouppedSignals.append(UDT_SIGNAL_STAT(ENM_FIELD_STATION_SIGNALS.BUTTON_STOP_ON_QUALITY))

        if self.id == ENM_MACHINE_TOOL_CLASSES.BEND:
            pass

        if self.id == ENM_MACHINE_TOOL_CLASSES.WELD:
            pass

        if self.id == ENM_MACHINE_TOOL_CLASSES.PAINT:
            pass

        self.cumulative_time_a = self.CUMULATIVE_TIME(1)    # absolute
        self.cumulative_time_s = self.CUMULATIVE_TIME(2)    # shift
        self.cumulative_time_d = self.CUMULATIVE_TIME(3)    # day

    ####################################################################################################################

    def tickUpdate(self):

        self.cumulative_time_a.tickUpdate(self)
        self.cumulative_time_s.tickUpdate(self)
        self.cumulative_time_d.tickUpdate(self)



########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_WORKSHOP_STAT():

    def __init__(self):

        self.groups = list([])      # list<UDT_MTCLASS_STAT> - т.е. группы это классы станков

        self.groups.append(UDT_MTCLASS_STAT(ENM_MACHINE_TOOL_CLASSES.PUNCH))
        self.groups.append(UDT_MTCLASS_STAT(ENM_MACHINE_TOOL_CLASSES.BEND))



