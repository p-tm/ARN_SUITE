########################################################################################################################


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QRadioButton


from udt_field_station_connector import UDT_FIELD_STATION_CONNECTOR



########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WIDGET_ARGATE_PANE_TESTS(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.widget_Row_0 = QWidget()
        self.layout_Row_0 = QHBoxLayout()
        self.widget_Row_0.setLayout(self.layout_Row_0)

        self.widget_Row_1 = QWidget()
        self.layout_Row_1 = QHBoxLayout()
        self.widget_Row_1.setLayout(self.layout_Row_1)

        self.layout_CoreLayout.addWidget(self.widget_Row_0)
        self.layout_CoreLayout.addWidget(self.widget_Row_1)
        self.layout_CoreLayout.addStretch(1)

        buttonHeightMax = 40

        # row 0

        self.groupbox_AutoReportType1 = QGroupBox(self)
        self.groupbox_AutoReportType1.setTitle("Авто-отчёт тип 1")

        self.groupbox_AutoReportType2 = QGroupBox(self)
        self.groupbox_AutoReportType2.setTitle("Авто-отчёт тип 2")

        self.layout_Row_0.addWidget(self.groupbox_AutoReportType1)
        self.layout_Row_0.addWidget(self.groupbox_AutoReportType2)


        # Groupbox 1
        #self.button_ART1_Generate = QPushButton(self.groupbox_AutoReportType1)
        #self.button_ART1_GenerateAndSend = QPushButton(self.groupbox_AutoReportType1)
        self.button_ART1_Generate = QPushButton()
        self.button_ART1_GenerateAndSend = QPushButton()

        self.layout_GroupBoxAutoReportType1 = QHBoxLayout()
        self.groupbox_AutoReportType1.setLayout(self.layout_GroupBoxAutoReportType1)

        self.layout_GroupBoxAutoReportType1.addWidget(self.button_ART1_Generate)
        self.layout_GroupBoxAutoReportType1.addWidget(self.button_ART1_GenerateAndSend)

        self.button_ART1_Generate.setMinimumHeight(buttonHeightMax)
        self.button_ART1_GenerateAndSend.setMinimumHeight(buttonHeightMax)

        self.button_ART1_Generate.setText("Сгенерировать")
        self.button_ART1_GenerateAndSend.setText("Сгенерировать\nи отправить")

        #self.groupbox_AutoReportType1.setGeometry(0, 0, 100, 100)
        #self.button_ART1_Generate.move(20, 20)
        #self.button_ART1_GenerateAndSend.move(70, 20)

        #self.button_ART1_Generate.setGeometry(10, 20, 120, 60)
        #self.button_ART1_GenerateAndSend.setGeometry(10+5+120, 20, 120, 60)

        # Groupbox 2
        #self.button_ART2_Generate = QPushButton(self.groupbox_AutoReportType2)
        #self.button_ART2_GenerateAndSend = QPushButton(self.groupbox_AutoReportType2)
        self.button_ART2_Generate = QPushButton()
        self.button_ART2_GenerateAndSend = QPushButton()

        self.layout_GroupBoxAutoReportType2 = QHBoxLayout()
        self.groupbox_AutoReportType2.setLayout(self.layout_GroupBoxAutoReportType2)

        self.layout_GroupBoxAutoReportType2.addWidget(self.button_ART2_Generate)
        self.layout_GroupBoxAutoReportType2.addWidget(self.button_ART2_GenerateAndSend)

        self.button_ART2_Generate.setMinimumHeight(buttonHeightMax)
        self.button_ART2_GenerateAndSend.setMinimumHeight(buttonHeightMax)

        self.button_ART2_Generate.setText("Сгенерировать")
        self.button_ART2_GenerateAndSend.setText("Сгенерировать\nи отправить")

        #self.button_ART2_Generate.setGeometry(10, 20, 120, 60)
        #self.button_ART2_GenerateAndSend.setGeometry(10+5+120, 20, 120, 60)

        # row 1

        self.groupbox_TestDBWrite = QGroupBox(self)
        self.groupbox_TestDBWrite.setTitle("Тесты записи в БД")
        self.layout_GroupBoxTestDBWrite = QHBoxLayout()
        self.groupbox_TestDBWrite.setLayout(self.layout_GroupBoxTestDBWrite)

        self.layout_Row_1.addWidget(self.groupbox_TestDBWrite)


        self.button_TestDBWrite_WrStatesHist = QPushButton()
        self.button_TestDBWrite_WrShiftStat = QPushButton()
        self.button_TestDBWrite_WrDailyStat = QPushButton()
        self.button_TestDBWrite_WrMonthStat = QPushButton()
        self.button_TestDBWrite_WrYearStat = QPushButton()

        self.layout_GroupBoxTestDBWrite.addWidget(self.button_TestDBWrite_WrStatesHist)
        self.layout_GroupBoxTestDBWrite.addWidget(self.button_TestDBWrite_WrShiftStat)
        self.layout_GroupBoxTestDBWrite.addWidget(self.button_TestDBWrite_WrDailyStat)
        self.layout_GroupBoxTestDBWrite.addWidget(self.button_TestDBWrite_WrMonthStat)
        self.layout_GroupBoxTestDBWrite.addWidget(self.button_TestDBWrite_WrYearStat)

        self.button_TestDBWrite_WrStatesHist.setMinimumHeight(buttonHeightMax)
        self.button_TestDBWrite_WrShiftStat.setMinimumHeight(buttonHeightMax)
        self.button_TestDBWrite_WrDailyStat.setMinimumHeight(buttonHeightMax)
        self.button_TestDBWrite_WrMonthStat.setMinimumHeight(buttonHeightMax)
        self.button_TestDBWrite_WrYearStat.setMinimumHeight(buttonHeightMax)

        self.button_TestDBWrite_WrStatesHist.setText("Real-time\nзапись")
        self.button_TestDBWrite_WrShiftStat.setText("Имитация\nконца смены")
        self.button_TestDBWrite_WrDailyStat.setText("Имитация\nконца дня")
        self.button_TestDBWrite_WrMonthStat.setText("Имитация\nконца месяца")
        self.button_TestDBWrite_WrYearStat.setText("Имитация\nконца года")


        self.connectSignals()

    ####################################################################################################################

    def connectSignals(self):

        self.button_ART1_Generate.pressed.connect(self.msgprc_OnButtonART1GeneratePressed)
        self.button_ART1_GenerateAndSend.pressed.connect(self.msgprc_OnButtonART1GenerateAndSendPressed)

        self.button_ART2_Generate.pressed.connect(self.msgprc_OnButtonART2GeneratePressed)
        self.button_ART2_GenerateAndSend.pressed.connect(self.msgprc_OnButtonART2GenerateAndSendPressed)

        self.button_TestDBWrite_WrStatesHist.pressed.connect(self.msgprc_OnButtonTestDBWriteWrStatesHist)
        self.button_TestDBWrite_WrShiftStat.pressed.connect(self.msgprc_OnButtonTestDBWriteWrShiftStat)
        self.button_TestDBWrite_WrDailyStat.pressed.connect(self.msgprc_OnButtonTestDBWriteWrDailyStat)
        self.button_TestDBWrite_WrMonthStat.pressed.connect(self.msgprc_OnButtonTestDBWriteWrMonthStat)
        self.button_TestDBWrite_WrYearStat.pressed.connect(self.msgprc_OnButtonTestDBWriteWrYearStat)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonART1GeneratePressed(self):   # ART1 - Auto-Report Type #1

        self.RepT1ButtonsEnable(False)
        self.appData.window_MainWindow.signal_RequestReportType1.emit(False,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonART1GenerateAndSendPressed(self):

        self.RepT1ButtonsEnable(False)
        self.appData.window_MainWindow.signal_RequestReportType1.emit(True,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonART2GeneratePressed(self):   # ART2 - Auto-Report Type #2

        self.RepT2ButtonsEnable(False)
        self.appData.window_MainWindow.signal_RequestReportType2.emit(False,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonART2GenerateAndSendPressed(self):

        self.RepT2ButtonsEnable(False)
        self.appData.window_MainWindow.signal_RequestReportType2.emit(True,self.appData.settings.keepCopyOfReportFileOnServer) # -> SUPERVISOR.msgprc_OnStartGeneration()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonTestDBWriteWrStatesHist(self):

        self.appData.window_MainWindow.signal_TestDBWrite_WrStatesHist.emit() # -> UDT_DB_CONNECTOR.msgprc_

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonTestDBWriteWrShiftStat(self):

        self.appData.window_MainWindow.signal_TestDBWrite_WrShiftStat.emit() # ->


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonTestDBWriteWrDailyStat(self):

        self.appData.window_MainWindow.signal_TestDBWrite_WrDailyStat.emit() # -> worker_DBAccess.msgprc_OnDBWriteWrDailyStat
        #self.appData.window_MainWindow.signal_RequestReportType1.emit(True, self.appData.settings.keepCopyOfReportFileOnServer)


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonTestDBWriteWrMonthStat(self):

        self.appData.window_MainWindow.signal_TestDBWrite_WrMonthStat.emit() # ->

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonTestDBWriteWrYearStat(self):

        self.appData.window_MainWindow.signal_TestDBWrite_WrYearStat.emit() # ->

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportT1Finished(self):
        self.RepT1ButtonsEnable(True)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportT2Finished(self):
        self.RepT2ButtonsEnable(True)

    ####################################################################################################################

    def RepT1ButtonsEnable(self, en):
        self.button_ART1_Generate.setEnabled(en)
        self.button_ART1_GenerateAndSend.setEnabled(en)

    ####################################################################################################################

    def RepT2ButtonsEnable(self, en):
        self.button_ART2_Generate.setEnabled(en)
        self.button_ART2_GenerateAndSend.setEnabled(en)






