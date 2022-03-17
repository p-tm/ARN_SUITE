########################################################################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGroupBox

from PyQt5.QtGui import QIcon

########################################################################################################################

from widget_shift_editor import WIDGET_SHIFT_EDITOR


########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WINDOW_SHIFTS_EDITOR_DIALOG(QDialog):

    signal_UpdateVar_AllVars = pyqtSignal()

    ####################################################################################################################

    def __init__(self, app_data, day):

        super().__init__()

        self.appData = app_data
        self.day = day

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        shift_plan = self.day.plan_id

        self.S1 = WIDGET_SHIFT_EDITOR(self.day.SHIFTS[0])
        self.S2 = WIDGET_SHIFT_EDITOR(self.day.SHIFTS[1])
        self.S3 = WIDGET_SHIFT_EDITOR(self.day.SHIFTS[2], True)  # can be night
        self.S4 = WIDGET_SHIFT_EDITOR(self.day.SHIFTS[3])
        self.S5 = WIDGET_SHIFT_EDITOR(self.day.SHIFTS[4])


        self.groupbox_ButtonPanel = QGroupBox()
        self.groupbox_ButtonPanel.setLayout(QHBoxLayout())

        self.button_OK = QPushButton()
        self.button_Cancel = QPushButton()


        self.initUI()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        self.setWindowTitle("Редактор сменного расписания на дату: " + self.day.date.toString("dd.MM.yyyy"))
        #self.setFixedSize(600, 300)

        if self.day.plan_id == 1:
            self.layout.addWidget(self.S1)
            self.layout.addWidget(self.S2)
            self.layout.addWidget(self.S3)
            self.layout.addStretch(1)
        if self.day.plan_id == 2:
            self.layout.addWidget(self.S4)
            self.layout.addWidget(self.S5)
            self.layout.addStretch(1)



        self.button_OK.setText("OK")
        self.button_Cancel.setText("Отмена")

        self.groupbox_ButtonPanel.layout().addStretch(1)
        self.groupbox_ButtonPanel.layout().addWidget(self.button_OK)
        self.groupbox_ButtonPanel.layout().addWidget(self.button_Cancel)

        self.layout.addWidget(self.groupbox_ButtonPanel)

    ####################################################################################################################

    def connectSignals(self):

        self.button_OK.clicked.connect(self.msgprc_OnOK)
        self.button_Cancel.clicked.connect(self.msgprc_OnCancel)

        self.signal_UpdateVar_AllVars.connect(self.appData.worker_MCycle.msgprc_OnUpdateVar_AllVars)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnOK(self):

        self.signal_UpdateVar_AllVars.emit()
        self.close()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCancel(self):

        self.close()

    ####################################################################################################################

