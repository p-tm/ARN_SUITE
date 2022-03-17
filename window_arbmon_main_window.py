########################################################################################################################
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSettings


from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget


from PyQt5.QtWidgets import QTabWidget

from PyQt5.QtGui import QCursor

########################################################################################################################

from enums import *
from const import *

from udt_arbmon_dispatcher import UDT_ARBMON_DISPATCHER
from udt_arbmon_db_connector import UDT_ARBMON_DB_CONNECTOR
from udt_arbmon_mcycle_worker import UDT_ARBMON_MCYCLE_WORKER

from widget_arbmon_pane_workshop import WIDGET_ARBMON_PANE_WORKSHOP
from widget_arbmon_pane_diagrams import WIDGET_ARBMON_PANE_DIAGRAMS
from widget_arbmon_pane_alarm import WIDGET_ARBMON_PANE_ALARM
from widget_arbmon_pane_norma import WIDGET_ARBMON_PANE_NORMA

from window_arbmon_nonmodal_msgbox import WINDOW_ARBMON_NONMODAL_MSGBOX

########################################################################################################################

__DEBUG__ = False

########################################################################################################################
# описание класса:
# - Главное окно для утилиты ARBMON
#
########################################################################################################################

class WINDOW_ARBMON_MAIN_WINDOW(QMainWindow):

    #
    signal_UpdateUI = pyqtSignal()
    signal_RestartTimers = pyqtSignal()
    # DB access signals
    signal_DBConnectionSuccess = pyqtSignal()       # ->
    signal_DBConnectionFailure = pyqtSignal()       # ->
    signal_InitialDataReadDone = pyqtSignal(bool)   # ->
    signal_RTDataReadDone = pyqtSignal(bool)        # ->
    signal_SettingsRead = pyqtSignal(bool)          # -> worker_Dispatcher.msgprc_OnSettingsRead()
    signal_RestartTimerRunningCaption = pyqtSignal()    # -> worker_Dispatcher.msgprc_OnRestartTimerRunningCaption()
    signal_RestartTimerAlarmWidgets = pyqtSignal()   # -> worker_Dispatcher.msgprc_OnRestartTimerAlarmPanels()

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        # APP SETTINGS
        # C:\Users\Pavel\AppData\Local\Programs\Python\Python38
        self.appData.settingsFileName = self.appData.str_ResDir + "/arbmon.ini"
        self.appData.settingsKeeper = QSettings(self.appData.settingsFileName, QSettings.IniFormat)

        try:
            self.appData.settings.ms_CHANGE_ALARM_WIDGET = int(self.appData.settingsKeeper.value("s_msChangeAlarmPanel"))
            self.appData.settings.ms_RUNNING_CAPTION_TICK = int(self.appData.settingsKeeper.value("s_msRunningStringStep"))
            self.appData.settings.ms_SHOW_WORKSHOP = int(self.appData.settingsKeeper.value("s_msWorkshopPane"))
            self.appData.settings.ms_SHOW_DIAGRAMS = int(self.appData.settingsKeeper.value("s_msDiagramPane"))
        except:
            pass

        # VARS

        self.widget_CoreWidget = QTabWidget() # QWidget()
        #self.layout_CoreLayout = QVBoxLayout()
        self.setCentralWidget(self.widget_CoreWidget)

        self.tpane_Main = QWidget()
        self.tpane_Diagrams = WIDGET_ARBMON_PANE_DIAGRAMS(self.appData)

        self.widget_CoreWidget.addTab(self.tpane_Main, "pane_Main")
        self.widget_CoreWidget.addTab(self.tpane_Diagrams, "pane_Diagrams")

        self.tpane_Main.setLayout(QVBoxLayout())

        #self.pane_ViewPane = QWidget()
        self.pane_Workshop = WIDGET_ARBMON_PANE_WORKSHOP(self.appData)
        self.pane_AlarmPane = QTabWidget()

        self.tpane_Main.layout().addWidget(self.pane_Workshop)
        self.tpane_Main.layout().addWidget(self.pane_AlarmPane)



        # self.pane_ViewPane

        #self.tpane_Workshop = WIDGET_ARBMON_PANE_WORKSHOP(self.appData)

        #self.pane_ViewPane.setLayout(QVBoxLayout())
        #self.pane_ViewPane.addTab(self.tpane_Workshop, "tpane_Workshop")
        #self.pane_ViewPane.layout().addWidget(self.tpane_Workshop)



        # self.pane_AlarmPane

        #self.tpane_NORMA = WIDGET_ARBMON_PANE_NORMA(self.appData)
        #self.tpane_MT0_ALR_FAILURE = WIDGET_ARBMON_PANE_ALARM(self.appData)
        #self.tpane_MT0_ALR_MATERIAL = WIDGET_ARBMON_PANE_ALARM(self.appData)

        self.list_AlarmPaneWidgets = list([])

        wdg = WIDGET_ARBMON_PANE_NORMA(self.appData)

        self.list_AlarmPaneWidgets.append(wdg)  # widget #1 is "norma", the rest are "alarm"

        #for i in range(1, 97):
        #    wdg = WIDGET_ARBMON_PANE_ALARM(self.appData)
        #    wdg.tabCaption = "alr " + str(i)
        #    self.list_AlarmPaneWidgets.append(wdg)

        K = 2

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P6_TRUBEND, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.ALR_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.ALR_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.STP_FAILURE)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.STP_MATERIAL)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW, ENM_ALARM_PANE_TYPE.STP_QUALITY)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1

        wdg = WIDGET_ARBMON_PANE_ALARM(self.appData, ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT, ENM_ALARM_PANE_TYPE.STP_PROCESS)
        wdg.tabCaption = "alr " + str(K)
        self.list_AlarmPaneWidgets.append(wdg)
        K += 1


        # place tabs



        # place tabs

        for wdg in self.list_AlarmPaneWidgets:
            self.pane_AlarmPane.addTab(wdg, wdg.tabCaption)




        #

        #self.widget_CoreWidget.setLayout(self.layout_CoreLayout)






        # re-init GUI and show window

        #if GC.__FOUR_MON__:
        #    self.setGeometry(0, 0, 3840, 2160)
        #    #self.setGeometry(0, 0, 7680, 4320)
        #elif GC.__FOUR_MON_4K__:
        #    self.setGeometry(0, 0, 7680, 4320)
        #else:
        #    self.setGeometry(0, 0, 1920, 1080)
        self.setGeometry(0, 0, GC.monitor_px_width, GC.monitor_px_height)
        self.initUI()
        self.show()




        self.appData.worker_DBAccess = UDT_ARBMON_DB_CONNECTOR(self.appData)
        self.appData.worker_MCycle = UDT_ARBMON_MCYCLE_WORKER(self.appData)
        self.appData.worker_Dispatcher = UDT_ARBMON_DISPATCHER(self.appData)

        self.appData.worker_Dispatcher.moveToThread(self.appData.thread_Dispatcher)
        self.appData.worker_DBAccess.moveToThread(self.appData.thread_DBAccess)
        self.appData.worker_MCycle.moveToThread(self.appData.thread_MCycle)




        self.appData.thread_DBAccess.signal_ThreadStartedB.connect(self.appData.worker_DBAccess.msgprc_ConnectToDb)

        self.signal_UpdateUI.connect(self.msgprc_OnUpdateWindow)
        self.signal_UpdateUI.connect(self.pane_Workshop.msgprc_OnUpdateWindow)
        for wdg in self.list_AlarmPaneWidgets:
            self.signal_UpdateUI.connect(wdg.msgprc_OnUpdateWindow)   # pane_norma + pane_alarm
        self.signal_UpdateUI.connect(self.tpane_Diagrams.msgprc_OnUpdateWindow)

        self.signal_RestartTimers.connect(self.appData.worker_Dispatcher.msgprc_OnRestartTimers)

        self.signal_DBConnectionSuccess.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionSuccess)
        self.signal_DBConnectionFailure.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionFailure)
        self.signal_InitialDataReadDone.connect(self.appData.worker_MCycle.msgprc_OnInitialDataReadDone)
        self.signal_RTDataReadDone.connect(self.appData.worker_MCycle.msgprc_OnRTDataReadDone)
        self.signal_SettingsRead.connect(self.appData.worker_Dispatcher.msgprc_OnSettingsRead)
        self.signal_RestartTimerRunningCaption.connect(self.appData.worker_Dispatcher.msgprc_OnRestartTimerRunningCaption)
        self.signal_RestartTimerAlarmWidgets.connect(self.appData.worker_Dispatcher.msgprc_OnRestartTimerAlarmWidgets)

        self.appData.worker_MCycle.signal_ScreenChanged.connect(self.appData.worker_Dispatcher.msgprc_OnScreenChanged)




        self.n_ALARM_PANE_ACTIVE_WIDGET = 0 # это в списке виджетов
        self.n_ALARM_PANE_ACTIVE_TAB = 0    # это номер таба

        #

        self.appData.thread_Dispatcher.start()
        self.appData.thread_DBAccess.start()
        self.appData.thread_MCycle.start()

        #

        self.appData.pane_Diagrams = self.tpane_Diagrams

        #

        self.msgbox_ServerOff = None
        self.msgbox_DBConnFail = None

        #

        no_cursor = QCursor(Qt.BlankCursor)
        self.appData.application_TheApp.setOverrideCursor(no_cursor)

    ####################################################################################################################

    def initUI(self):

        if GC.__FOUR_MON__:
            monitor = QDesktopWidget().screenGeometry(0)
            self.move(monitor.left(), monitor.top())
        elif GC.__FOUR_MON_4K__:
            monitor = QDesktopWidget().screenGeometry(0)
            self.move(monitor.left(), monitor.top())
        else:
            monitor = QDesktopWidget().screenGeometry(1) # прилипнуть ко второму монитору
            self.move(monitor.left(), monitor.top())

        # Window core settings

        wnd_flags = self.windowFlags()
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
        # self.setWindowFlags(wnd_flags & ~(Qt.WindowMinimizeButtonHint|Qt.WindowMaximizeButtonHint|Qt.WindowCloseButtonHint|Qt.WindowSystemMenuHint|Qt.WindowTitleHint))
        self.setWindowTitle("ARBMON - \"Арнег\" - мониторинг состояния оборудования")
        #if not __DEBUG__:
        # self.showFullScreen()

        # Window Layout

        #self.layout_CoreLayout.addWidget(self.pane_ViewPane)
        #self.layout_CoreLayout.addWidget(self.pane_AlarmPane)


        #

        #self.layout_CoreLayout.setContentsMargins(0, 0, 0, 0)
        #self.layout_CoreLayout.setSpacing(0) # gap height
        self.tpane_Main.layout().setContentsMargins(0, 0, 0, 0)
        self.tpane_Main.layout().setSpacing(0)  # gap height

        if not __DEBUG__:
            self.widget_CoreWidget.tabBar().hide()
            self.pane_AlarmPane.tabBar().hide()

        #self.pane_ViewPane.setStyleSheet("QTabWidget::pane {border: 0px solid yellow; background: #000000;}")
        #self.pane_ViewPane.tabBar().setStyleSheet("QTabBar::tab {border: 1px solid red;}")
        self.widget_CoreWidget.setStyleSheet("QTabWidget::pane {border: 0px solid yellow; background: #000000; ppdding: 0px;}")
        self.widget_CoreWidget.tabBar().setStyleSheet("QTabBar::tab {border: 1px solid red;}")

        #self.pane_AlarmPane.setStyleSheet("QTabWidget::pane {border: 0px solid yellow; background: #323232;}")
        self.pane_AlarmPane.setStyleSheet("QTabWidget::pane {border: 0px solid yellow; background: #000000;}")
        self.pane_AlarmPane.tabBar().setStyleSheet("QTabBar::tab {border: 1px solid red; background: #C0C0C0;}")

        if GC.__FOUR_MON__:
            self.pane_AlarmPane.setMaximumHeight(240)
        elif GC.__FOUR_MON_4K__:
            self.pane_AlarmPane.setMaximumHeight(480)
        else:
            self.pane_AlarmPane.setMaximumHeight(120)




    ####################################################################################################################

    def closeEvent(self, event):

        #print("close app request")

        # close non-modal windows

        if self.msgbox_ServerOff is not None:
            self.msgbox_ServerOff.close()
        if self.msgbox_DBConnFail is not None:
            self.msgbox_DBConnFail.close()

        # make sure to finish all the threads

        self.appData.thread_Dispatcher.quit()
        self.appData.thread_DBAccess.quit()
        self.appData.thread_MCycle.quit()

        # close db connection

        self.appData.db.close()

        # save settings

        self.appData.settingsKeeper.setValue("s_msChangeAlarmPanel", self.appData.settings.ms_CHANGE_ALARM_WIDGET)
        self.appData.settingsKeeper.setValue("s_msRunningStringStep", self.appData.settings.ms_RUNNING_CAPTION_TICK)
        self.appData.settingsKeeper.setValue("s_msWorkshopPane", self.appData.settings.ms_SHOW_WORKSHOP)
        self.appData.settingsKeeper.setValue("s_msDiagramPane", self.appData.settings.ms_SHOW_DIAGRAMS)

        #accept close event

        event.accept()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        self.n_ALARM_PANE_ACTIVE_TAB = self.n_ALARM_PANE_ACTIVE_WIDGET
        self.pane_AlarmPane.setCurrentIndex( self.n_ALARM_PANE_ACTIVE_TAB )
        #self.list_AlarmPaneWidgets.setCurrentIndex( self.n_ALARM_PANE_ACTIVE_TAB )

        self.widget_CoreWidget.setCurrentIndex(self.appData.currentScreen - 1)

        if self.appData.DB_CONN_SUPERVISOR.DB_DATA_STATUS:
            self.msgbox_ServerOff = None
        else:
            if self.msgbox_ServerOff is None:
                self.msgbox_ServerOff = WINDOW_ARBMON_NONMODAL_MSGBOX(type=WINDOW_ARBMON_NONMODAL_MSGBOX.DB_DATA_FAILURE,bg_win=self)
                self.msgbox_ServerOff.show()

        if self.appData.DB_CONN_SUPERVISOR.DB_READ_STATUS:
            self.msgbox_DBConnFail = None
        else:
            if self.msgbox_DBConnFail is None:
                self.msgbox_DBConnFail = WINDOW_ARBMON_NONMODAL_MSGBOX(type=WINDOW_ARBMON_NONMODAL_MSGBOX.DB_READ_FAILURE,bg_win=self)
                self.msgbox_DBConnFail.show()


    ####################################################################################################################