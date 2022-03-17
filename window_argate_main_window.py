########################################################################################################################
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QDateTime, QDate, QTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QObject

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLabel

from PyQt5.QtSql import QSqlQuery

from PyQt5.QtGui import QIcon

########################################################################################################################

from enums import *

from udt_argate_dispatcher import UDT_ARGATE_DISPATCHER
from udt_network_checker import UDT_NETWORK_CHECKER
from udt_field_station_connector import UDT_FIELD_STATION_CONNECTOR
from udt_argate_db_connector import UDT_ARGATE_DB_CONNECTOR
from udt_argate_mcycle_worker import UDT_ARGATE_MCYCLE_WORKER
from udt_argate_excel_exporter import UDT_ARGATE_EXCEL_EXPORTER
from udt_mail_sender import UDT_MAIL_SENDER

from widget_argate_pane_main import WIDGET_ARGATE_PANE_MAIN
from widget_argate_pane_settings import WIDGET_ARGATE_PANE_SETTINGS
from widget_argate_pane_app_tracker import WIDGET_ARGATE_PANE_APP_TRACKER
from widget_argate_pane_tests import WIDGET_ARGATE_PANE_TESTS
from widget_argate_pane_field_access_tracker import WIDGET_ARGATE_PANE_FIELD_ACCESS_TRACKER
from widget_argate_pane_db_access_tracker import WIDGET_ARGATE_PANE_DB_ACCESS_TRACKER
from widget_argate_pane_reports_generation_tracker import WIDGET_ARGATE_PANE_REPORTS_GENERATION_TRACKER
from window_argate_about_dialog import WINDOW_ARGATE_ABOUT_DIALOG

from udt_tracker_list import UDT_TRACKER_LIST


########################################################################################################################
# описание класса:
# - Главное окно для утилиты ARGATE
#
########################################################################################################################

class WINDOW_ARGATE_MAIN_WINDOW(QMainWindow):

    signal_IsCheckingNetwork = pyqtSignal()
    signal_IsCheckingSocket = pyqtSignal(int)
    signal_IsCheckingNode = pyqtSignal(int)

    signal_StationFound = pyqtSignal(int)
    signal_StationLost = pyqtSignal(int)


    signal_ConnectToDb = pyqtSignal()

    #signal_RequestReportType1 = pyqtSignal()
    #signal_RequestAndSendReportType1 = pyqtSignal()
    #signal_RequestReportType2 = pyqtSignal()
    #signal_RequestAndSendReportType2 = pyqtSignal()
    #signal_SendEmail = pyqtSignal(str,str)
    #signal_Test1 = pyqtSignal()

    signal_TestDBWrite_WrStatesHist = pyqtSignal()
    signal_TestDBWrite_WrShiftStat = pyqtSignal()
    signal_TestDBWrite_WrDailyStat = pyqtSignal()
    signal_TestDBWrite_WrMonthStat = pyqtSignal()
    signal_TestDBWrite_WrYearStat = pyqtSignal()

    signal_DBWrite_WrStatesHist = pyqtSignal()
    signal_DBWrite_WrShiftStat = pyqtSignal()
    signal_DBWrite_WrDailyStat = pyqtSignal()
    signal_DBWrite_WrMonthStat = pyqtSignal()
    signal_DBWrite_WrYearStat = pyqtSignal()

    #

    #

    signal_DBConnectionSuccess = pyqtSignal()
    signal_DBConnectionFailure = pyqtSignal()
    signal_InitialDataReadDone = pyqtSignal(bool)
    signal_RTDataWriteDone = pyqtSignal(bool)   # вроде бы только пишем и ничего не читаем ???

    #

    signal_UpdateOutputWindow = pyqtSignal()
    signal_UpdateAppTracker = pyqtSignal()
    signal_UpdateFieldAccessTracker = pyqtSignal()
    signal_UpdateDBAccessTracker = pyqtSignal()
    signal_UpdateReportsGenerationTracker = pyqtSignal()


    # REPORT_T1 generation

    signal_RequestReportType1 = pyqtSignal(bool,bool)   # -> SUPERVISOR.msgprc_OnStartGeneration()
    signal_DBRead_TblReportT1 = pyqtSignal()            # -> worker_DBAccess.msgprc_OnDBRead_TblReportT1()
    signal_DBRead_TblReportT1_Done = pyqtSignal(bool)   # -> SUPERVISOR.msgprc_OnTableReceived()
    signal_ExcelFileT1_Done = pyqtSignal(bool,str,str)  # -> SUPERVISOR.msgprc_OnExcelFileReady()
    signal_T1_SendEmail = pyqtSignal(str,str)           # -> worker_MailSender.msgprc_OnSendEmail()
    signal_ReportT1Finished = pyqtSignal()              # -> widget_TabPaneTests.msgprc_OnReportT1Finished()

    # REPORT_T2 generation

    signal_RequestReportType2 = pyqtSignal(bool,bool)   # -> SUPERVISOR.msgprc_OnStartGeneration()
    signal_DBRead_TblReportT2 = pyqtSignal()            # -> worker_DBAccess.msgprc_OnDBRead_TblReportT2()
    signal_DBRead_TblReportT2_Done = pyqtSignal(bool)   # -> SUPERVISOR.msgprc_OnTableReceived()
    signal_ExcelFileT2_Done = pyqtSignal(bool,str,str)  # -> SUPERVISOR.msgprc_OnExcelFileReady()
    signal_T2_SendEmail = pyqtSignal(str, str)          # -> worker_MailSender.msgprc_OnSendEmail()
    signal_ReportT2Finished = pyqtSignal()              # -> widget_TabPaneTests.msgprc_OnReportT2Finished()



    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        # APP SETTINGS
        # C:\Users\Pavel\AppData\Local\Programs\Python\Python38
        self.appData.settingsFileName = self.appData.str_ResDir + "/argate.ini"
        self.appData.settingsKeeper = QSettings(self.appData.settingsFileName, QSettings.IniFormat)
        self.appData.icon_MainWindowIcon = QIcon(self.appData.str_ResDir + "/window_icon.png")

        try:
            self.appData.settings.writeRtDataToDB = int(self.appData.settingsKeeper.value("s_writeRtDataToDB"))
            self.appData.settings.writeStatesHistoryToDB = int(self.appData.settingsKeeper.value("s_writeStatesHistoryToDB"))

            self.appData.settings.reportStartDate = QDate.fromString(self.appData.settingsKeeper.value("s_reportStartDate"),"dd.MM.yyyy")
            self.appData.settings.dailyReportTime = QTime.fromString(self.appData.settingsKeeper.value("s_dailyReportTime"),"hh:mm:ss")
            self.appData.settings.monthReportTime = QTime.fromString(self.appData.settingsKeeper.value("s_monthReportTime"),"hh:mm:ss")
            self.appData.settings.yearReportTime = QTime.fromString(self.appData.settingsKeeper.value("s_yearReportTime"),"hh:mm:ss")

            self.appData.settings.keepCopyOfReportFileOnServer = int(self.appData.settingsKeeper.value("s_keepCopyOfReportFileOnServer"))
            self.appData.settings.dirForReportFiles = str(self.appData.settingsKeeper.value("s_dirForReportFiles"))
            self.appData.settings.destEmail = str(self.appData.settingsKeeper.value("s_destEmail"))
            self.appData.settings.show12hShiftsInReportT1 = int(self.appData.settingsKeeper.value("s_show12hShiftsInReportT1"))

        except:
            pass



        # VARS

        self.widget_CoreWidget = QWidget()
        self.layout_CoreLayout = QGridLayout()
        self.splitter_VSplitter = QSplitter(Qt.Horizontal)
        self.splitter_HSplitter = QSplitter(Qt.Vertical)

        self.widget_TreePaneWidget = QWidget()
        self.layout_TreePaneLayout = QVBoxLayout()

        self.widget_ViewPaneWidget = QWidget()
        self.layout_ViewPaneLayout = QVBoxLayout()

        self.widget_OutputPaneWidget = QWidget()
        self.layout_OutputPaneLayout = QVBoxLayout()

        self.label_TreeCaption = QLabel()
        self.tree_Tree = QTreeWidget()

        self.label_ViewCaption = QLabel()
        self.pane_ViewPane = QTabWidget()

        self.label_OutputCaption = QLabel()
        self.output_OutputWindow = QListView()

        self.pane_Main = WIDGET_ARGATE_PANE_MAIN(self.appData)
        self.pane_Settings = WIDGET_ARGATE_PANE_SETTINGS(self.appData)
        self.pane_Tests = WIDGET_ARGATE_PANE_TESTS(self.appData)
        self.pane_AppTracker = WIDGET_ARGATE_PANE_APP_TRACKER(self.appData)
        self.pane_FieldAccessTracker = WIDGET_ARGATE_PANE_FIELD_ACCESS_TRACKER(self.appData)
        self.pane_DBAccessTracker = WIDGET_ARGATE_PANE_DB_ACCESS_TRACKER(self.appData)
        self.pane_ReportsGenerationTracker = WIDGET_ARGATE_PANE_REPORTS_GENERATION_TRACKER(self.appData)

        self.pane_ViewPane.addTab(self.pane_Main, "pane_Main")
        self.pane_ViewPane.addTab(self.pane_Settings, "pane_Settings")
        self.pane_ViewPane.addTab(self.pane_Tests, "pane_Tests")
        self.pane_ViewPane.addTab(self.pane_AppTracker, "pane_")
        self.pane_ViewPane.addTab(self.pane_FieldAccessTracker, "pane_")
        self.pane_ViewPane.addTab(self.pane_DBAccessTracker, "pane_")
        self.pane_ViewPane.addTab(self.pane_ReportsGenerationTracker, "pane_")

        self.appData.widget_TabPaneMain = self.pane_Main
        self.appData.widget_TabPaneSettings = self.pane_Settings
        self.appData.widget_TabPaneTests = self.pane_Tests
        self.appData.widget_TabPaneAppTracker = self.pane_AppTracker
        self.appData.widget_TabPaneFieldAccessTracker = self.pane_FieldAccessTracker
        self.appData.widget_TabPaneDBAccessTracker = self.pane_DBAccessTracker
        self.appData.widget_TabPaneReportsGenerationTracker = self.pane_ReportsGenerationTracker



        self.widget_CoreWidget.setLayout(self.layout_CoreLayout)
        self.setCentralWidget(self.widget_CoreWidget)




        # MENU BAR

        # self.exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        self.exitAction = QAction('&Закрыть', self)

        self.menubar_MenuBar = self.menuBar()

        self.menuitem_File = self.menubar_MenuBar.addMenu("Файл")
        self.menuitem_Help = self.menubar_MenuBar.addMenu("?")

        # self.action_Exit = self.menuitem_File.addAction("Выйти")
        self.action_Exit = self.menuitem_File.addAction(self.exitAction)

        self.action_About = self.menuitem_Help.addAction("О программе...")


        # STATUS BAR

        self.statusbar_StatusBar = self.statusBar()

        # messaging

        self.tree_Tree.itemClicked.connect(self.msgproc_OnTreeItemClicked)



        # re-init GUI and show window

        self.setGeometry(50, 50, 1000, 800)
        self.initUI()
        self.show()


        self.appData.worker_CheckNetwork = UDT_NETWORK_CHECKER(self.appData)
        self.appData.worker_FieldAccess = UDT_FIELD_STATION_CONNECTOR(self.appData)
        self.appData.worker_DBAccess = UDT_ARGATE_DB_CONNECTOR(self.appData)
        self.appData.worker_MCycle = UDT_ARGATE_MCYCLE_WORKER(self.appData)
        self.appData.worker_Dispatcher = UDT_ARGATE_DISPATCHER(self.appData)
        #self.appData.worker_ExcelExporter = UDT_ARGATE_EXCEL_EXPORTER(self.appData)
        #self.appData.worker_MailSender = UDT_MAIL_SENDER(self.appData)

        self.appData.worker_Dispatcher.moveToThread(self.appData.thread_Dispatcher)
        self.appData.worker_CheckNetwork.moveToThread(self.appData.thread_CheckNetwork)
        self.appData.worker_FieldAccess.moveToThread(self.appData.thread_FieldAccess)
        self.appData.worker_DBAccess.moveToThread(self.appData.thread_DBAccess)
        self.appData.worker_MCycle.moveToThread(self.appData.thread_MCycle)
        #self.appData.worker_ExcelExporter.moveToThread(self.appData.thread_ExcelExporter)
        #self.appData.worker_MailSender.moveToThread(self.appData.thread_MailSender)

        self.appData.REPORT_T1_SUPERVISOR.moveToThread(self.appData.thread_MCycle)
        self.appData.REPORT_T2_SUPERVISOR.moveToThread(self.appData.thread_MCycle)

        self.appData.thread_Dispatcher.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnThreadDispatcherStarted)
        self.appData.thread_Dispatcher.signal_ThreadStarted.connect(self.msgproc_OnThreadDispatcherStarted)

        self.appData.thread_CheckNetwork.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnCheckNetworkThreadStarted)
        self.appData.thread_CheckNetwork.signal_ThreadStarted.connect(self.msgproc_OnCheckNetworkThreadStarted)

        self.appData.thread_FieldAccess.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnFieldAccessThreadStarted)
        self.appData.thread_FieldAccess.signal_ThreadStarted.connect(self.msgproc_OnFieldAccessThreadStarted)
        #self.appData.thread_FieldAccess.signal_ThreadFinished.connect(self.msgproc_OnFieldAccessThreadFinished)

        self.appData.worker_FieldAccess.signal_connectResult.connect(self.msgproc_OnFieldAccessNodeConnected)
        #self.appData.worker_FieldAccess.signal_readDataResult.connect(self.msgproc_OnFieldAccessReadData)
        self.appData.worker_FieldAccess.signal_disconnectResult.connect(self.msgproc_OnFieldAccessNodeDisconnected)

        self.appData.thread_DBAccess.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnDBAccessThreadStarted)
        self.appData.thread_DBAccess.signal_ThreadStarted.connect(self.msgproc_OnDBAccessThreadStarted)
        self.appData.thread_DBAccess.signal_ThreadStartedB.connect(self.appData.worker_DBAccess.msgprc_ConnectToDb)

        self.appData.thread_MCycle.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnT1ThreadStarted) # поменять на mcycle
        self.appData.thread_MCycle.signal_ThreadStarted.connect(self.msgproc_OnT1ThreadStarted) # поменять на mcycle

        #self.appData.thread_ExcelExporter.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnExcelExporterThreadStarted)
        #self.appData.thread_ExcelExporter.signal_ThreadStarted.connect(self.msgproc_OnExcelExporterThreadStarted)

        #self.appData.thread_MailSender.signal_ThreadStarted.connect(self.pane_AppTracker.msgproc_OnMailSenderThreadStarted)
        #self.appData.thread_MailSender.signal_ThreadStarted.connect(self.msgproc_OnMailSenderThreadStarted)



        self.signal_StationFound.connect(self.appData.worker_FieldAccess.msgprc_OnStationFound)
        self.signal_StationLost.connect(self.appData.worker_FieldAccess.msgprc_OnStationLost)

        self.appData.worker_FieldAccess.connectSignals()   # УБРАТЬ

        #self.appData.worker_DBAccess.connectSignals()   # УБРАТЬ
        self.appData.worker_MCycle.connectSignals()     # УБРАТЬ




        #self.appData.query = QSqlQuery()

        self.connectSignals()
        #self.tab_Tab2.connectSignals()

        self.appData.thread_Dispatcher.start()
        self.appData.thread_CheckNetwork.start()
        self.appData.thread_FieldAccess.start()
        self.appData.thread_DBAccess.start()
        self.appData.thread_MCycle.start()
        #self.appData.thread_ExcelExporter.start()
        #self.appData.thread_MailSender.start()

    ####################################################################################################################




    ####################################################################################################################

    def initUI(self):

        # Window core settings

        self.setWindowTitle("ARGATE - \"Арнег\" - мониторинг состояния оборудования")
        self.setWindowIcon(self.appData.icon_MainWindowIcon)

        # Window Layout

        self.layout_CoreLayout.addWidget(self.splitter_VSplitter, 0, 0, 1, 1)
        self.layout_CoreLayout.addWidget(self.splitter_HSplitter, 1, 0, 1, 1)

        self.widget_TreePaneWidget.setLayout(self.layout_TreePaneLayout)
        self.widget_ViewPaneWidget.setLayout(self.layout_ViewPaneLayout)
        self.widget_OutputPaneWidget.setLayout(self.layout_OutputPaneLayout)

        self.widget_CoreWidget.setLayout(self.layout_CoreLayout)

        self.layout_TreePaneLayout.addWidget(self.label_TreeCaption)
        self.layout_TreePaneLayout.addWidget(self.tree_Tree)

        self.layout_ViewPaneLayout.addWidget(self.label_ViewCaption)
        self.layout_ViewPaneLayout.addWidget(self.pane_ViewPane)

        self.layout_OutputPaneLayout.addWidget(self.label_OutputCaption)
        self.layout_OutputPaneLayout.addWidget(self.output_OutputWindow)

        self.splitter_VSplitter.addWidget(self.widget_TreePaneWidget)
        self.splitter_VSplitter.addWidget(self.widget_ViewPaneWidget)
        #self.splitter_VSplitter.setSizes([100,100])

        self.splitter_HSplitter.addWidget(self.splitter_VSplitter)
        self.splitter_HSplitter.addWidget(self.widget_OutputPaneWidget)

        self.setCentralWidget(self.widget_CoreWidget)

        # populate tree

        self.tree_Tree.setHeaderHidden(True)
        self.tree_Tree.setColumnCount(3)
        self.tree_Tree.setColumnWidth(0, 200)

        new_item = QTreeWidgetItem(self.tree_Tree)
        new_item.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_MAIN))
        new_item.setText(0, "Главная")

        new_item = QTreeWidgetItem(self.tree_Tree)
        new_item.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_UNKNOWN))
        new_item.setText(0, "Служебные")

        new_item_2 = QTreeWidgetItem(new_item)
        new_item_2.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_SETTINGS))
        new_item_2.setText(0, "Настройки")

        new_item_3 = QTreeWidgetItem(new_item)
        new_item_3.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_TESTS))
        new_item_3.setText(0, "Тесты")

        new_item_4 = QTreeWidgetItem(new_item)
        new_item_4.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_APP_MONITOR))
        new_item_4.setText(0, "Трекер : приложение")

        new_item_5 = QTreeWidgetItem(new_item)
        new_item_5.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_FIELDACCESS_MONITOR))
        new_item_5.setText(0, "Трекер : IO stations access")

        new_item_6 = QTreeWidgetItem(new_item)
        new_item_6.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_DBACCESS_MONITOR))
        new_item_6.setText(0, "Трекер : DB access")

        new_item_7 = QTreeWidgetItem(new_item)
        new_item_7.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARGATE_PANES.PANE_REPORT_GENERATION_MONITOR))
        new_item_7.setText(0, "Трекер : генерация отчётов")



        # set-up tabs

        self.pane_ViewPane.tabBar().hide()

        # set-up output window

        self.output_OutputWindow.setModel(self.appData.model_OutputWindow)





        # Fill-up

        self.label_TreeCaption.setText("Дерево")
        self.label_ViewCaption.setText("Главная")
        self.label_OutputCaption.setText("Трекер")


        # MENU BAR

        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Выйти')
        #self.exitAction.triggered.connect(self.appData.application_TheApp.quit)
        self.exitAction.triggered.connect(self.close)

        # STATUS BAR

        self.statusbar_StatusBar.showMessage(self.appData.programVersion)

        # finished

        #self.appData.model_OutputWindow.theList.append(
         #   QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "-- " + self.appData.programDescription + " --")
        #self.appData.model_FieldAccessTracker.layoutChanged.emit()

        self.appData.model_OutputWindow.append(
            QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "-- " + self.appData.programDescription + " --")
        self.signal_UpdateOutputWindow.emit()

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "-- " + self.appData.programDescription + " --")
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "-- " + self.appData.programDescription + " --"

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    def connectSignals(self):

        #self.appData.worker_DBAccess.signal_Connected.connect(self.appData.widget_TabPaneAppTracker.msgprc_OnDBConnected)
        #self.appData.worker_DBAccess.signal_Connected.connect(self.appData.widget_TabPaneDBAccessTracker.msgprc_OnDBConnected)
        #self.appData.worker_DBAccess.signal_DBConnected.connect(self.msgprc_OnDBConnected)

        #self.appData.worker_DBAccess.signal_ConnectionFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBConnectionFailed)

        #self.appData.worker_DBAccess.signal_DBWriteSuccessful.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBWriteSuccessful)
        #self.appData.worker_DBAccess.signal_DBWriteFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBWriteFailed)
        #self.appData.worker_DBAccess.signal_DBReadSuccessful.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBReadSuccessful)
        #self.appData.worker_DBAccess.signal_DBReadFailed.connect(self.appData.widget_TabPaneDBAccessTracker.msgproc_OnDBReadFailed)

        #self.signal_RequestReportType1.connect(self.appData.worker_MCycle.msgprc_OnRequestReportType1)
        #self.signal_RequestAndSendReportType1.connect(self.appData.worker_MCycle.msgprc_OnRequestAndSendReportType1)
        #self.signal_RequestReportType2.connect(self.appData.worker_MCycle.msgprc_OnRequestReportType2)
        #self.signal_RequestAndSendReportType2.connect(self.appData.worker_MCycle.msgprc_OnRequestAndSendReportType2)
        #self.signal_SendEmail.connect(self.appData.worker_MailSender.msgprc_OnSendEmail)
        #self.signal_Test1.connect(self.appData.worker_MCycle.msgprc_OnEndOfDay) - удалить

        self.action_About.triggered.connect(self.msgprc_OnMenuItemAboutClick)

        self.signal_IsCheckingNetwork.connect(self.msgprc_OnIsCheckingNetwork)
        self.signal_IsCheckingSocket.connect(self.msgprc_OnIsCheckingSocket)
        self.signal_IsCheckingNode.connect(self.msgprc_OnIsCheckingNode)

        self.signal_TestDBWrite_WrStatesHist.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrStatesHist)
        self.signal_TestDBWrite_WrShiftStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrShiftStat)
        self.signal_TestDBWrite_WrDailyStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrDailyStat)
        self.signal_TestDBWrite_WrMonthStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrMonthStat)
        self.signal_TestDBWrite_WrYearStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrYearStat)

        #self.signal_DBWrite_WrStateHist.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrStatesHist)
        self.signal_DBWrite_WrShiftStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrShiftStat)
        self.signal_DBWrite_WrDailyStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrDailyStat)
        self.signal_DBWrite_WrMonthStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrMonthStat)
        self.signal_DBWrite_WrYearStat.connect(self.appData.worker_DBAccess.msgprc_OnDBWriteWrYearStat)

        #

        self.signal_UpdateOutputWindow.connect(self.msgprc_OnUpdateOutputWindow)
        self.signal_UpdateAppTracker.connect(self.msgprc_OnUpdateAppTracker)
        self.signal_UpdateFieldAccessTracker.connect(self.msgprc_OnUpdateFieldAccessTracker)
        self.signal_UpdateDBAccessTracker.connect(self.msgprc_OnUpdateDBAccessTracker)
        self.signal_UpdateReportsGenerationTracker.connect(self.msgprc_OnUpdateReportsGenerationTracker)

        self.signal_DBConnectionSuccess.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionSuccess)
        self.signal_DBConnectionFailure.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionFailure)
        self.signal_InitialDataReadDone.connect(self.appData.worker_MCycle.msgprc_OnInitialDataReadDone)

        #

        self.signal_RequestReportType1.connect(self.appData.REPORT_T1_SUPERVISOR.msgprc_OnStartGeneration)
        self.signal_DBRead_TblReportT1.connect(self.appData.worker_DBAccess.msgprc_OnDBRead_TblReportT1)
        self.signal_DBRead_TblReportT1_Done.connect(self.appData.REPORT_T1_SUPERVISOR.msgprc_OnTableReceived)
        self.signal_ExcelFileT1_Done.connect(self.appData.REPORT_T1_SUPERVISOR.msgprc_OnExcelFileReady)
        #self.signal_T1_SendEmail.connect(self.appData.worker_MailSender.msgprc_OnSendEmail)
        #self.signal_T1_SendEmail_Done.connect(self.appData.REPORT_T1_SUPERVISOR.msgprc_OnEmailSent)
        self.signal_ReportT1Finished.connect(self.appData.widget_TabPaneTests.msgprc_OnReportT1Finished)



        self.signal_RequestReportType2.connect(self.appData.REPORT_T2_SUPERVISOR.msgprc_OnStartGeneration)
        self.signal_DBRead_TblReportT2.connect(self.appData.worker_DBAccess.msgprc_OnDBRead_TblReportT2)
        self.signal_DBRead_TblReportT2_Done.connect(self.appData.REPORT_T2_SUPERVISOR.msgprc_OnTableReceived)
        self.signal_ExcelFileT2_Done.connect(self.appData.REPORT_T2_SUPERVISOR.msgprc_OnExcelFileReady)
        self.signal_ReportT2Finished.connect(self.appData.widget_TabPaneTests.msgprc_OnReportT2Finished)



    ####################################################################################################################

    #@QtCore.pyqtSlot(QTreeWidgetItem, int)
    def msgproc_OnTreeItemClicked(self, item, col):

        pane_id = QVariant(item.data(0, Qt.WhatsThisRole)).value()

        # __debug_begin__
        # print(pane_id)
        # __debug_end__

        if pane_id != ENM_ARGATE_PANES.PANE_UNKNOWN:

            self.pane_ViewPane.setCurrentIndex(pane_id-1)

            if pane_id == ENM_ARGATE_PANES.PANE_MAIN:
                self.label_ViewCaption.setText("Главная")
            if pane_id == ENM_ARGATE_PANES.PANE_SETTINGS:
                self.label_ViewCaption.setText("Настройки")
            if pane_id == ENM_ARGATE_PANES.PANE_TESTS:
                self.label_ViewCaption.setText("Тесты")
            if pane_id == ENM_ARGATE_PANES.PANE_APP_MONITOR:
                self.label_ViewCaption.setText("Трекер : приложение")
            if pane_id == ENM_ARGATE_PANES.PANE_FIELDACCESS_MONITOR:
                self.label_ViewCaption.setText("Трекер : IO stations access")
            if pane_id == ENM_ARGATE_PANES.PANE_DBACCESS_MONITOR:
                self.label_ViewCaption.setText("Трекер : DB access")
            if pane_id == ENM_ARGATE_PANES.PANE_REPORT_GENERATION_MONITOR:
                self.label_ViewCaption.setText("Трекер : генерация отчётов")

    ####################################################################################################################

    def closeEvent(self, event):

        print("close app request")

        self.appData.db.close()

        # make sure to finish all the threads

        self.appData.thread_Dispatcher.quit()
        self.appData.thread_MCycle.quit()
        self.appData.thread_DBAccess.quit()
        self.appData.thread_FieldAccess.quit()
        self.appData.thread_CheckNetwork.quit()
        #self.appData.thread_ExcelExporter.quit()
        #self.appData.thread_MailSender.quit()

        # save settings

        self.saveSettings()

        #self.appData.settings.destEmail = self.pane_Settings.lineedit_DestinationEmail.text() # а вот в чем дело ))
        #                                                                                    # данные хранятся в интерфейсе )
        #                                                                                    # хотя как то удобно вроде получается
        #
        #self.appData.settingsKeeper.setValue("s_writeRtDataToDB", self.appData.settings.writeRtDataToDB)
        #self.appData.settingsKeeper.setValue("s_writeStatesHistoryToDB", self.appData.settings.writeStatesHistoryToDB)
        #
        #self.appData.settingsKeeper.setValue("s_reportStartDate", self.appData.settings.reportStartDate.toString("dd.MM.yyyy"))
        #self.appData.settingsKeeper.setValue("s_dailyReportTime", self.appData.settings.dailyReportTime.toString("hh:mm:ss"))
        #self.appData.settingsKeeper.setValue("s_monthReportTime", self.appData.settings.monthReportTime.toString("hh:mm:ss"))
        #self.appData.settingsKeeper.setValue("s_yearReportTime", self.appData.settings.yearReportTime.toString("hh:mm:ss"))
        #
        #self.appData.settingsKeeper.setValue("s_keepCopyOfReportFileOnServer", self.appData.settings.keepCopyOfReportFileOnServer)
        #self.appData.settingsKeeper.setValue("s_dirForReportFiles", self.appData.settings.dirForReportFiles)
        #self.appData.settingsKeeper.setValue("s_destEmail", self.appData.settings.destEmail)
        #self.appData.settingsKeeper.setValue("s_show12hShiftsInReportT1", self.appData.settings.show12hShiftsInReportT1)

        #accept close event

        event.accept()

    ####################################################################################################################

    def saveSettings(self):

        self.appData.settings.destEmail = self.pane_Settings.lineedit_DestinationEmail.text() # а вот в чем дело ))
                                                                                            # данные хранятся в интерфейсе )
                                                                                            # хотя как то удобно вроде получается

        self.appData.settingsKeeper.setValue("s_writeRtDataToDB", self.appData.settings.writeRtDataToDB)
        self.appData.settingsKeeper.setValue("s_writeStatesHistoryToDB", self.appData.settings.writeStatesHistoryToDB)

        self.appData.settingsKeeper.setValue("s_reportStartDate", self.appData.settings.reportStartDate.toString("dd.MM.yyyy"))
        self.appData.settingsKeeper.setValue("s_dailyReportTime", self.appData.settings.dailyReportTime.toString("hh:mm:ss"))
        self.appData.settingsKeeper.setValue("s_monthReportTime", self.appData.settings.monthReportTime.toString("hh:mm:ss"))
        self.appData.settingsKeeper.setValue("s_yearReportTime", self.appData.settings.yearReportTime.toString("hh:mm:ss"))

        self.appData.settingsKeeper.setValue("s_keepCopyOfReportFileOnServer", self.appData.settings.keepCopyOfReportFileOnServer)
        self.appData.settingsKeeper.setValue("s_dirForReportFiles", self.appData.settings.dirForReportFiles)
        self.appData.settingsKeeper.setValue("s_destEmail", self.appData.settings.destEmail)
        self.appData.settingsKeeper.setValue("s_show12hShiftsInReportT1", self.appData.settings.show12hShiftsInReportT1)


    ####################################################################################################################

    # FieldIOAccess Thread signals
    @pyqtSlot(str)
    def msgproc_OnFieldAccessThreadFinished(self, text):

        self.appData.model_FieldAccessTracker.theList.append(
            QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        self.appData.model_FieldAccessTracker.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnIsCheckingNetwork(self):

        text = "запрос на сканирование сети"

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker


    @pyqtSlot(int)
    def msgprc_OnIsCheckingSocket(self,mt_id):

        text = "check socket station #" + str(mt_id)

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    @pyqtSlot(int)
    def msgprc_OnIsCheckingNode(self,mt_id):

        text = "check opc-server station #" + str(mt_id)

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    ####################################################################################################################

    @pyqtSlot(int,int,QDateTime)
    def msgproc_OnFieldAccessNodeConnected(self, node_id, result_id, dt):

        text = "Подключение к станции №" + str(node_id) + " прошло "

        if result_id == 1:
            text = text + "успешно (+)"
        if result_id == 2:
            text = text + "неудачно (-)"

        #text = text + dt.toString("dd.MM.yyyy hh:mm:ss.zzz")

        #self.appData.model_FieldAccessTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_FieldAccessTracker.layoutChanged.emit()
        #self.appData.model_FieldAccessTracker.setCurrentIndex(2)
        #self.appData.model_FieldAccessTracker.scrollTo(self.appData.model_FieldAccessTracker.rowInList())

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    ####################################################################################################################

    def msgproc_OnFieldAccessReadData(self, node_id, result_id, dt):

        text = "Чтение данных из станции №" + str(node_id) + " прошло "

        if result_id == 1:
            text = text + "успешно (+)"
        if result_id == 2:
            text = text + "неудачно (-)"

        #text = text + dt.toString("dd.MM.yyyy hh:mm:ss.zzz")

        #self.appData.model_FieldAccessTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_FieldAccessTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    ####################################################################################################################

    def msgproc_OnFieldAccessNodeDisconnected(self, node_id, dt):

        text = "Отключение от станции №" + str(node_id) + " "

        #text = text + dt.toString("dd.MM.yyyy hh:mm:ss.zzz")

        #self.appData.model_FieldAccessTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_FieldAccessTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnThreadDispatcherStarted(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnCheckNetworkThreadStarted(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnFieldAccessThreadStarted(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnDBAccessThreadStarted(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnT1ThreadStarted(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnExcelExporterThreadStarted(self, str):
    #
    #    text = str
    #
    #    self.appData.model_OutputWindow.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_OutputWindow.layoutChanged.emit()
    #
    #####################################################################################################################
    #
    #@pyqtSlot(str)
    #def msgproc_OnMailSenderThreadStarted(self, str):
    #
    #    text = str
    #
    #    self.appData.model_OutputWindow.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgprc_OnDBConnected(self, str):

        text = str

        #self.appData.model_OutputWindow.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_OutputWindow.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateOutputWindow(self):

        if self.output_OutputWindow is not None:
            self.appData.model_OutputWindow.layoutChanged.emit()
            self.output_OutputWindow.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateAppTracker(self):

        if self.appData.widget_TabPaneAppTracker is not None:
            if not self.appData.widget_TabPaneAppTracker.paused:
                self.appData.model_AppTrackerView.layoutChanged.emit()
                self.appData.widget_TabPaneAppTracker.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateFieldAccessTracker(self):

        if self.appData.widget_TabPaneFieldAccessTracker is not None:
            if not self.appData.widget_TabPaneFieldAccessTracker.paused:
                self.appData.model_FieldAccessTrackerView.layoutChanged.emit()
                self.appData.widget_TabPaneFieldAccessTracker.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateDBAccessTracker(self):

        #if self.appData.widget_TabPaneDBAccessTracker is not None:
        #
        #    if not self.appData.widget_TabPaneDBAccessTracker.paused:
        #
        #        n = self.appData.widget_TabPaneDBAccessTracker.cnt_MissedTrackerRecords + 1
        #        sublist = self.appData.model_DBAccessTrackerBack.theList[-n:]
        #
        #        for item in sublist:
        #            self.appData.model_DBAccessTrackerView.append(item)
        #
        #        self.appData.widget_TabPaneDBAccessTracker.cnt_MissedTrackerRecords = 0
        #
        #
        #        self.appData.model_DBAccessTrackerView.layoutChanged.emit()
        #        self.appData.widget_TabPaneDBAccessTracker.listbox_Tracker.scrollToBottom()
        #
        #    else:
        #        self.appData.widget_TabPaneDBAccessTracker.cnt_MissedTrackerRecords += 1
        #else:
        #    self.appData.model_DBAccessTrackerView.append(self.appData.model_DBAccessTrackerBack.theList[-1])

        if self.appData.widget_TabPaneDBAccessTracker is not None:
            if not self.appData.widget_TabPaneDBAccessTracker.paused:
                self.appData.model_DBAccessTrackerView.layoutChanged.emit()
                self.appData.widget_TabPaneDBAccessTracker.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateReportsGenerationTracker(self):

        if self.appData.widget_TabPaneReportsGenerationTracker is not None:
            if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
                self.appData.model_RepGenTrackerView.layoutChanged.emit()
                self.appData.widget_TabPaneReportsGenerationTracker.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    def msgprc_OnMenuItemAboutClick(self):

        dlg = WINDOW_ARGATE_ABOUT_DIALOG(self.appData)

        dlg.move(
            self.appData.window_MainWindow.x() + self.appData.window_MainWindow.width() / 2 - dlg.width() / 2,
            self.appData.window_MainWindow.y() + self.appData.window_MainWindow.height() / 2 - dlg.height() / 2
        )

        dlg.exec_()

    ####################################################################################################################


