########################################################################################################################

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QLineEdit

from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QFileDialog

########################################################################################################################

########################################################################################################################
# описание класса:
# - виджет для вкладки "Детализированный отчёт"
#
########################################################################################################################

class WIDGET_ARTERM_PANE_DETAILED_REP(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.calender_ReportBeginDate = QCalendarWidget()
        self.timeedit_ReportBeginTime = QTimeEdit()
        self.calender_ReportEndDate = QCalendarWidget()
        self.timeedit_ReportEndTime = QTimeEdit()

        self.timeedit_ReportBeginTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_ReportEndTime.setDisplayFormat("hh:mm:ss")

        self.initUI()
        self.initData()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        gb1 = QGroupBox()
        gb1.setTitle(" Временной интервал ")
        gb1.setLayout(QHBoxLayout())

        wdg = QWidget()
        wdg.setLayout(QVBoxLayout())
        wdg.layout().addWidget(QLabel("Начало интервала: дата"))
        wdg.layout().addWidget(self.calender_ReportBeginDate)
        wdg.layout().addWidget(QLabel("Начало интервала: время"))
        wdg.layout().addWidget(self.timeedit_ReportBeginTime)
        gb1.layout().addWidget(wdg)

        wdg = QWidget()
        wdg.setLayout(QVBoxLayout())
        wdg.layout().addWidget(QLabel("Конец интервала: дата"))
        wdg.layout().addWidget(self.calender_ReportEndDate)
        wdg.layout().addWidget(QLabel("Конец интервала: время"))
        wdg.layout().addWidget(self.timeedit_ReportEndTime)
        gb1.layout().addWidget(wdg)

        gb1.layout().addStretch(1)

        gb1.setFixedHeight(300)


        gb2 = QGroupBox()
        gb2.setTitle(" Сортировка ")
        gb2.setLayout(QHBoxLayout())

        rb = QRadioButton()
        rb.setText("по времени")
        gb2.layout().addWidget(rb)

        rb = QRadioButton()
        rb.setText("по станку")
        gb2.layout().addWidget(rb)

        gb2.layout().addStretch(1)

        gb2.setFixedHeight(50)

        path_edit_header = QLabel("Папка для хранения копий отчётов")
        path_widget = QWidget()
        path_widget.setLayout(QHBoxLayout())
        path_widget.layout().addWidget(QLineEdit())
        path_widget.layout().addWidget(QPushButton("..."))

        path_widget.layout().itemAt(1).widget().setFixedWidth(30)

        tracker_header = QLabel("Генерация отчёта")
        tracker = QListView()

        gb4 = QGroupBox()
        gb4.setLayout(QHBoxLayout())
        gb4.layout().addStretch(1)
        gb4.layout().addWidget(QPushButton("Сгенерировать"))

        gb4.setFixedHeight(40)







        self.layout_CoreLayout.addWidget(gb1)
        self.layout_CoreLayout.addWidget(gb2)
        self.layout_CoreLayout.addWidget(path_edit_header)
        self.layout_CoreLayout.addWidget(path_widget)
        self.layout_CoreLayout.addWidget(tracker_header)
        self.layout_CoreLayout.addWidget(tracker)
        self.layout_CoreLayout.addWidget(gb4)

        self.radiobutton_ReportSortByTime = gb2.layout().itemAt(0).widget()
        self.radiobutton_ReportSortByMT = gb2.layout().itemAt(1).widget()
        self.lineedit_FolderPath = path_widget.layout().itemAt(0).widget()
        self.button_SelectFolder = path_widget.layout().itemAt(1).widget()
        self.tracker_DetailedRepProcess = tracker
        self.button_GenerateRep = gb4.layout().itemAt(1).widget()

    ####################################################################################################################

    def initData(self):

        self.calender_ReportBeginDate.setMinimumDate(QDate(2021, 1, 0))
        self.calender_ReportEndDate.setMaximumDate(QDate(2049, 12, 31))

        self.calender_ReportBeginDate.setSelectedDate(self.appData.settings.date_ReportBeginDate)
        self.calender_ReportEndDate.setSelectedDate(self.appData.settings.date_ReportEndDate)

        self.timeedit_ReportBeginTime.setTime(self.appData.settings.time_ReportBeginTime)
        self.timeedit_ReportEndTime.setTime(self.appData.settings.time_ReportEndTime)

        self.tracker_DetailedRepProcess.setModel(self.appData.model_DetailedRepTrackerView)
        self.tracker_DetailedRepProcess.setAlternatingRowColors(True)

        self.lineedit_FolderPath.setText(self.appData.settings.path_ReportFolder)

        self.radiobutton_ReportSortByTime.setChecked(self.appData.settings.enum_ReportSortBy == 1)
        self.radiobutton_ReportSortByMT.setChecked(self.appData.settings.enum_ReportSortBy == 2)

    ####################################################################################################################

    def connectSignals(self):

        self.calender_ReportBeginDate.clicked.connect(self.msgprc_OnReportBeginDateSelect)
        self.calender_ReportEndDate.clicked.connect(self.msgprc_OnReportEndDateSelect)
        self.timeedit_ReportBeginTime.timeChanged.connect(self.msgprc_OnReportBeginTimeSelect)
        self.timeedit_ReportEndTime.timeChanged.connect(self.msgprc_OnReportEndTimeSelect)

        self.button_SelectFolder.clicked.connect(self.msgprc_OnButtonSelectFolderClick)
        self.button_GenerateRep.clicked.connect(self.msgprc_OnButtonGenerateDetailedRep)
        self.radiobutton_ReportSortByTime.toggled.connect(self.msgprc_OnRadiobuttonReportSortByTimeToggle)
        self.radiobutton_ReportSortByMT.toggled.connect(self.msgprc_OnRadiobuttonReportSortByMTToggle)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonSelectFolderClick(self):

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        folder = QFileDialog.getExistingDirectory()
        self.lineedit_FolderPath.setText(folder)

        self.appData.settings.path_ReportFolder = folder

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonGenerateDetailedRep(self):

        self.appData.window_MainWindow.signal_GenerateDetailedRep.emit()    # -> SUPERVISOR.msgprc_

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRadiobuttonReportSortByTimeToggle(self):

        if self.radiobutton_ReportSortByTime.isChecked():
            self.appData.settings.enum_ReportSortBy = 1;

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRadiobuttonReportSortByMTToggle(self):

        if self.radiobutton_ReportSortByMT.isChecked():
            self.appData.settings.enum_ReportSortBy = 2;

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportBeginDateSelect(self):

        self.appData.settings.date_ReportBeginDate = self.calender_ReportBeginDate.selectedDate()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportEndDateSelect(self):

        self.appData.settings.date_ReportEndDate = self.calender_ReportEndDate.selectedDate()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportBeginTimeSelect(self):

        self.appData.settings.time_ReportBeginTime = self.timeedit_ReportBeginTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportEndTimeSelect(self):

        self.appData.settings.time_ReportEndTime = self.timeedit_ReportEndTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonGenerateDetailedRep(self):

        self.button_GenerateRep.setEnabled(False)

        self.appData.window_MainWindow.signal_GenerateDetailedRep.emit()    # -> SUPERVISOR.msgprc_OnStartGeneration

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnReportFinished(self):

        self.button_GenerateRep.setEnabled(True)

    ####################################################################################################################








