########################################################################################################################

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel

from PyQt5.QtCore import Qt

########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WINDOW_DATE_PICKER_DIALOG(QDialog):

    def __init__(self,app_data):

        super().__init__()

        self.appData = app_data

        self.label_Caption = QLabel()
        self.datepick_Calender = QCalendarWidget()

        self.widget_ButtonPanel = QWidget()
        self.button_OK = QPushButton()
        self.button_Cancel = QPushButton()

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.layout_CoreLayout.addWidget(self.label_Caption)
        self.layout_CoreLayout.addWidget(self.datepick_Calender)
        self.layout_CoreLayout.addStretch(1)
        self.layout_CoreLayout.addWidget(self.widget_ButtonPanel)



        self.layout_ButtonPanelLayout = QHBoxLayout()
        self.widget_ButtonPanel.setLayout(self.layout_ButtonPanelLayout)

        self.layout_ButtonPanelLayout.addStretch(1)
        self.layout_ButtonPanelLayout.addWidget(self.button_OK)
        self.layout_ButtonPanelLayout.addWidget(self.button_Cancel)



        self.label_Caption.setText("Выбор даты")

        self.initUI()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        #self.setWindowFlags(self.windowFlags() & ~Qt::WindowContextHelpButtonHint)

        w_flags = self.windowFlags()
        w_flags = w_flags & ~Qt.WindowContextHelpButtonHint

        self.setWindowFlags(w_flags)

        self.button_OK.setText("OK")
        self.button_Cancel.setText("Отмена")

        self.button_OK.setMinimumWidth(60)
        self.button_OK.setMinimumHeight(30)

        self.button_Cancel.setMinimumWidth(60)
        self.button_Cancel.setMinimumHeight(30)

        self.datepick_Calender.setSelectedDate(self.appData.settings.reportStartDate)
        self.selected_date = self.appData.settings.reportStartDate

    ####################################################################################################################

    def connectSignals(self):

        self.button_OK.pressed.connect(self.msgprc_OnOk)
        self.button_Cancel.pressed.connect(self.msgprc_OnCancel)

        self.datepick_Calender.clicked.connect(self.msgprc_OnDataSelect)

    ####################################################################################################################

    def msgprc_OnOk(self):

        self.appData.settings.reportStartDate = self.selected_date
        self.close()

    ####################################################################################################################

    def msgprc_OnCancel(self):

        self.close()

    ####################################################################################################################

    def msgprc_OnDataSelect(self):

        self.selected_date = self.datepick_Calender.selectedDate()

    ####################################################################################################################

