########################################################################################################################

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDir
from PyQt5.QtCore import QFileInfo

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox



########################################################################################################################

from window_date_picker_dialog import WINDOW_DATE_PICKER_DIALOG

########################################################################################################################
# описание класса:
# - виджет для вкладки "Настройки"
#
########################################################################################################################

class WIDGET_ARGATE_PANE_SETTINGS(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)



        #self.widget_Row_0 = QWidget()
        #self.layout_Row_0 = QVBoxLayout()
        #self.widget_Row_0.setLayout(self.layout_Row_0)

        #self.layout_CoreLayout.addWidget(self.widget_Row_0)
        #self.layout_CoreLayout.addStretch(1)

        self.groupbox_ReportsGen = QGroupBox(self)
        self.groupbox_ReportsGen.setTitle("Генерация отчётов")

        self.groupbox_ReportsSettings = QGroupBox(self)
        self.groupbox_ReportsSettings.setTitle("Сохранение отчётов")

        self.layout_CoreLayout.addWidget(self.groupbox_ReportsGen)
        self.layout_CoreLayout.addWidget(self.groupbox_ReportsSettings)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        btn = QPushButton()
        btn.setText("Сохранить")
        btn.clicked.connect(self.msgprc_OnSaveSettings)
        wdg.layout().addStretch(1)
        wdg.layout().addWidget(btn)
        self.layout_CoreLayout.addWidget(wdg)

        self.layout_CoreLayout.addStretch(1)

        # Groupbox "Генерация отчётов"

        self.layout_GroupboxReportsGen = QVBoxLayout()
        self.groupbox_ReportsGen.setLayout(self.layout_GroupboxReportsGen)

        self.widget_GroupboxReportsGen_StartDate = QWidget()
        self.widget_GroupboxReportsGen_DailyReports = QWidget()
        self.widget_GroupboxReportsGen_MonthReports = QWidget()
        self.widget_GroupboxReportsGen_YearReports = QWidget()
        self.checkbox_Show12hShifts = QCheckBox()

        self.layout_GroupboxReportsGen_StartDate = QHBoxLayout()
        self.layout_GroupboxReportsGen_DailyReports = QHBoxLayout()
        self.layout_GroupboxReportsGen_MonthReports = QHBoxLayout()
        self.layout_GroupboxReportsGen_YearReports = QHBoxLayout()

        self.widget_GroupboxReportsGen_StartDate.setLayout(self.layout_GroupboxReportsGen_StartDate)
        self.widget_GroupboxReportsGen_DailyReports.setLayout(self.layout_GroupboxReportsGen_DailyReports)
        self.widget_GroupboxReportsGen_MonthReports.setLayout(self.layout_GroupboxReportsGen_MonthReports)
        self.widget_GroupboxReportsGen_YearReports.setLayout(self.layout_GroupboxReportsGen_YearReports)

        self.layout_GroupboxReportsGen.addWidget(self.widget_GroupboxReportsGen_StartDate)
        self.layout_GroupboxReportsGen.addWidget(self.widget_GroupboxReportsGen_DailyReports)
        self.layout_GroupboxReportsGen.addWidget(self.widget_GroupboxReportsGen_MonthReports)
        self.layout_GroupboxReportsGen.addWidget(self.widget_GroupboxReportsGen_YearReports)
        self.layout_GroupboxReportsGen.addWidget(self.checkbox_Show12hShifts)
        self.layout_GroupboxReportsGen.addStretch(1)

        self.label_StartDate = QLabel()
        #self.datepick_StartDate = QCalendarWidget()
        self.edit_StartDate = QLineEdit()
        self.button_StartDate = QPushButton()

        self.label_DailyReports = QLabel()
        self.timeedit_DailyReports = QTimeEdit()
        self.label_DailyReports_2 = QLabel()

        self.label_MonthReports = QLabel()
        self.timeedit_MonthReports = QTimeEdit()
        self.label_MonthReports_2 = QLabel()

        self.label_YearReports = QLabel()
        self.timeedit_YearReports = QTimeEdit()
        self.label_YearReports_2 = QLabel()



        self.layout_GroupboxReportsGen_StartDate.addWidget(self.label_StartDate)
        self.layout_GroupboxReportsGen_StartDate.addWidget(self.edit_StartDate)
        self.layout_GroupboxReportsGen_StartDate.addWidget(self.button_StartDate)
        self.layout_GroupboxReportsGen_StartDate.addStretch(1)

        self.layout_GroupboxReportsGen_DailyReports.addWidget(self.label_DailyReports)
        self.layout_GroupboxReportsGen_DailyReports.addWidget(self.timeedit_DailyReports)
        self.layout_GroupboxReportsGen_DailyReports.addWidget(self.label_DailyReports_2)
        self.layout_GroupboxReportsGen_DailyReports.addStretch(1)

        self.layout_GroupboxReportsGen_MonthReports.addWidget(self.label_MonthReports)
        self.layout_GroupboxReportsGen_MonthReports.addWidget(self.timeedit_MonthReports)
        self.layout_GroupboxReportsGen_MonthReports.addWidget(self.label_MonthReports_2)
        self.layout_GroupboxReportsGen_MonthReports.addStretch(1)

        self.layout_GroupboxReportsGen_YearReports.addWidget(self.label_YearReports)
        self.layout_GroupboxReportsGen_YearReports.addWidget(self.timeedit_YearReports)
        self.layout_GroupboxReportsGen_YearReports.addWidget(self.label_YearReports_2)
        self.layout_GroupboxReportsGen_YearReports.addStretch(1)

        self.label_StartDate.setText("Начальная дата")
        self.edit_StartDate.setText(self.appData.settings.reportStartDate.toString("dd.MM.yyyy"))
        self.button_StartDate.setText("...")

        self.label_DailyReports.setText("Генерация ежедневных отчётов:")
        self.label_DailyReports_2.setText("текущего дня")

        self.label_MonthReports.setText("Генерация ежемесячных отчётов:")
        self.label_MonthReports_2.setText("последнего дня текущего месяца")

        self.label_YearReports.setText("Генерация ежегодных отчётов:")
        self.label_YearReports_2.setText("31 декабря текущего года")

        self.label_StartDate.setMinimumWidth(200)
        self.label_DailyReports.setMinimumWidth(200)
        self.label_MonthReports.setMinimumWidth(200)
        self.label_YearReports.setMinimumWidth(200)

        self.edit_StartDate.setMinimumWidth(100)
        self.timeedit_DailyReports.setMinimumWidth(100)
        self.timeedit_MonthReports.setMinimumWidth(100)
        self.timeedit_YearReports.setMinimumWidth(100)

        self.timeedit_DailyReports.setDisplayFormat("hh:mm:ss")
        self.timeedit_MonthReports.setDisplayFormat("hh:mm:ss")
        self.timeedit_YearReports.setDisplayFormat("hh:mm:ss")

        self.checkbox_Show12hShifts.setText("Отображать в отчёте типа #1 информацию о 12-часовых сменах")

        self.edit_StartDate.setReadOnly(True)
        self.button_StartDate.setFixedWidth(30)

        # initialization

        self.timeedit_DailyReports.setTime(self.appData.settings.dailyReportTime)
        self.timeedit_MonthReports.setTime(self.appData.settings.monthReportTime)
        self.timeedit_YearReports.setTime(self.appData.settings.yearReportTime)
        self.checkbox_Show12hShifts.setChecked(self.appData.settings.show12hShiftsInReportT1)









        # Groupbox "Сохранение отчётов"

        self.checkbox_KeepOnServer = QCheckBox()
        self.label_FilePathEdit = QLabel()
        self.widget_ReportsSettingsFilePath = QWidget()

        self.lineedit_FilePathEdit = QLineEdit()
        self.button_FilePathDialog = QPushButton()

        self.label_DestinationEmail = QLabel()
        self.lineedit_DestinationEmail = QLineEdit()




        self.layout_GroupboxReportsSettings = QVBoxLayout()
        self.groupbox_ReportsSettings.setLayout( self.layout_GroupboxReportsSettings)

        self.layout_ReportsSettingsFilePath = QHBoxLayout()
        self.widget_ReportsSettingsFilePath.setLayout(self.layout_ReportsSettingsFilePath)

        self.layout_GroupboxReportsSettings.addWidget(self.checkbox_KeepOnServer)
        self.layout_GroupboxReportsSettings.addWidget(self.label_FilePathEdit)
        self.layout_GroupboxReportsSettings.addWidget(self.widget_ReportsSettingsFilePath)
        self.layout_GroupboxReportsSettings.addWidget(self.label_DestinationEmail)
        self.layout_GroupboxReportsSettings.addWidget(self.lineedit_DestinationEmail)
        self.layout_GroupboxReportsSettings.addStretch(1)

        self.layout_ReportsSettingsFilePath.addWidget(self.lineedit_FilePathEdit)
        self.layout_ReportsSettingsFilePath.addWidget(self.button_FilePathDialog)

        self.checkbox_KeepOnServer.setText("Сохранять копии отчётов на сервере")
        self.label_FilePathEdit.setText("Папка для хранения копий отчётов")
        self.button_FilePathDialog.setText("...")
        self.label_DestinationEmail.setText("Адрес e-mail для отправки отчётов")

        self.button_FilePathDialog.setFixedWidth(30)

        # initialization

        self.checkbox_KeepOnServer.setChecked(self.appData.settings.keepCopyOfReportFileOnServer)
        self.lineedit_FilePathEdit.setText(self.appData.settings.dirForReportFiles)
        self.lineedit_DestinationEmail.setText(self.appData.settings.destEmail)
        self.checkbox_Show12hShifts.setChecked(self.appData.settings.show12hShiftsInReportT1)

        # connect handlers

        self.checkbox_KeepOnServer.clicked.connect(self.msgprc_OnCheckboxKeepReportFilesClicked)
        self.button_FilePathDialog.clicked.connect(self.msgprc_OnButtonOpenFileDialogPressed)

        self.button_StartDate.clicked.connect(self.msgprc_OnButtonStartDateSelectPressed)

        self.timeedit_DailyReports.timeChanged.connect(self.msgprc_OnDailyReportTimeTimeChanged)
        self.timeedit_MonthReports.timeChanged.connect(self.msgprc_OnMonthReportTimeTimeChanged)
        self.timeedit_YearReports.timeChanged.connect(self.msgprc_OnYearReportTimeTimeChanged)

        self.checkbox_Show12hShifts.clicked.connect(self.msgprc_OnCheckboxShow12hShiftsClicked)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonOpenFileDialogPressed(self):

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        #if dialog.exec_():

        directory = QDir()
        directory = QFileDialog.getExistingDirectory()
        self.lineedit_FilePathEdit.setText(directory)

        self.appData.settings.dirForReportFiles = directory

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCheckboxKeepReportFilesClicked(self):

        do_keep = self.checkbox_KeepOnServer.isChecked()

        self.appData.settings.keepCopyOfReportFileOnServer = int(do_keep)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDailyReportTimeTimeChanged(self):

        self.appData.settings.dailyReportTime = self.timeedit_DailyReports.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnMonthReportTimeTimeChanged(self):

        self.appData.settings.monthReportTime = self.timeedit_MonthReports.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnYearReportTimeTimeChanged(self):

        self.appData.settings.yearReportTime = self.timeedit_YearReports.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnButtonStartDateSelectPressed(self):

        dlg = WINDOW_DATE_PICKER_DIALOG(self.appData)
        dlg.setWindowTitle("Выбор стартовой даты")
        dlg.move(
            self.appData.window_MainWindow.x() + self.appData.window_MainWindow.width()/2 - dlg.width()/2,
            self.appData.window_MainWindow.y() + self.appData.window_MainWindow.height()/2 - dlg.height()/2
        )
        dlg.exec_()

        self.edit_StartDate.setText(self.appData.settings.reportStartDate.toString("dd.MM.yyyy"))

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCheckboxShow12hShiftsClicked(self):

        do_show = self.checkbox_Show12hShifts.isChecked()

        self.appData.settings.show12hShiftsInReportT1 = int(do_show)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnSaveSettings(self):

        self.appData.window_MainWindow.saveSettings()

        msgbox = QMessageBox(self)
        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
        msgbox.setWindowTitle("Инфо")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setText(
            "Настройки сохранены")
        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
        msgbox.setStandardButtons(QMessageBox.Ok)

        msgbox.exec_()





