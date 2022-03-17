########################################################################################################################

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableView

########################################################################################################################

from global_functions import *
from udt_table_model_classes import *


########################################################################################################################
# описание класса:
# - виджет для вкладки "Главная"
#
########################################################################################################################

class WIDGET_ARTERM_PANE_BASIC(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QGridLayout()
        self.setLayout(self.layout_CoreLayout)

        self.prefillComDataTable()

        self.table1 = QTableView()
        self.l1 = QLabel()
        self.b1 = QPushButton()
        self.b2 = QPushButton()
        self.thr_start = QPushButton()
        self.thr_fin = QPushButton()

        self.table1.setModel(self.appData.model_ComDataTable)




        self.layout_CoreLayout.addWidget(self.table1, 0, 0, 1, 3)


        self.initUI()

    ####################################################################################################################

    def initUI(self):

        self.table1.verticalHeader().hide()
        #self.table1.horizontalHeader().hide()

        ww = self.table1.width()

        self.table1.setColumnWidth(0, 300)
        self.table1.setColumnWidth(1, 150)
        self.table1.setColumnWidth(2, ww-450)

    ####################################################################################################################

    def prefillComDataTable(self):

        # <header>

        self.appData.model_ComDataTable.header.append("")
        self.appData.model_ComDataTable.header.append("")
        self.appData.model_ComDataTable.header.append("")

        # <body>
        # current date
        current_row = 0
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущая дата")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.DATE, self.appData.CD.date)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current time
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущее время")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.appData.CD.time)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current weekday
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущий день недели")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # weekday features
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "День недели: рабочий/выходной")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # holiday
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Праздничный день")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)



        # shift format
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "План смен")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.appData.CD.shiftPlanCaption)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current shift
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Текущая смена")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.appData.CD.shiftCaption)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current shift - begin
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Начало смены")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.appData.CD.curShiftBTime)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current shift - end
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Конец смены")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.appData.CD.curShiftETime)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # break
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Перерыв")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current scheduled brake
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Название перерыва")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, self.appData.CD.scheduledBreakCaption)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current scheduled break - begin
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Начало перерыва")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.appData.CD.curScheduledBreakBTime)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # current scheduled break - end
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Конец перерыва")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.TIME, self.appData.CD.curScheduledBreakBTime)
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # is dinner
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Обеденный перерыв")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        # is working shift
        current_row += 1
        rec = UDT_TABLE_RECORD()
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "Рабочая смена")
        rec.append(UDT_TABLE_CELL(current_row, 0, dat))
        dat = UDT_TABLE_CELL_DATA(ENM_TABLE_DATA_TYPE.STRING, "")
        dat.textAlignment = Qt.AlignRight | Qt.AlignVCenter
        rec.append(UDT_TABLE_CELL(current_row, 1, dat))
        rec.append(UDT_TABLE_CELL(current_row, 2, UDT_TABLE_CELL_DATA()))

        self.appData.model_ComDataTable.body.append(rec)

        cc = self.appData.model_ComDataTable.columnCount(0)
        rr = self.appData.model_ComDataTable.rowCount(0)

        pass

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        #self.appData.CD.date = QDateTime.currentDateTime().date()
        #self.appData.CD.time = QDateTime.currentDateTime().time()

        ww = self.table1.width()
        ww1 = self.table1.columnWidth(0)
        ww2 = self.table1.columnWidth(1)
        self.table1.setColumnWidth(2, ww-ww1-ww2)





        # also updates all other fields, so changes data on day change, shift change, etc.

        self.appData.model_ComDataTable.body[0][1].data.value = self.appData.CD.date
        self.appData.model_ComDataTable.body[1][1].data.value = self.appData.CD.time
        self.appData.model_ComDataTable.body[2][1].data.value = GF.weekdayIdToString(self.appData.CD.weekday)
        self.appData.model_ComDataTable.body[3][1].data.value = GF.isWeekendToString(self.appData.CD.isWeekend)
        self.appData.model_ComDataTable.body[4][1].data.value = GF.yes_no_ToString(self.appData.CD.isHoliday)
        self.appData.model_ComDataTable.body[5][1].data.value = self.appData.CD.shiftPlanCaption
        self.appData.model_ComDataTable.body[6][1].data.value = self.appData.CD.shiftCaption
        self.appData.model_ComDataTable.body[7][1].data.value = self.appData.CD.curShiftBTime
        self.appData.model_ComDataTable.body[8][1].data.value = self.appData.CD.curShiftETime
        self.appData.model_ComDataTable.body[9][1].data.value = GF.yes_no_ToString(self.appData.CD.isScheduledBreak)
        self.appData.model_ComDataTable.body[10][1].data.value = self.appData.CD.scheduledBreakCaption
        self.appData.model_ComDataTable.body[11][1].data.value = self.appData.CD.curScheduledBreakBTime
        self.appData.model_ComDataTable.body[12][1].data.value = self.appData.CD.curScheduledBreakETime
        self.appData.model_ComDataTable.body[13][1].data.value = GF.yes_no_ToString(self.appData.CD.isDinner)
        self.appData.model_ComDataTable.body[14][1].data.value = GF.yes_no_ToString(self.appData.CD.isWorkingShift)


        if self.appData.CD.isWeekend:
            self.appData.model_ComDataTable.body[2][1].data.textColor = QColor(255, 0, 0)
            self.appData.model_ComDataTable.body[3][1].data.textColor = QColor(255, 0, 0)
        else:
            self.appData.model_ComDataTable.body[2][1].data.textColor = QColor(0, 0, 0)
            self.appData.model_ComDataTable.body[3][1].data.textColor = QColor(0, 0, 0)


        self.appData.model_ComDataTable.layoutChanged.emit()
        #self.appData.model_ComDataTable.dataChanged.emit(???)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnColumnResized(self): # пока не нашёл соответствующего сигнала

        ww = self.table1.width()
        ww1 = self.table1.columnWidth(0)
        ww2 = self.table1.columnWidth(1)
        self.table1.setColumnWidth(2, ww-ww1-ww2)

    ####################################################################################################################


