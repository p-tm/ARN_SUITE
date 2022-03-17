########################################################################################################################

from copy import copy

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal


########################################################################################################################
# описание класса:
# - просто раздаёт сигналы таймера, по которым производится
#   опрос узлов и опрос данных
########################################################################################################################

class UDT_ARBMON_DISPATCHER(QObject):

    signal_StartExt = pyqtSignal()  # for tests only
    signal_StartExt2 = pyqtSignal() # for tests onl

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.timer_MainCycle = QTimer()
        self.timer_MainCycle.setTimerType(Qt.PreciseTimer)
        self.timer_MainCycle.setInterval(200)   # с этой периодичностью производится main_cycle а также обновление окон (!)
        self.timer_MainCycle.start()
        self.timer_MainCycle.timeout.connect(self.appData.worker_MCycle.msgprc_OnMainCycle)

        #QTimer.singleShot(200, self.shot)

        self.timer_GetRTData = QTimer()
        self.timer_GetRTData.setTimerType(Qt.PreciseTimer)
        self.timer_GetRTData.setInterval(500)   # обращение к БД 2 р/сек - чаще думаю нельзя
        self.timer_GetRTData.start()
        self.timer_GetRTData.timeout.connect(self.appData.worker_DBAccess.msgprc_GetRTData)

        #QTimer.singleShot(500, self.shot2)

        self.ms_CHANGE_ALARM_WIDGET = self.appData.settings.ms_CHANGE_ALARM_WIDGET

        self.timer_ChangeAlarmWidget = QTimer()
        self.timer_ChangeAlarmWidget.setInterval(self.ms_CHANGE_ALARM_WIDGET)
        self.timer_ChangeAlarmWidget.start()
        self.timer_ChangeAlarmWidget.timeout.connect(self.appData.worker_MCycle.msgprc_OnChangeAlarmWidget)

        self.ms_RUNNING_CAPTION_TICK = self.appData.settings.ms_RUNNING_CAPTION_TICK

        self.timer_RunningCaption = QTimer()
        self.timer_RunningCaption.setTimerType(Qt.PreciseTimer)
        self.timer_RunningCaption.setInterval(self.ms_RUNNING_CAPTION_TICK)
        self.timer_RunningCaption.start()
        self.timer_RunningCaption.timeout.connect(self.appData.worker_MCycle.msgprc_OnRunningCaptionUpdate)

        #self.ms_SHOW_WORKSHOP = self.appData.settings.ms_SHOW_WORKSHOP
        #self.ms_SHOW_DIAGRAMS = self.appData.settings.ms_SHOW_DIAGRAMS

        #self.time_ChangeScreen = QTimer()
        #self.time_ChangeScreen.setSingleShot(True)
        #self.time_ChangeScreen.setInterval(self.ms_SHOW_WORKSHOP)
        #self.time_ChangeScreen.start()
        #self.time_ChangeScreen.timeout.connect(self.appData.worker_MCycle.msgprc_OnChangeScreen)
        QTimer.singleShot(self.appData.settings.ms_SHOW_WORKSHOP,self.appData.worker_MCycle.msgprc_OnChangeScreen)

        self.timer_GetSettingsCycle = QTimer()
        self.timer_GetSettingsCycle.setInterval(10000)   # с этой периодичностью производится считавание настроек из БД
        self.timer_GetSettingsCycle.start()
        self.timer_GetSettingsCycle.timeout.connect(self.appData.worker_DBAccess.msgprc_GetSettings)



        self.signal_StartExt.connect(self.appData.worker_MCycle.msgprc_OnMainCycle)
        self.signal_StartExt2.connect(self.appData.worker_DBAccess.msgprc_GetRTData)



    ####################################################################################################################

    @pyqtSlot(int)
    def msgprc_OnScreenChanged(self, scr):

        if scr == 1:
            #self.time_ChangeScreen = QTimer()
            #self.time_ChangeScreen.setSingleShot(True)
            #self.time_ChangeScreen.setInterval(self.ms_SHOW_WORKSHOP)
            #self.time_ChangeScreen.start()
            #self.time_ChangeScreen.timeout.connect(self.appData.worker_MCycle.msgprc_OnChangeScreen)
            QTimer.singleShot(self.appData.settings.ms_SHOW_WORKSHOP,self.appData.worker_MCycle.msgprc_OnChangeScreen)

        if scr == 2:
            #self.time_ChangeScreen = QTimer()
            #self.time_ChangeScreen.setSingleShot(True)
            #self.time_ChangeScreen.setInterval(self.ms_SHOW_WORKSHOP)
            #self.time_ChangeScreen.start()
            #self.time_ChangeScreen.timeout.connect(self.appData.worker_MCycle.msgprc_OnChangeScreen)
            QTimer.singleShot(self.appData.settings.ms_SHOW_DIAGRAMS,self.appData.worker_MCycle.msgprc_OnChangeScreen)
                                                                                                      
    ####################################################################################################################

    @pyqtSlot()
    def shot(self):

        QTimer.singleShot(200, self.shot)

        self.signal_StartExt.emit()

    @pyqtSlot()
    def shot2(self):

        QTimer.singleShot(500, self.shot2)

        self.signal_StartExt2.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRestartTimers(self):

        self.ms_RUNNING_CAPTION_TICK = self.appData.settings.ms_RUNNING_CAPTION_TICK

        self.timer_RunningCaption = QTimer()
        self.timer_RunningCaption.setTimerType(Qt.PreciseTimer)
        self.timer_RunningCaption.setInterval(self.ms_RUNNING_CAPTION_TICK)
        self.timer_RunningCaption.timeout.connect(self.appData.worker_MCycle.msgprc_OnRunningCaptionUpdate)
        self.timer_RunningCaption.start()

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnSettingsRead(self):

        if self.appData.settings_Z1.ms_RUNNING_CAPTION_TICK != self.appData.settings.ms_RUNNING_CAPTION_TICK:
            self.appData.window_MainWindow.signal_RestartTimerRunningCaption.emit()
        if self.appData.settings_Z1.ms_CHANGE_ALARM_WIDGET != self.appData.settings.ms_CHANGE_ALARM_WIDGET:
            self.appData.window_MainWindow.signal_RestartTimerAlarmWidgets.emit()

        self.appData.settings_Z1 = copy(self.appData.settings)


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRestartTimerRunningCaption(self):

        self.ms_RUNNING_CAPTION_TICK = self.appData.settings.ms_RUNNING_CAPTION_TICK

        self.timer_RunningCaption = QTimer()
        self.timer_RunningCaption.setTimerType(Qt.PreciseTimer)
        self.timer_RunningCaption.setInterval(self.ms_RUNNING_CAPTION_TICK)
        self.timer_RunningCaption.timeout.connect(self.appData.worker_MCycle.msgprc_OnRunningCaptionUpdate)
        self.timer_RunningCaption.start()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRestartTimerAlarmWidgets(self):

        self.ms_CHANGE_ALARM_WIDGET = self.appData.settings.ms_CHANGE_ALARM_WIDGET

        self.timer_ChangeAlarmWidget = QTimer()
        self.timer_ChangeAlarmWidget.setInterval(self.ms_CHANGE_ALARM_WIDGET)
        self.timer_ChangeAlarmWidget.timeout.connect(self.appData.worker_MCycle.msgprc_OnChangeAlarmWidget)
        self.timer_ChangeAlarmWidget.start()

    ####################################################################################################################



