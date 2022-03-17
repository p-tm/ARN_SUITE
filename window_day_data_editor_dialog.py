########################################################################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGroupBox

from PyQt5.QtGui import QIcon

from copy import copy

########################################################################################################################

from window_shifts_editor_dialog import WINDOW_SHIFTS_EDITOR_DIALOG


########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WINDOW_DAY_DATA_EDITOR_DIALOG(QDialog):

    signal_UpdateVar_AllVars = pyqtSignal()

    ####################################################################################################################

    def __init__(self,app_data):

        super().__init__()

        self.appData = app_data



        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.groupbox_Upper = QGroupBox()
        self.groupbox_Upper.setLayout(QVBoxLayout())

        self.groupbox_Lower = QGroupBox()
        self.groupbox_Lower.setLayout(QHBoxLayout())


        self.widget_Date = QWidget()
        self.widget_Date.setLayout(QHBoxLayout())
        self.label_Date = QLabel()
        self.field_Date = QLabel()

        self.widget_ShiftPlan = QWidget()
        self.widget_ShiftPlan.setLayout(QHBoxLayout())
        self.label_ShiftPlan = QLabel()
        self.combobox_ShiftPlan = QComboBox()

        self.widget_IsHoliday = QWidget()
        self.widget_IsHoliday.setLayout(QHBoxLayout())
        self.checkbox_IsHoliday = QCheckBox()

        self.button_LaunchShiftEditor = QPushButton()
        self.button_OK = QPushButton()
        self.button_Cancel = QPushButton()



        self.initUI()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        self.setWindowTitle("Редактор расписания")
        #self.setMinimumWidth(300)
        #self.setMinimumHeight(300)

        self.setFixedSize(300, 300)

        self.layout_CoreLayout.addWidget(self.groupbox_Upper)
        self.layout_CoreLayout.addWidget(self.groupbox_Lower)



        self.label_Date.setText("Дата:")
        self.label_ShiftPlan.setText("План смен")
        self.checkbox_IsHoliday.setText("Праздничный день")

        self.widget_Date.layout().addWidget(self.label_Date)
        self.widget_Date.layout().addStretch(1)
        self.widget_Date.layout().addWidget(self.field_Date)

        self.widget_ShiftPlan.layout().addWidget(self.label_ShiftPlan)
        self.widget_ShiftPlan.layout().addStretch(1)
        self.widget_ShiftPlan.layout().addWidget(self.combobox_ShiftPlan)

        self.widget_IsHoliday.layout().addWidget(self.checkbox_IsHoliday)
        self.widget_IsHoliday.layout().addStretch(1)


        self.groupbox_Upper.layout().addWidget(self.widget_Date)
        self.groupbox_Upper.layout().addWidget(self.widget_ShiftPlan)
        self.groupbox_Upper.layout().addWidget(self.widget_IsHoliday)
        self.groupbox_Upper.layout().addStretch(1)


        self.button_LaunchShiftEditor.setText("Редактор смены")
        self.button_OK.setText("ОК")
        self.button_Cancel.setText("Отмена")

        #self.button_LaunchShiftEditor.setMinimumHeight(40)
        #self.button_OK.setMinimumHeight(40)
        #self.button_Cancel.setMinimumHeight(40)

        #self.button_LaunchShiftEditor.setMinimumWidth(80)
        #self.button_OK.setMinimumWidth(80)
        #self.button_Cancel.setMinimumWidth(80)

        self.groupbox_Lower.layout().addStretch(1)
        self.groupbox_Lower.layout().addWidget(self.button_LaunchShiftEditor)
        self.groupbox_Lower.layout().addWidget(self.button_OK)
        self.groupbox_Lower.layout().addWidget(self.button_Cancel)

        #

        self.field_Date.setText(self.appData.viewer_DAY.date.toString("dd.MM.yyyy"))

        self.combobox_ShiftPlan.addItem(self.appData.SHIFTS_PLANS[0].plan_tag, self.appData.SHIFTS_PLANS[0].plan_id)
        self.combobox_ShiftPlan.addItem(self.appData.SHIFTS_PLANS[1].plan_tag, self.appData.SHIFTS_PLANS[1].plan_id)

        self.combobox_ShiftPlan.setItemData(0, self.appData.SHIFTS_PLANS[0].plan_id, Qt.UserRole)
        self.combobox_ShiftPlan.setItemData(1, self.appData.SHIFTS_PLANS[1].plan_id, Qt.UserRole)

        self.combobox_ShiftPlan.setCurrentIndex(self.appData.editor_DAY.plan_id-1)

        self.checkbox_IsHoliday.setChecked(self.appData.editor_DAY.is_holiday)




    ####################################################################################################################

    def connectSignals(self):

        self.combobox_ShiftPlan.currentIndexChanged.connect(self.msgprc_UserUpdateShiftPlan)
        self.checkbox_IsHoliday.stateChanged.connect(self.msgprc_UserUpdateIsHoliday)

        self.button_LaunchShiftEditor.clicked.connect(self.msgprc_OnLaunchShiftEditor)
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

    @pyqtSlot()
    def msgprc_UserUpdateShiftPlan(self):

        self.appData.editor_DAY.plan_id = self.combobox_ShiftPlan.itemData(self.combobox_ShiftPlan.currentIndex(), Qt.UserRole)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UserUpdateIsHoliday(self):

        self.appData.editor_DAY.is_holiday = self.checkbox_IsHoliday.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnLaunchShiftEditor(self):

        self.appData.editor_DAY = copy(self.appData.viewer_DAY)

        dlg = WINDOW_SHIFTS_EDITOR_DIALOG(self.appData, self.appData.editor_DAY)

        dlg.move(
            self.appData.window_MainWindow.x() + self.appData.window_MainWindow.width() / 2 - dlg.width() / 2,
            self.appData.window_MainWindow.y() + self.appData.window_MainWindow.height() / 2 - dlg.height() / 2
        )


        dlg.exec_()

    ####################################################################################################################








