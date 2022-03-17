########################################################################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGroupBox

########################################################################################################################



########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WIDGET_SHIFT_EDITOR(QWidget):

    ####################################################################################################################

    def __init__(self, shift, can_be_night=False):

        super().__init__()

        self.shift = shift
        self.can_be_night = can_be_night
        self.br_indent_symbol = "->"

        self.frame = QGroupBox()
        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.layout = QVBoxLayout()
        self.frame.setLayout(self.layout)



        self.label_ShiftWDayNum = QLabel()
        self.label_ShiftCaption = QLabel()
        self.label_ShiftBTime = QLabel()
        self.timeedit_ShiftBTime = QTimeEdit()
        self.label_ShiftETime = QLabel()
        self.timeedit_ShiftETime = QTimeEdit()
        self.widget_Gap_1 = QWidget()
        self.checkbox_IsNight = QCheckBox()
        self.widget_Gap_2 = QWidget()
        self.checkbox_Dummy = QCheckBox()

        self.label_BR1_Indent = QLabel()
        self.label_BR1_Number = QLabel()
        self.label_BR1_Caption = QLabel()
        self.label_BR1_BTime = QLabel()
        self.timeedit_BR1_BTime = QTimeEdit()
        self.label_BR1_ETime = QLabel()
        self.timeedit_BR1_ETime = QTimeEdit()
        self.widget_BR1_Gap1 = QWidget()
        self.checkbox_BR1_Active = QCheckBox()
        self.widget_BR1_Gap2 = QWidget()
        self.checkbox_BR1_IsDinner = QCheckBox()

        self.label_BR2_Indent = QLabel()
        self.label_BR2_Number = QLabel()
        self.label_BR2_Caption = QLabel()
        self.label_BR2_BTime = QLabel()
        self.timeedit_BR2_BTime = QTimeEdit()
        self.label_BR2_ETime = QLabel()
        self.timeedit_BR2_ETime = QTimeEdit()
        self.widget_BR2_Gap1 = QWidget()
        self.checkbox_BR2_Active = QCheckBox()
        self.widget_BR2_Gap2 = QWidget()
        self.checkbox_BR2_IsDinner = QCheckBox()
        
        self.label_BR3_Indent = QLabel()
        self.label_BR3_Number = QLabel()
        self.label_BR3_Caption = QLabel()
        self.label_BR3_BTime = QLabel()
        self.timeedit_BR3_BTime = QTimeEdit()
        self.label_BR3_ETime = QLabel()
        self.timeedit_BR3_ETime = QTimeEdit()
        self.widget_BR3_Gap1 = QWidget()
        self.checkbox_BR3_Active = QCheckBox()
        self.widget_BR3_Gap2 = QWidget()
        self.checkbox_BR3_IsDinner = QCheckBox()
        
        self.label_BR4_Indent = QLabel()
        self.label_BR4_Number = QLabel()
        self.label_BR4_Caption = QLabel()
        self.label_BR4_BTime = QLabel()
        self.timeedit_BR4_BTime = QTimeEdit()
        self.label_BR4_ETime = QLabel()
        self.timeedit_BR4_ETime = QTimeEdit()
        self.widget_BR4_Gap1 = QWidget()
        self.checkbox_BR4_Active = QCheckBox()
        self.widget_BR4_Gap2 = QWidget()
        self.checkbox_BR4_IsDinner = QCheckBox()



        self.widget_shift_record = QWidget()
        self.widget_shift_record.setLayout(QHBoxLayout())

        self.widget_break_1_record = QWidget()
        self.widget_break_1_record.setLayout(QHBoxLayout())

        self.widget_break_2_record = QWidget()
        self.widget_break_2_record.setLayout(QHBoxLayout())

        self.widget_break_3_record = QWidget()
        self.widget_break_3_record.setLayout(QHBoxLayout())

        self.widget_break_4_record = QWidget()
        self.widget_break_4_record.setLayout(QHBoxLayout())







        self.initUI()
        self.connectSignals()
        self.updateUI()



    ####################################################################################################################

    def initUI(self):

        self.layout_CoreLayout.addWidget(self.frame)

        self.layout_CoreLayout.setContentsMargins(20, 0, 20, 0)
        self.layout_CoreLayout.setSpacing(0)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(0)

        self.frame.setTitle(self.shift.shiftCaption)

        self.label_ShiftBTime.setText("нач.смены")
        self.label_ShiftETime.setText("кон.смены")
        self.checkbox_IsNight.setText("ночь")

        self.label_ShiftBTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_ShiftETime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.label_BR1_BTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_BR1_ETime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.label_BR2_BTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_BR2_ETime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.label_BR3_BTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_BR3_ETime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.label_BR4_BTime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_BR4_ETime.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.timeedit_ShiftBTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_ShiftETime.setDisplayFormat("hh:mm:ss")

        self.timeedit_BR1_BTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_BR1_ETime.setDisplayFormat("hh:mm:ss")

        self.timeedit_BR2_BTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_BR2_ETime.setDisplayFormat("hh:mm:ss")

        self.timeedit_BR3_BTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_BR3_ETime.setDisplayFormat("hh:mm:ss")

        self.timeedit_BR4_BTime.setDisplayFormat("hh:mm:ss")
        self.timeedit_BR4_ETime.setDisplayFormat("hh:mm:ss")

        column_1_width = 100
        column_2_width = 50
        column_3_width = 100
        column_4_width = 100
        column_5_width = 100
        column_6_width = 100
        column_7_width = 20
        column_8_width = 100
        column_9_width = 20
        column_10_width = 130



        self.widget_shift_record.layout().addWidget(self.label_ShiftWDayNum)
        #self.widget_shift_record.layout().addWidget(self.label_ShiftCaption)
        self.widget_shift_record.layout().addWidget(self.label_ShiftBTime)
        self.widget_shift_record.layout().addWidget(self.timeedit_ShiftBTime)
        self.widget_shift_record.layout().addWidget(self.label_ShiftETime)
        self.widget_shift_record.layout().addWidget(self.timeedit_ShiftETime)
        self.widget_shift_record.layout().addWidget(self.widget_Gap_1)
        self.widget_shift_record.layout().addWidget(self.checkbox_IsNight)
        self.widget_shift_record.layout().addWidget(self.widget_Gap_2)
        self.widget_shift_record.layout().addWidget(self.checkbox_Dummy)


        #self.label_ShiftWDayNum.setContentsMargins(0, 0, 0, 0)
        #self.label_ShiftCaption.setContentsMargins(0, 0, 0, 0)
        #self.label_ShiftBTime.setContentsMargins(0, 0, 0, 0)
        #self.timeedit_ShiftBTime.setContentsMargins(0, 0, 0, 0)
        #self.label_ShiftETime.setContentsMargins(0, 0, 0, 0)
        #self.timeedit_ShiftETime.setContentsMargins(0, 0, 0, 0)
        #self.widget_Gap_1.setContentsMargins(0, 0, 0, 0)
        #self.checkbox_IsNight.setContentsMargins(0, 0, 0, 0)
        #self.widget_Gap_2.setContentsMargins(0, 0, 0, 0)
        #self.checkbox_Dummy.setContentsMargins(0, 0, 0, 0)


        self.layout.addWidget(self.widget_shift_record)

        self.label_ShiftWDayNum.setFixedWidth(column_1_width)
        #self.label_ShiftCaption.setFixedWidth(column_2_width)
        self.label_ShiftBTime.setFixedWidth(column_3_width)
        self.timeedit_ShiftBTime.setFixedWidth(column_4_width)
        self.label_ShiftETime.setFixedWidth(column_5_width)
        self.timeedit_ShiftETime.setFixedWidth(column_6_width)
        self.widget_Gap_1.setFixedWidth(column_7_width)
        self.checkbox_IsNight.setFixedWidth(column_8_width)
        self.widget_Gap_2.setFixedWidth(column_9_width)
        self.checkbox_Dummy.setFixedWidth(column_10_width)









        self.checkbox_IsNight.setEnabled(self.can_be_night)
        self.checkbox_Dummy.setEnabled(False)



        #

        self.label_BR1_Indent.setText(self.br_indent_symbol)
        self.label_BR1_Number.setText("1")
        self.label_BR1_Caption.setText(self.shift.SCHEDULED_BREAKS[0].breakCaption)
        self.label_BR1_BTime.setText("нач.перерыва")
        self.label_BR1_ETime.setText("кон.перерыва")
        self.checkbox_BR1_Active.setText("действующий")
        self.checkbox_BR1_IsDinner.setText("обеденный перерыв")

        self.widget_break_1_record.layout().addWidget(self.label_BR1_Indent)
        #self.widget_break_1_record.layout().addWidget(self.label_BR1_Number)
        #self.widget_break_1_record.layout().addWidget(self.label_BR1_Caption)
        self.widget_break_1_record.layout().addWidget(self.label_BR1_BTime)
        self.widget_break_1_record.layout().addWidget(self.timeedit_BR1_BTime)
        self.widget_break_1_record.layout().addWidget(self.label_BR1_ETime)
        self.widget_break_1_record.layout().addWidget(self.timeedit_BR1_ETime)
        self.widget_break_1_record.layout().addWidget(self.widget_BR1_Gap1)
        self.widget_break_1_record.layout().addWidget(self.checkbox_BR1_Active)
        self.widget_break_1_record.layout().addWidget(self.widget_BR1_Gap2)
        self.widget_break_1_record.layout().addWidget(self.checkbox_BR1_IsDinner)

        self.layout.addWidget(self.widget_break_1_record)

        self.label_BR1_Indent.setFixedWidth(column_1_width)
        #self.label_BR1_Caption.setFixedWidth(column_2_width)
        self.label_BR1_BTime.setFixedWidth(column_3_width)
        self.timeedit_BR1_BTime.setFixedWidth(column_4_width)
        self.label_BR1_ETime.setFixedWidth(column_5_width)
        self.timeedit_BR1_ETime.setFixedWidth(column_6_width)
        self.widget_BR1_Gap1.setFixedWidth(column_7_width)
        self.checkbox_BR1_Active.setFixedWidth(column_8_width)
        self.widget_BR1_Gap2.setFixedWidth(column_9_width)
        self.checkbox_BR1_IsDinner.setFixedWidth(column_10_width)
        
        #

        self.label_BR2_Indent.setText(self.br_indent_symbol)
        self.label_BR2_Number.setText("2")
        self.label_BR2_Caption.setText(self.shift.SCHEDULED_BREAKS[1].breakCaption)
        self.label_BR2_BTime.setText("нач.перерыва")
        self.label_BR2_ETime.setText("кон.перерыва")
        self.checkbox_BR2_Active.setText("действующий")
        self.checkbox_BR2_IsDinner.setText("обеденный перерыв")

        self.widget_break_2_record.layout().addWidget(self.label_BR2_Indent)
        #self.widget_break_2_record.layout().addWidget(self.label_BR2_Number)
        #self.widget_break_2_record.layout().addWidget(self.label_BR2_Caption)
        self.widget_break_2_record.layout().addWidget(self.label_BR2_BTime)
        self.widget_break_2_record.layout().addWidget(self.timeedit_BR2_BTime)
        self.widget_break_2_record.layout().addWidget(self.label_BR2_ETime)
        self.widget_break_2_record.layout().addWidget(self.timeedit_BR2_ETime)
        self.widget_break_2_record.layout().addWidget(self.widget_BR2_Gap1)
        self.widget_break_2_record.layout().addWidget(self.checkbox_BR2_Active)
        self.widget_break_2_record.layout().addWidget(self.widget_BR2_Gap2)
        self.widget_break_2_record.layout().addWidget(self.checkbox_BR2_IsDinner)

        self.layout.addWidget(self.widget_break_2_record)
        
        self.label_BR2_Indent.setFixedWidth(column_1_width)
        #self.label_BR2_Caption.setFixedWidth(column_2_width)
        self.label_BR2_BTime.setFixedWidth(column_3_width)
        self.timeedit_BR2_BTime.setFixedWidth(column_4_width)
        self.label_BR2_ETime.setFixedWidth(column_5_width)
        self.timeedit_BR2_ETime.setFixedWidth(column_6_width)
        self.widget_BR2_Gap1.setFixedWidth(column_7_width)
        self.checkbox_BR2_Active.setFixedWidth(column_8_width)
        self.widget_BR2_Gap2.setFixedWidth(column_9_width)
        self.checkbox_BR2_IsDinner.setFixedWidth(column_10_width)

        #

        self.label_BR3_Indent.setText(self.br_indent_symbol)
        self.label_BR3_Number.setText("2")
        self.label_BR3_Caption.setText(self.shift.SCHEDULED_BREAKS[1].breakCaption)
        self.label_BR3_BTime.setText("нач.перерыва")
        self.label_BR3_ETime.setText("кон.перерыва")
        self.checkbox_BR3_Active.setText("действующий")
        self.checkbox_BR3_IsDinner.setText("обеденный перерыв")

        self.widget_break_3_record.layout().addWidget(self.label_BR3_Indent)
        #self.widget_break_3_record.layout().addWidget(self.label_BR3_Number)
        #self.widget_break_3_record.layout().addWidget(self.label_BR3_Caption)
        self.widget_break_3_record.layout().addWidget(self.label_BR3_BTime)
        self.widget_break_3_record.layout().addWidget(self.timeedit_BR3_BTime)
        self.widget_break_3_record.layout().addWidget(self.label_BR3_ETime)
        self.widget_break_3_record.layout().addWidget(self.timeedit_BR3_ETime)
        self.widget_break_3_record.layout().addWidget(self.widget_BR3_Gap1)
        self.widget_break_3_record.layout().addWidget(self.checkbox_BR3_Active)
        self.widget_break_3_record.layout().addWidget(self.widget_BR3_Gap2)
        self.widget_break_3_record.layout().addWidget(self.checkbox_BR3_IsDinner)

        self.layout.addWidget(self.widget_break_3_record)
        
        self.label_BR3_Indent.setFixedWidth(column_1_width)
        #self.label_BR3_Caption.setFixedWidth(column_2_width)
        self.label_BR3_BTime.setFixedWidth(column_3_width)
        self.timeedit_BR3_BTime.setFixedWidth(column_4_width)
        self.label_BR3_ETime.setFixedWidth(column_5_width)
        self.timeedit_BR3_ETime.setFixedWidth(column_6_width)
        self.widget_BR3_Gap1.setFixedWidth(column_7_width)
        self.checkbox_BR3_Active.setFixedWidth(column_8_width)
        self.widget_BR3_Gap2.setFixedWidth(column_9_width)
        self.checkbox_BR3_IsDinner.setFixedWidth(column_10_width)
        
        
        
        #

        self.label_BR4_Indent.setText(self.br_indent_symbol)
        self.label_BR4_Number.setText("3")
        self.label_BR4_Caption.setText(self.shift.SCHEDULED_BREAKS[2].breakCaption)
        self.label_BR4_BTime.setText("нач.перерыва")
        self.label_BR4_ETime.setText("кон.перерыва")
        self.checkbox_BR4_Active.setText("действующий")
        self.checkbox_BR4_IsDinner.setText("обеденный перерыв")

        self.widget_break_4_record.layout().addWidget(self.label_BR4_Indent)
        #self.widget_break_4_record.layout().addWidget(self.label_BR4_Number)
        #self.widget_break_4_record.layout().addWidget(self.label_BR4_Caption)
        self.widget_break_4_record.layout().addWidget(self.label_BR4_BTime)
        self.widget_break_4_record.layout().addWidget(self.timeedit_BR4_BTime)
        self.widget_break_4_record.layout().addWidget(self.label_BR4_ETime)
        self.widget_break_4_record.layout().addWidget(self.timeedit_BR4_ETime)
        self.widget_break_4_record.layout().addWidget(self.widget_BR4_Gap1)
        self.widget_break_4_record.layout().addWidget(self.checkbox_BR4_Active)
        self.widget_break_4_record.layout().addWidget(self.widget_BR4_Gap2)
        self.widget_break_4_record.layout().addWidget(self.checkbox_BR4_IsDinner)

        self.layout.addWidget(self.widget_break_4_record)
        
        self.label_BR4_Indent.setFixedWidth(column_1_width)
        #self.label_BR4_Caption.setFixedWidth(column_2_width)
        self.label_BR4_BTime.setFixedWidth(column_3_width)
        self.timeedit_BR4_BTime.setFixedWidth(column_4_width)
        self.label_BR4_ETime.setFixedWidth(column_5_width)
        self.timeedit_BR4_ETime.setFixedWidth(column_6_width)
        self.widget_BR4_Gap1.setFixedWidth(column_7_width)
        self.checkbox_BR4_Active.setFixedWidth(column_8_width)
        self.widget_BR4_Gap2.setFixedWidth(column_9_width)
        self.checkbox_BR4_IsDinner.setFixedWidth(column_10_width)

        #


    ####################################################################################################################

    def connectSignals(self):

        self.timeedit_ShiftBTime.timeChanged.connect(self.msgprc_UpdateVar_ShiftBTime)
        self.timeedit_ShiftETime.timeChanged.connect(self.msgprc_UpdateVar_ShiftETime)
        self.checkbox_IsNight.stateChanged.connect(self.msgprc_UpdateVar_IsNight)

        self.timeedit_BR1_BTime.timeChanged.connect(self.msgprc_UpdateVar_BR1_BTime)
        self.timeedit_BR1_ETime.timeChanged.connect(self.msgprc_UpdateVar_BR1_ETime)
        self.checkbox_BR1_Active.stateChanged.connect(self.msgprc_UpdateVar_BR1_Active)
        self.checkbox_BR1_IsDinner.stateChanged.connect(self.msgprc_UpdateVar_BR1_IsDinner)

        self.timeedit_BR2_BTime.timeChanged.connect(self.msgprc_UpdateVar_BR2_BTime)
        self.timeedit_BR2_ETime.timeChanged.connect(self.msgprc_UpdateVar_BR2_ETime)
        self.checkbox_BR2_Active.stateChanged.connect(self.msgprc_UpdateVar_BR2_Active)
        self.checkbox_BR2_IsDinner.stateChanged.connect(self.msgprc_UpdateVar_BR2_IsDinner)

        self.timeedit_BR3_BTime.timeChanged.connect(self.msgprc_UpdateVar_BR3_BTime)
        self.timeedit_BR3_ETime.timeChanged.connect(self.msgprc_UpdateVar_BR3_ETime)
        self.checkbox_BR3_Active.stateChanged.connect(self.msgprc_UpdateVar_BR3_Active)
        self.checkbox_BR3_IsDinner.stateChanged.connect(self.msgprc_UpdateVar_BR3_IsDinner)

        self.timeedit_BR4_BTime.timeChanged.connect(self.msgprc_UpdateVar_BR4_BTime)
        self.timeedit_BR4_ETime.timeChanged.connect(self.msgprc_UpdateVar_BR4_ETime)
        self.checkbox_BR4_Active.stateChanged.connect(self.msgprc_UpdateVar_BR4_Active)
        self.checkbox_BR4_IsDinner.stateChanged.connect(self.msgprc_UpdateVar_BR4_IsDinner)



    ####################################################################################################################

    def updateUI(self):

        self.label_ShiftWDayNum.setText(self.shift.shiftCaption)
        #self.label_ShiftWDayNum.setText(str(self.shift.shift_number_w_day))
        #self.label_ShiftCaption.setText(self.shift.shiftCaption)

        self.timeedit_ShiftBTime.setTime(self.shift.b_time)
        self.timeedit_ShiftETime.setTime(self.shift.e_time)
        self.checkbox_IsNight.setChecked(self.shift.isNight)

        self.timeedit_BR1_BTime.setTime(self.shift.SCHEDULED_BREAKS[0].b_time)
        self.timeedit_BR1_ETime.setTime(self.shift.SCHEDULED_BREAKS[0].e_time)
        self.checkbox_BR1_Active.setChecked(self.shift.SCHEDULED_BREAKS[0].active)
        self.checkbox_BR1_IsDinner.setChecked(self.shift.SCHEDULED_BREAKS[0].isDinner)

        self.timeedit_BR2_BTime.setTime(self.shift.SCHEDULED_BREAKS[1].b_time)
        self.timeedit_BR2_ETime.setTime(self.shift.SCHEDULED_BREAKS[1].e_time)
        self.checkbox_BR2_Active.setChecked(self.shift.SCHEDULED_BREAKS[1].active)
        self.checkbox_BR2_IsDinner.setChecked(self.shift.SCHEDULED_BREAKS[1].isDinner)

        self.timeedit_BR3_BTime.setTime(self.shift.SCHEDULED_BREAKS[2].b_time)
        self.timeedit_BR3_ETime.setTime(self.shift.SCHEDULED_BREAKS[2].e_time)
        self.checkbox_BR3_Active.setChecked(self.shift.SCHEDULED_BREAKS[2].active)
        self.checkbox_BR3_IsDinner.setChecked(self.shift.SCHEDULED_BREAKS[2].isDinner)

        self.timeedit_BR4_BTime.setTime(self.shift.SCHEDULED_BREAKS[3].b_time)
        self.timeedit_BR4_ETime.setTime(self.shift.SCHEDULED_BREAKS[3].e_time)
        self.checkbox_BR4_Active.setChecked(self.shift.SCHEDULED_BREAKS[3].active)
        self.checkbox_BR4_IsDinner.setChecked(self.shift.SCHEDULED_BREAKS[3].isDinner)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_ShiftBTime(self):

        self.shift.b_time = self.timeedit_ShiftBTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_ShiftETime(self):

        self.shift.e_time = self.timeedit_ShiftETime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_IsNight(self):

        self.shift.isNight = self.checkbox_IsNight.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR1_BTime(self):

        self.shift.SCHEDULED_BREAKS[0].b_time = self.timeedit_BR1_BTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR1_ETime(self):

        self.shift.SCHEDULED_BREAKS[0].e_time = self.timeedit_BR1_ETime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR1_Active(self):

        self.shift.SCHEDULED_BREAKS[0].active = self.checkbox_BR1_Active.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR1_IsDinner(self):

        self.shift.SCHEDULED_BREAKS[0].isDinner = self.checkbox_BR1_IsDinner.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR2_BTime(self):

        self.shift.SCHEDULED_BREAKS[1].b_time = self.timeedit_BR2_BTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR2_ETime(self):

        self.shift.SCHEDULED_BREAKS[1].e_time = self.timeedit_BR2_ETime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR2_Active(self):

        self.shift.SCHEDULED_BREAKS[1].active = self.checkbox_BR2_Active.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR2_IsDinner(self):

        self.shift.SCHEDULED_BREAKS[1].isDinner = self.checkbox_BR2_IsDinner.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR3_BTime(self):

        self.shift.SCHEDULED_BREAKS[2].b_time = self.timeedit_BR3_BTime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR3_ETime(self):
        self.shift.SCHEDULED_BREAKS[2].e_time = self.timeedit_BR3_ETime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR3_Active(self):

        self.shift.SCHEDULED_BREAKS[2].active = self.checkbox_BR3_Active.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR3_IsDinner(self):

        self.shift.SCHEDULED_BREAKS[2].isDinner = self.checkbox_BR3_IsDinner.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR4_BTime(self):

        self.shift.SCHEDULED_BREAKS[3].b_time = self.timeedit_BR4_BTime.time()

        pass

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR4_ETime(self):
        self.shift.SCHEDULED_BREAKS[3].e_time = self.timeedit_BR4_ETime.time()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR4_Active(self):

        self.shift.SCHEDULED_BREAKS[3].active = self.checkbox_BR4_Active.isChecked()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_UpdateVar_BR4_IsDinner(self):

        self.shift.SCHEDULED_BREAKS[3].isDinner = self.checkbox_BR4_IsDinner.isChecked()

    ####################################################################################################################









