########################################################################################################################
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate, QTime, QDateTime

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from copy import copy

########################################################################################################################

from enums import *

from widget_arterm_pane_basic import WIDGET_ARTERM_PANE_BASIC
from widget_arterm_pane_field_monitor import WIDGET_ARTERM_PANE_FIELD_MONITOR
from widget_arterm_pane_day_viewer import WIDGET_ARTERM_PANE_DAY_VIEWER
from widget_arterm_pane_detalied_rep import WIDGET_ARTERM_PANE_DETAILED_REP
from widget_arterm_pane_settings import WIDGET_ARTERM_PANE_SETTINGS
from widget_arterm_pane_settings_arbmon import WIDGET_ARTERM_PANE_SETTINGS_ARBMON

from window_arterm_about_dialog import WINDOW_ARTERM_ABOUT_DIALOG
from window_autorization_dialog import WINDOW_AUTORIZATION_DIALOG
from window_tracker_nonmodal import WINDOW_TRACKER_NONMODAL

from udt_arterm_dispatcher import UDT_ARTERM_DISPATCHER
from udt_arterm_mcycle_worker import UDT_ARTERM_MCYCLE_WORKER
from udt_arterm_db_connector import UDT_ARTERM_DB_CONNECTOR
from udt_user import UDT_USER

########################################################################################################################
# описание класса:
# - Главное окно для утилиты ARTERM
#
########################################################################################################################

class WINDOW_ARTERM_MAIN_WINDOW(QMainWindow):

    #
    signal_UpdateUI = pyqtSignal()
    signal_SingleUpdateArbmonSettings = pyqtSignal()
    signal_ReportOfDBConnectionFailure = pyqtSignal()
    signal_ReportOfInitialDataReadFailure = pyqtSignal()

    # DB access signals
    signal_DBConnectionSuccess = pyqtSignal()
    signal_DBConnectionFailure = pyqtSignal()
    signal_InitialDataReadDone = pyqtSignal(bool)
    signal_RTDataReadDone = pyqtSignal(bool)

    #signal_GetInitialDataReady = pyqtSignal(bool)
    signal_GetDataForSelectedDay = pyqtSignal(QDate)
    signal_GetDataForSelectedDayReady = pyqtSignal(bool) # изменить на ..Done !!
    signal_WriteDataForSelectedDay = pyqtSignal()
    signal_WriteDataForSelectedDayDone = pyqtSignal(bool)
    signal_WriteArbmonSettings = pyqtSignal()
    signal_WriteArbmonSettingsDone = pyqtSignal(bool)

    signal_UpdateDBAccessTracker = pyqtSignal()

    # DETAILED_REP generation

    signal_GenerateDetailedRep = pyqtSignal()                   # -> SUPERVISOR.msgprc_OnStartGeneration()
    signal_DBRead_TblDetailedRep = pyqtSignal()                 # -> worker_DBAccess.msgprc_OnReadTableDetailedReport()
    signal_DBRead_TblDetailedRep_Done = pyqtSignal(bool)        # -> SUPERVISOR.msgprc_OnTableReceived()
    signal_Excel_TblDetailedRep_Done = pyqtSignal(bool,str,str) # -> SUPERVISOR.msgprc_OnExcelFileReady()
    signal_ReportFinished = pyqtSignal()                        # -> widget_

    signal_UpdateReportsGenerationTracker = pyqtSignal()

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        # APP SETTINGS
        # C:\Users\Pavel\AppData\Local\Programs\Python\Python38
        self.appData.settingsFileName = self.appData.str_ResDir + "/arterm.ini"
        self.appData.settingsKeeper = QSettings(self.appData.settingsFileName, QSettings.IniFormat)
        self.appData.icon_MainWindowIcon = QIcon(self.appData.str_ResDir + "/window_icon.png")

        try:

            self.appData.settings.date_ReportBeginDate = QDate.fromString(self.appData.settingsKeeper.value("s_dateReportBeginDate"), "dd.MM.yyyy")
            self.appData.settings.time_ReportBeginTime = QTime.fromString(self.appData.settingsKeeper.value("s_timeReportBeginTime"), "hh:mm:ss")

            self.appData.settings.date_ReportEndDate = QDate.fromString(self.appData.settingsKeeper.value("s_dateReportEndDate"), "dd.MM.yyyy")
            self.appData.settings.time_ReportEndTime = QTime.fromString(self.appData.settingsKeeper.value("s_timeReportEndTime"), "hh:mm:ss")

            self.appData.settings.path_ReportFolder = str(self.appData.settingsKeeper.value("s_pathReportFolder"))
            self.appData.settings.enum_ReportSortBy = int(self.appData.settingsKeeper.value("s_enumReportSortBy"))

        except:
            pass


            #self.appData.settings.reportStartDate = QDate.fromString(self.appData.settingsKeeper.value("s_reportStartDate"),"dd.MM.yyyy")
            #self.appData.settings.dailyReportTime = QTime.fromString(self.appData.settingsKeeper.value("s_dailyReportTime"),"hh:mm:ss")


        # VARS

        self.widget_CoreWidget = QWidget()
        self.layout_CoreLayout = QVBoxLayout()
        self.splitter_VSplitter = QSplitter(Qt.Horizontal)

        self.widget_LeftPaneWidget = QWidget()
        self.layout_LeftPaneLayout = QVBoxLayout()

        self.widget_TreePaneWidget = QWidget()
        self.layout_TreePaneLayout = QVBoxLayout()

        self.widget_CalenderPaneWidget = QWidget()
        self.layout_CalenderPaneLayout = QVBoxLayout()

        self.widget_ViewPaneWidget = QWidget()
        self.layout_ViewPaneLayout = QVBoxLayout()

        self.label_TreeCaption = QLabel()
        self.tree_Tree = QTreeWidget()

        # ----------------------------------------------------------------------

        self.label_CalenderCaption = QLabel()
        self.calender_Calender = QCalendarWidget()
        self.widget_CalenderButtonPanel = QWidget()

        self.layout_CalenderButtonPanel = QHBoxLayout()

        self.button_CalenderGoToToday = QPushButton()
        self.button_CalenderGoToTomorrow = QPushButton()
        self.button_GetDataForSelectedDay = QPushButton()

        # ----------------------------------------------------------------------

        self.label_ViewCaption = QLabel()
        self.pane_ViewPane = QTabWidget()


        #----------------------------------------------------------------------

        self.tpane_Basic             = WIDGET_ARTERM_PANE_BASIC(self.appData)
        self.tpane_FieldMonitor      = WIDGET_ARTERM_PANE_FIELD_MONITOR(self.appData, ENM_LAMP_SHAPE.SQUARED)
        self.tpane_DayViewer         = WIDGET_ARTERM_PANE_DAY_VIEWER(self.appData)
        self.tpane_DetailedRep       = WIDGET_ARTERM_PANE_DETAILED_REP(self.appData)
        self.tpane_Settings          = WIDGET_ARTERM_PANE_SETTINGS(self.appData)
        self.tpane_ARBMON            = WIDGET_ARTERM_PANE_SETTINGS_ARBMON(self.appData)

        self.pane_ViewPane.addTab(self.tpane_Basic, "pane_Basic")
        self.pane_ViewPane.addTab(self.tpane_FieldMonitor, "pane_FMon")
        self.pane_ViewPane.addTab(self.tpane_DayViewer, "pane_SV")
        self.pane_ViewPane.addTab(self.tpane_DetailedRep, "pane_DetRep")
        self.pane_ViewPane.addTab(self.tpane_Settings, "pane_Sett")
        self.pane_ViewPane.addTab(self.tpane_ARBMON, "pane_ARBM")

        self.appData.tpane_Basic = self.tpane_Basic
        self.appData.tpane_FieldMonitor = self.tpane_FieldMonitor
        self.appData.tpane_DayViewer = self.tpane_DayViewer
        self.appData.tpane_DetailedRep = self.tpane_DetailedRep
        self.appData.tpane_Settings = self.tpane_Settings
        self.appData.tpane_ARBMON = self.tpane_ARBMON



        # MENU BAR

        # self.exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        self.exitAction = QAction('&Закрыть', self)
        self.aboutAction = QAction('&О программе...', self)

        self.menubar_MenuBar = self.menuBar()

        self.menuitem_File = self.menubar_MenuBar.addMenu("Файл")
        #self.menuitem_System = self.menubar_MenuBar.addMenu("Система")
        self.menuitem_Operation = self.menubar_MenuBar.addMenu("Функции")
        self.menuitem_Help = self.menubar_MenuBar.addMenu("?")

        self.action_Exit = self.menuitem_File.addAction(self.exitAction)

        #self.action_MachineTools = self.menuitem_System.addAction("Станки")
        #self.action_ShiftPlans = self.menuitem_System.addAction("Планы смен")
        #self.action_ShiftTypes = self.menuitem_System.addAction("Типы смен")

        self.action_Autorization = self.menuitem_Operation.addAction("Авторизация")
        self.action_Logout = self.menuitem_Operation.addAction("Выход")
        self.menuitem_Operation.addSeparator()
        self.action_DbAccesTracker = self.menuitem_Operation.addAction("Трекер: доступ к БД")

        self.action_About = self.menuitem_Help.addAction(self.aboutAction)

        # STATUS BAR

        self.statusbar_StatusBar = self.statusBar()

        self.statusbar_widget_Misc = QLabel()
        self.statusbar_widget_AutorizationStatus = QLabel()
        self.statusbar_widget_dbReadStatus = QLabel()
        self.statusbar_widget_dbDataStatus = QLabel()

        self.statusbar_widget_Misc.setMinimumWidth(100)
        self.statusbar_widget_dbReadStatus.setMinimumWidth(60)
        self.statusbar_widget_dbDataStatus.setMinimumWidth(60)

        self.pic_dbReadGreen = QPixmap(self.appData.str_ResDir + "/db_read_green.png").scaled(50,20)
        self.pic_dbReadDisconn = QPixmap(self.appData.str_ResDir + "/db_read_disconn.png").scaled(50, 20)
        self.pic_dbDataGreen = QPixmap(self.appData.str_ResDir + "/db_write_green.png").scaled(50, 20)
        self.pic_dbDataFail = QPixmap(self.appData.str_ResDir + "/db_write_disconn.png").scaled(50, 20)

        self.statusbar_widget_dbReadStatus.setPixmap(self.pic_dbReadDisconn)
        self.statusbar_widget_dbDataStatus.setPixmap(self.pic_dbDataFail)

        # threads


        self.appData.worker_DBAccess = UDT_ARTERM_DB_CONNECTOR(self.appData)
        self.appData.worker_MCycle = UDT_ARTERM_MCYCLE_WORKER(self.appData)
        self.appData.worker_Dispatcher = UDT_ARTERM_DISPATCHER(self.appData)






        # re-init GUI and show window

        self.setGeometry(50, 50, 1400, 400)
        self.initUI()
        self.show()

        #self.appData.worker_DBAccess.connectSignals()
        self.connectSignals()

        # threads


        self.appData.worker_DBAccess.moveToThread(self.appData.thread_DBAccess)
        self.appData.worker_MCycle.moveToThread(self.appData.thread_MCycle)
        self.appData.worker_Dispatcher.moveToThread(self.appData.thread_Dispatcher)



        self.appData.thread_DBAccess.start()
        self.appData.thread_MCycle.start()
        self.appData.thread_Dispatcher.start()


    ####################################################################################################################

    def initUI(self):

        # Window core settings

        self.setWindowTitle("ARTERM - \"Арнег\" - мониторинг состояния оборудования")
        self.setWindowIcon(self.appData.icon_MainWindowIcon)

        # Window Layout

        self.layout_CoreLayout.addWidget(self.splitter_VSplitter)

        self.splitter_VSplitter.addWidget(self.widget_LeftPaneWidget)
        self.splitter_VSplitter.addWidget(self.widget_ViewPaneWidget)

        self.widget_CoreWidget.setLayout(self.layout_CoreLayout)

        self.layout_LeftPaneLayout.addWidget(self.widget_TreePaneWidget)
        self.layout_LeftPaneLayout.addWidget(self.widget_CalenderPaneWidget)
        self.layout_LeftPaneLayout.addStretch(1)

        self.widget_LeftPaneWidget.setLayout(self.layout_LeftPaneLayout)
        #self.widget_LeftPaneWidget.setMinimumWidth(200)



        self.layout_TreePaneLayout.addWidget(self.label_TreeCaption)
        self.layout_TreePaneLayout.addWidget(self.tree_Tree)

        self.widget_TreePaneWidget.setLayout(self.layout_TreePaneLayout)

        xw = self.calender_Calender.minimumSizeHint().width()
        self.splitter_VSplitter.setSizes([xw, self.width()-xw])

        # statusbar



        #self.statusbar_pic_DBAccess.setPixmap(pic.scaled(50, 25))

        self.statusbar_StatusBar.addWidget(self.statusbar_widget_Misc)
        self.statusbar_StatusBar.addWidget(self.statusbar_widget_AutorizationStatus)
        self.statusbar_StatusBar.addPermanentWidget(self.statusbar_widget_dbDataStatus)
        self.statusbar_StatusBar.addPermanentWidget(self.statusbar_widget_dbReadStatus)



        # ----------------------------------------------------------------------

        self.layout_CalenderPaneLayout.addWidget(self.label_CalenderCaption)
        self.layout_CalenderPaneLayout.addWidget(self.calender_Calender)

        self.layout_CalenderPaneLayout.addWidget(self.widget_CalenderButtonPanel)


        self.layout_CalenderButtonPanel.addStretch(1)
        self.layout_CalenderButtonPanel.addWidget(self.button_GetDataForSelectedDay)
        self.layout_CalenderButtonPanel.addWidget(self.button_CalenderGoToToday)
        self.layout_CalenderButtonPanel.addWidget(self.button_CalenderGoToTomorrow)

        self.widget_CalenderButtonPanel.setLayout(self.layout_CalenderButtonPanel)



        # ----------------------------------------------------------------------


        self.widget_CalenderPaneWidget.setLayout(self.layout_CalenderPaneLayout)
        #self.widget_CalenderPaneWidget.setVisible(False)

        self.layout_ViewPaneLayout.addWidget(self.label_ViewCaption)
        self.layout_ViewPaneLayout.addWidget(self.pane_ViewPane)

        self.widget_ViewPaneWidget.setLayout(self.layout_ViewPaneLayout)

        self.setCentralWidget(self.widget_CoreWidget)

        # populate tree

        self.tree_Tree.setHeaderHidden(True)
        self.tree_Tree.setColumnCount(1)
        self.tree_Tree.setColumnWidth(0, 200)

        self.treeitem_Basic = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_Basic.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_BASIC))
        self.treeitem_Basic.setText(0, "Базовые текущие данные")

        self.treeitem_Field = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_Field.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_FIELD_MONITOR))
        self.treeitem_Field.setText(0, "Состояние оборудования")

        self.treeitem_DayViewer = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_DayViewer.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_DAY_VIEWER))
        self.treeitem_DayViewer.setText(0, "Производственный календарь")

        self.treeitem_DetailedRep = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_DetailedRep.setData(0,Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_DETAILED_REP))
        self.treeitem_DetailedRep.setText(0, "Детализированный отчёт")

        self.treeitem_Service = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_Service.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_UNKNOWN))
        self.treeitem_Service.setText(0, "Служебные")   # надо сделать чтобы не открывалось без авторизации на edit

        self.treeitem_Service_Settings = QTreeWidgetItem(self.treeitem_Service)
        self.treeitem_Service_Settings.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_SERVICE_SETTINGS))
        self.treeitem_Service_Settings.setText(0, "Настройки")

        self.treeitem_Service_ARBMON = QTreeWidgetItem(self.treeitem_Service)
        self.treeitem_Service_ARBMON.setData(0, Qt.WhatsThisRole, QVariant(ENM_ARTERM_PANES.PANE_SERVICE_ARBMON))
        self.treeitem_Service_ARBMON.setText(0, "Центральный монитор")





        # set-up tabs

        self.pane_ViewPane.tabBar().hide()

        self.pane_ViewPane.setCurrentIndex(0)
        self.label_ViewCaption.setText("Базовые текущие данные")







        # Fill-up

        self.label_TreeCaption.setText("Дерево")
        self.label_CalenderCaption.setText("Календарь")

        self.button_CalenderGoToToday.setText("Сегодня")
        self.button_CalenderGoToTomorrow.setText("Завтра")
        self.button_GetDataForSelectedDay.setText("Получить данные")



        # MENU BAR

        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Выйти')



        # STATUS BAR

        #self.statusbar_StatusBar.showMessage(self.appData.programVersion)

        #calender

        self.calender_Calender.setMinimumDate(QDate(2021,1,0))
        self.calender_Calender.setMaximumDate(QDate(2049,12,31))



    ####################################################################################################################

    def connectSignals(self):

        # system
        self.appData.thread_DBAccess.signal_ThreadStartedB.connect(self.appData.worker_DBAccess.msgprc_ConnectToDb)


        # MAIN MENU
        self.action_Autorization.triggered.connect(self.msgprc_OnAutorization)
        self.action_Logout.triggered.connect(self.msgprc_OnLogout)
        self.action_DbAccesTracker.triggered.connect(self.msgprc_OnDbAccessTracker)
        self.exitAction.triggered.connect(self.close)


        self.aboutAction.triggered.connect(self.msgprc_OnMenuItemAboutClick)

        # TREE
        self.tree_Tree.itemClicked.connect(self.msgprc_OnTreeItemClicked)

        #
        self.signal_UpdateUI.connect(self.msgprc_OnUpdateWindow)
        self.signal_UpdateUI.connect(self.tpane_Basic.msgprc_OnUpdateWindow)
        self.signal_UpdateUI.connect(self.tpane_FieldMonitor.msgprc_OnUpdateWindow)
        self.signal_UpdateUI.connect(self.tpane_DayViewer.msgprc_OnUpdateWindow)
        self.signal_UpdateUI.connect(self.tpane_ARBMON.msgprc_OnUpdateWindow)

        self.signal_SingleUpdateArbmonSettings.connect(self.tpane_ARBMON.msgprc_OnSingleUpdateWindow)
        self.signal_ReportOfDBConnectionFailure.connect(self.msgprc_OnReportOfDBConnectionFailure)
        self.signal_ReportOfInitialDataReadFailure.connect(self.msgprc_OnReportOfInitialDataReadFailure)



        self.button_GetDataForSelectedDay.clicked.connect(self.msgprc_OnGetDataForSelectedDay)
        self.button_CalenderGoToToday.clicked.connect(self.msgprc_OnCalenderGoToToday)
        self.button_CalenderGoToTomorrow.clicked.connect(self.msgprc_OnCalenderGoToTomorrow)

        # DB Access

        self.signal_DBConnectionSuccess.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionSuccess)
        self.signal_DBConnectionFailure.connect(self.appData.worker_MCycle.msgprc_OnDBConnectionFailure)
        self.signal_InitialDataReadDone.connect(self.appData.worker_MCycle.msgprc_OnInitialDataReadDone)
        self.signal_RTDataReadDone.connect(self.appData.worker_MCycle.msgprc_OnRTDataReadDone)

        #self.signal_GetInitialDataReady.connect(self.msgprc_OnGetInitialDataReady)

        self.signal_GetDataForSelectedDay.connect(self.appData.worker_DBAccess.msgprc_OnGetDataForSelectedDay)
        self.signal_GetDataForSelectedDayReady.connect(self.appData.worker_MCycle.msgprc_OnGetDataForSelectedDayReady)
        self.signal_WriteDataForSelectedDay.connect(self.appData.worker_DBAccess.msgprc_OnWriteDataForSelectedDay)
        self.signal_WriteDataForSelectedDayDone.connect(self.appData.worker_MCycle.msgprc_OnWriteDataForSelectedDayDone)
        self.signal_WriteArbmonSettings.connect(self.appData.worker_DBAccess.msgprc_OnWriteArbmonSettings)
        self.signal_WriteArbmonSettingsDone.connect(self.appData.tpane_ARBMON.msgprc_OnWriteArbmonSettingsDone)

        #

        self.signal_UpdateDBAccessTracker.connect(self.msgprc_OnUpdateDBAccessTracker)

        #

        self.signal_GenerateDetailedRep.connect(self.appData.DETAILED_REP_SUPERVISOR.msgprc_OnStartGeneration)
        self.signal_DBRead_TblDetailedRep.connect(self.appData.worker_DBAccess.msgprc_OnReadTableDetailedReport)
        self.signal_DBRead_TblDetailedRep_Done.connect(self.appData.DETAILED_REP_SUPERVISOR.msgprc_OnTableReceived)
        self.signal_Excel_TblDetailedRep_Done.connect(self.appData.DETAILED_REP_SUPERVISOR.msgprc_OnExcelFileReady)
        self.signal_ReportFinished.connect(self.appData.tpane_DetailedRep.msgprc_OnReportFinished)

        self.signal_UpdateReportsGenerationTracker.connect(self.msgprc_OnUpdateReportsGenerationTracker)

    ####################################################################################################################

    def closeEvent(self, event):

        #print("close app request")

        # close non-modal windows

        if self.appData.window_DBAccessTracker is not None:
            self.appData.window_DBAccessTracker.close()



        # make sure to finish all the threads

        self.appData.thread_Dispatcher.quit()
        self.appData.thread_DBAccess.quit()
        self.appData.thread_MCycle.quit()

        # close db connection

        self.appData.db.close()

        # save settings

        self.saveSettings()

        # ...

        event.accept()

    ####################################################################################################################

    def saveSettings(self):

        self.appData.settingsKeeper.setValue("s_dateReportBeginDate", self.appData.settings.date_ReportBeginDate.toString("dd.MM.yyyy"))
        self.appData.settingsKeeper.setValue("s_timeReportBeginTime", self.appData.settings.time_ReportBeginTime.toString("hh:mm:ss"))
        self.appData.settingsKeeper.setValue("s_dateReportEndDate", self.appData.settings.date_ReportEndDate.toString("dd.MM.yyyy"))
        self.appData.settingsKeeper.setValue("s_timeReportEndTime", self.appData.settings.time_ReportEndTime.toString("hh:mm:ss"))

        self.appData.settingsKeeper.setValue("s_enumReportSortBy", self.appData.settings.enum_ReportSortBy)
        self.appData.settingsKeeper.setValue("s_pathReportFolder", self.appData.settings.path_ReportFolder)

    ####################################################################################################################

    def msgprc_OnTreeItemClicked(self, item):

        pane_id = QVariant(item.data(0, Qt.WhatsThisRole)).value()

        if pane_id != ENM_ARGATE_PANES.PANE_UNKNOWN:

            self.pane_ViewPane.setCurrentIndex(pane_id-1)

            if pane_id == ENM_ARTERM_PANES.PANE_BASIC:

                self.label_ViewCaption.setText("Базовые текущие данные")
                #self.widget_CalenderPaneWidget.setVisible(False)


            if pane_id == ENM_ARTERM_PANES.PANE_FIELD_MONITOR:

                self.label_ViewCaption.setText("Монитор оборудования")
                #self.widget_CalenderPaneWidget.setVisible(False)

            if pane_id == ENM_ARTERM_PANES.PANE_DAY_VIEWER:

                self.label_ViewCaption.setText("Расписание")
                #self.widget_CalenderPaneWidget.setVisible(True)
                self.calender_Calender.setSelectedDate(QDate.currentDate())

            if pane_id == ENM_ARTERM_PANES.PANE_DETAILED_REP:

                self.label_ViewCaption.setText("Детализированный отчёт")

            if pane_id == ENM_ARTERM_PANES.PANE_SERVICE_SETTINGS:

                self.label_ViewCaption.setText("Настройки")

            if pane_id == ENM_ARTERM_PANES.PANE_SERVICE_ARBMON:

                self.label_ViewCaption.setText("Центральный монитор")
                #self.appData.tpane_ARBMON.initData()

    ####################################################################################################################

    def msgprc_OnMenuItemAboutClick(self):

        dlg = WINDOW_ARTERM_ABOUT_DIALOG(self.appData)

        dlg.move(
            self.appData.window_MainWindow.x() + self.appData.window_MainWindow.width() / 2 - dlg.width() / 2,
            self.appData.window_MainWindow.y() + self.appData.window_MainWindow.height() / 2 - dlg.height() / 2
        )

        dlg.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        self.statusbar_widget_Misc.setText(self.appData.programVersion)

        if self.appData.LOGGED_IN:
            self.action_Logout.setEnabled(True)
            self.statusbar_widget_AutorizationStatus.setText("Пользователь: " + self.appData.ACTIVE_USER.caption)
        else:
            self.action_Logout.setEnabled(False)
            self.statusbar_widget_AutorizationStatus.setText("Пользователь не авторизован")

        if self.appData.DB_CONN_SUPERVISOR.DB_READ_STATUS:
            self.statusbar_widget_dbReadStatus.setPixmap(self.pic_dbReadGreen)
        else:
            self.statusbar_widget_dbReadStatus.setPixmap(self.pic_dbReadDisconn)

        if self.appData.DB_CONN_SUPERVISOR.DB_DATA_STATUS:
            self.statusbar_widget_dbDataStatus.setPixmap(self.pic_dbDataGreen)
        else:
            self.statusbar_widget_dbDataStatus.setPixmap(self.pic_dbDataFail)


        if self.appData.LOGGED_IN:
            if self.appData.ACTIVE_USER.permission_edit:
                self.treeitem_Service.setHidden(False)
                self.treeitem_Service.setDisabled(False)
                #self.treeitem_Service.setItemExpandable(True)
                #self.treeitem_Service.setFlags(self.treeitem_Service.flags() | Qt.ItemIsEnabled)
                self.tpane_DayViewer.button_LaunchEditor.setEnabled(True)
                self.tpane_DayViewer.button_ApplyChanges.setEnabled(True)
            elif self.appData.ACTIVE_USER.permission_view:
                self.treeitem_Service.setHidden(False)
                self.treeitem_Service.setDisabled(True)
                #self.treeitem_Service.setItemExpandable(True)
                #self.treeitem_Service.setFlags(self.treeitem_Service.flags() & ~Qt.ItemIsEnabled)
            else:
                self.treeitem_Service.setHidden(True)
                #self.treeitem_Service.setItemExpandable(False)
                #self.treeitem_Service.setFlags(self.treeitem_Service.flags() & ~Qt.ItemIsEnabled & ~Qt.ItemIsSelectable)
        else:
            #self.treeitem_Service.setExpanded(False)
            #self.treeitem_Service.setDisabled(True)
            self.treeitem_Service.setHidden(True)
            #self.treeitem_Service.setFlags(self.treeitem_Service.flags() & ~Qt.ItemIsEnabled & ~Qt.ItemIsSelectable)
            self.tpane_DayViewer.button_LaunchEditor.setEnabled(False)
            self.tpane_DayViewer.button_ApplyChanges.setEnabled(False)



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnGetDataForSelectedDay(self):

        self.signal_GetDataForSelectedDay.emit(self.calender_Calender.selectedDate())

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCalenderGoToToday(self):

        self.calender_Calender.setSelectedDate(QDate.currentDate())

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCalenderGoToTomorrow(self):

        _date = QDate.currentDate().addDays(1)

        self.calender_Calender.setSelectedDate(_date)

    ####################################################################################################################

    #@pyqtSlot(bool)
    #def msgprc_OnGetInitialDataReady(self, success):
    #
    #    if success:
    #
    #        self.appData.tpane_ARBMON.initData()
    #
    #    else:
    #
    #        msgbox = QMessageBox()
    #        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
    #        msgbox.setWindowTitle("Ошибка")
    #        msgbox.setIcon(QMessageBox.Critical)
    #        msgbox.setText(
    #            "Инициализация данных прошла неудачно")
    #        msgbox.setDetailedText(
    #            "Попробуйте перезапустить программу."
    #            "Если ошибка опвторится, то ... ??")
    #        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
    #        msgbox.setStandardButtons(QMessageBox.Ok)
    #
    #        for btn in msgbox.buttons():
    #            #btn_role = msgbox.buttonRole(btn)
    #            if msgbox.buttonRole(btn) == QMessageBox.ActionRole:
    #                btn.click()
    #                #btn.setDisabled(True)
    #                #btn.setText("-")
    #            if msgbox.buttonRole(btn) == QMessageBox.RejectRole:
    #                btn.setText("Закрыть")
    #
    #
    #        msgbox.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnAutorization(self):

        dlg = WINDOW_AUTORIZATION_DIALOG(self.appData,  self)

        dlg.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnLogout(self):

        self.appData.ACTIVE_USER = copy(UDT_USER())
        self.appData.LOGGED_IN = False

        msgbox = QMessageBox(parent=self)   # is parent is set the dialog is centered to the center of parent
        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
        msgbox.setWindowTitle("Инфо")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setText(
            "Вы вышли из системы")
        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportOfDBConnectionFailure(self):

        msgbox = QMessageBox(parent=self)
        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
        msgbox.setWindowTitle("Ошибка")
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText(
            "Не удаётся подключиться к серверу")
        msgbox.setDetailedText(
            "Попробуйте перезапустить программу."
            "Если ошибка повторится, то ... ??")
        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
        msgbox.setStandardButtons(QMessageBox.Ok)

        for btn in msgbox.buttons():
            #btn_role = msgbox.buttonRole(btn)
            if msgbox.buttonRole(btn) == QMessageBox.ActionRole:
                btn.click()
                #btn.setDisabled(True)
                #btn.setText("-")
            if msgbox.buttonRole(btn) == QMessageBox.RejectRole:
                btn.setText("Закрыть")


        msgbox.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportOfInitialDataReadFailure(self):

        msgbox = QMessageBox(parent=self)
        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
        msgbox.setWindowTitle("Ошибка")
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText(
            "Инициализация данных прошла неудачно")
        msgbox.setDetailedText(
            "Попробуйте перезапустить программу."
            "Если ошибка опвторится, то ... ??")
        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
        msgbox.setStandardButtons(QMessageBox.Ok)

        for btn in msgbox.buttons():
            #btn_role = msgbox.buttonRole(btn)
            if msgbox.buttonRole(btn) == QMessageBox.ActionRole:
                btn.click()
                #btn.setDisabled(True)
                #btn.setText("-")
            if msgbox.buttonRole(btn) == QMessageBox.RejectRole:
                btn.setText("Закрыть")


        msgbox.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDbAccessTracker(self):

        self.appData.window_DBAccessTracker = WINDOW_TRACKER_NONMODAL(self.appData, self.appData.model_DBAccessTrackerView, self)
        self.appData.window_DBAccessTracker.show()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateDBAccessTracker(self):

        #if self.appData.window_DBAccessTracker is not None:
        #
        #    if not self.appData.window_DBAccessTracker.paused:
        #
        #        n = self.appData.window_DBAccessTracker.cnt_MissedTrackerRecords + 1
        #        sublist = self.appData.model_DBAccessTrackerBack.theList[-n:]
        #
        #        for item in sublist:
        #            self.appData.model_DBAccessTrackerView.append(item)
        #
        #        self.appData.window_DBAccessTracker.cnt_MissedTrackerRecords = 0
        #
        #
        #        self.appData.model_DBAccessTrackerView.layoutChanged.emit()
        #        self.appData.window_DBAccessTracker.listbox_Tracker.scrollToBottom()
        #
        #    else:
        #        self.appData.window_DBAccessTracker.cnt_MissedTrackerRecords += 1
        #else:
        #    self.appData.model_DBAccessTrackerView.append(self.appData.model_DBAccessTrackerBack.theList[-1])

        if self.appData.window_DBAccessTracker is not None:
            if not self.appData.window_DBAccessTracker.paused:
                self.appData.model_DBAccessTrackerView.layoutChanged.emit()
                self.appData.window_DBAccessTracker.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateReportsGenerationTracker(self):

        if self.appData.tpane_DetailedRep is not None:
            #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
            if True:
                self.appData.model_DetailedRepTrackerView.layoutChanged.emit()
                self.appData.tpane_DetailedRep.tracker_DetailedRepProcess.scrollToBottom()

    ####################################################################################################################