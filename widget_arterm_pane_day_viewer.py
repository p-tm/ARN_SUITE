########################################################################################################################

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTableView
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QGroupBox

from copy import copy

########################################################################################################################

from global_functions import *
from udt_table_model_classes import *

from window_day_data_editor_dialog import WINDOW_DAY_DATA_EDITOR_DIALOG
from udt_checkbox_in_a_box import UDT_CHECKBOX_IN_A_BOX



########################################################################################################################
# описание класса:
# - виджет для вкладки ...
#
########################################################################################################################

STYLESHEET_LABEL_DAY_DESCRIPTION = """
    QLabel {
        border: 1px solid gray;
        border-radius: 0px;
        background-color: #FFEEEE;
        padding: 10px 10px 10px 10px;
    }
"""

########################################################################################################################

STYLESHEET_TABLE_CELL_LABEL_BLACK = """
    QLabel {
        padding: 0px 0px 0px 10px;
    }
"""

STYLESHEET_TABLE_CELL_LABEL_RED = """
    QLabel {
        color: #FF0000;
        padding: 0px 0px 0px 10px;
    }
"""
########################################################################################################################

STYLESHEET_CHECKBOX = """
    QCheckBox:disabled {
        background-color: #FF0000;
        color: #FF0000;
    }
    QCheckBox:enabled {
        color: #0000FF;
    }
        
"""

########################################################################################################################

STYLESHEET_BUTTON_PANEL = """
    QGroupBox {
        border: 1px solid #808080;
    }   
"""

########################################################################################################################

class WIDGET_ARTERM_PANE_DAY_VIEWER(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.table_HeadTable = QTableWidget()
        self.table_HeadTable.setRowCount(4) ; self.table_HeadTable.setColumnCount(3)

        self.label_DayDescription = QLabel()

        self.tree_Tree = QTreeWidget()
        self.tree_Tree.setColumnCount(9)
        self.tree_Tree.setMinimumHeight(300)

        self.panel_ButtonPanel = QGroupBox()

        #self.tree_Tree.setHeaderLabels(["1","2","3","4","5","6"])

        #self.treeitem_Shifts = QTreeWidgetItem(self.tree_Tree)
        #self.treeitem_Shifts.setText(0, "Смены")

        # ----------------------------------------------------------------------

        self.tblcell_label_CurrentDate = QLabel()
        self.tblcell_label_CurrentDate.setText("?")

        self.tblcell_label_IsWeekend = QLabel()
        self.tblcell_label_IsWeekend.setText("?")

        self.tblcell_label_IsHoliday = QLabel()
        self.tblcell_label_IsHoliday.setText("?")

        self.tblcell_label_ShiftPlan = QLabel()
        self.tblcell_label_ShiftPlan.setText("?")

        # ----------------------------------------------------------------------

        #self.label_DayDescription.setText("здесь надо прописать\nнаименование праздника")
        self.label_DayDescription.setText("")

        # ----------------------------------------------------------------------

        self.layout_ButtonPanelLayout = QHBoxLayout()
        self.panel_ButtonPanel.setLayout(self.layout_ButtonPanelLayout)

        self.button_LaunchEditor = QPushButton()
        self.button_ApplyChanges = QPushButton()

        # ----------------------------------------------------------------------

        self.boolTest = False

        self.initUI()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        self.layout_CoreLayout.addWidget(self.table_HeadTable)
        self.layout_CoreLayout.addWidget(self.label_DayDescription)
        self.layout_CoreLayout.addWidget(self.tree_Tree)
        self.layout_CoreLayout.addWidget(self.panel_ButtonPanel)
        #self.layout_CoreLayout.addStretch(1)

        self.widgetInserted = True

        # ----------------------------------------------------------------------

        self.table_HeadTable.setHorizontalHeaderLabels(["","",""])
        self.table_HeadTable.verticalHeader().hide()
        self.table_HeadTable.horizontalHeader().hide()

        self.table_HeadTable.horizontalHeader().setFixedHeight(15)
        #self.table_HeadTable.setRowHeight(0,40)
        #self.table_HeadTable.setRowHeight(1, 40)
        #self.table_HeadTable.setColumnWidth(0,200)
        self.table_HeadTable.setFixedHeight(self.table_HeadTable.rowHeight(0) * self.table_HeadTable.rowCount() + 1)
        #self.table_HeadTable.setContentsMargins(20,20,20,20)
        #self.table_HeadTable.verticalScrollBar().setDisabled(True)
        #self.table_HeadTable.horizontalScrollBar().setDisabled(True)
        self.table_HeadTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_HeadTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self.table_HeadTable.setItem(0, 0, QTableWidgetItem("Дата"))
        self.table_HeadTable.setItem(1, 0, QTableWidgetItem("Рабочий/выходной день"))
        self.table_HeadTable.setItem(2, 0, QTableWidgetItem("Праздничный день"))
        self.table_HeadTable.setItem(3, 0, QTableWidgetItem("План смен"))

        self.table_HeadTable.setCellWidget(0, 1, self.tblcell_label_CurrentDate)
        self.table_HeadTable.setCellWidget(1, 1, self.tblcell_label_IsWeekend)
        self.table_HeadTable.setCellWidget(2, 1, self.tblcell_label_IsHoliday)
        self.table_HeadTable.setCellWidget(3, 1, self.tblcell_label_ShiftPlan)

        self.tblcell_label_CurrentDate.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)
        self.tblcell_label_IsWeekend.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)
        self.tblcell_label_IsHoliday.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)
        self.tblcell_label_ShiftPlan.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)

        self.tblcell_label_CurrentDate.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tblcell_label_IsWeekend.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tblcell_label_IsHoliday.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tblcell_label_ShiftPlan.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # ----------------------------------------------------------------------

        self.tree_Tree.setColumnWidth(0, 150)
        self.tree_Tree.setColumnWidth(1, 80)
        self.tree_Tree.setColumnWidth(2, 80)
        self.tree_Tree.setColumnWidth(3, 150)
        self.tree_Tree.setColumnWidth(4, 80)
        self.tree_Tree.setColumnWidth(5, 80)
        self.tree_Tree.setColumnWidth(6, 50)
        self.tree_Tree.setColumnWidth(7, 50)

        # ----------------------------------------------------------------------

        self.label_DayDescription.setStyleSheet(STYLESHEET_LABEL_DAY_DESCRIPTION)

        # ----------------------------------------------------------------------

        self.layout_ButtonPanelLayout.addStretch(1)
        self.layout_ButtonPanelLayout.addWidget(self.button_LaunchEditor)
        self.layout_ButtonPanelLayout.addWidget(self.button_ApplyChanges)

        self.panel_ButtonPanel.setStyleSheet(STYLESHEET_BUTTON_PANEL)

        self.button_LaunchEditor.setText("Редактор")
        self.button_ApplyChanges.setText("Сохранить изменения")

    ####################################################################################################################

    def connectSignals(self):

        self.button_LaunchEditor.clicked.connect(self.msgprc_OnLaunchEditor)
        self.button_ApplyChanges.clicked.connect(self.msgprc_OnApplyChanges)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        if self.appData.CD.date is not None:
            self.tblcell_label_CurrentDate.setText(self.appData.CD.date.toString("dd.MM.yyyy"))

        if self.appData.viewer_DAY.is_holiday is not None:
            if self.appData.viewer_DAY.is_holiday:
            #if self.boolTest:
                if not self.widgetInserted:
                    self.layout_CoreLayout.insertWidget(1, self.label_DayDescription)
                    self.label_DayDescription.setVisible(True)
                    self.label_DayDescription.setText("Праздничный день")
                    self.widgetInserted = True
            else:
                if self.widgetInserted:
                    self.layout_CoreLayout.removeWidget(self.label_DayDescription)
                    self.label_DayDescription.setVisible(False)
                    self.label_DayDescription.setText("???")
                    self.widgetInserted = False




        ww = self.table_HeadTable.width()

        self.table_HeadTable.setColumnWidth(0, 300)
        self.table_HeadTable.setColumnWidth(1, 150)
        self.table_HeadTable.setColumnWidth(2, ww-450)

        # ----------------------------------------------------------------------

        if self.appData.viewer_DAY.date is not None:

            self.tblcell_label_CurrentDate.setText(self.appData.viewer_DAY.date.toString("dd.MM.yyyy"))
            self.tblcell_label_IsWeekend.setText(GF.isWeekendToString(self.appData.viewer_DAY.is_weekend))
            self.tblcell_label_IsHoliday.setText(GF.yes_no_ToString(self.appData.viewer_DAY.is_holiday))
            for pl in self.appData.SHIFTS_PLANS:
                if pl.plan_id == self.appData.viewer_DAY.plan_id:
                    self.appData.viewer_DAY.plan_tag = pl.plan_tag
                    break
            self.tblcell_label_ShiftPlan.setText(self.appData.viewer_DAY.plan_tag)

            if self.appData.viewer_DAY.is_weekend:
                self.tblcell_label_CurrentDate.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_RED)
                self.tblcell_label_IsWeekend.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_RED)
            else:
                self.tblcell_label_CurrentDate.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)
                self.tblcell_label_IsWeekend.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)

            if self.appData.viewer_DAY.is_holiday:
                self.tblcell_label_IsHoliday.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_RED)
            else:
                self.tblcell_label_IsHoliday.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_BLACK)

        # ----------------------------------------------------------------------

        if self.appData.updateDayViewer:

            self.tree_Tree.clear()



            self.tree_Tree.setHeaderLabels(["Смены","Нач.см.","Кон.см.","Перерывы","Нач.пер.","Кон.пер.","Ночь","Обед",""])



            is_weekend = self.appData.viewer_DAY.is_weekend
            is_holiday = self.appData.viewer_DAY.is_holiday
            shift_plan = self.appData.viewer_DAY.plan_id

            if is_weekend or is_holiday:

                pass  # в списке смен ничего нет

            else:

                self.treeitem_Shifts = QTreeWidgetItem(self.tree_Tree)
                self.treeitem_Shifts.setText(0, "Смены")

                for sh in self.appData.viewer_DAY.SHIFTS:

                    if shift_plan == 1: # 8H

                        if sh.shift_type_id == 1 or sh.shift_type_id == 2 or sh.shift_type_id == 3:

                            next_shift_item = QTreeWidgetItem(self.treeitem_Shifts)
                            #next_shift_item.setText(0, str(sh.shift_number_w_day))
                            #next_shift_item.setText(1, sh.shiftCaption)
                            next_shift_item.setText(0, sh.shiftCaption)
                            next_shift_item.setText(1, sh.b_time.toString("hh:mm:ss"))
                            next_shift_item.setText(2, sh.e_time.toString("hh:mm:ss"))
                            chb = UDT_CHECKBOX_IN_A_BOX()
                            chb.checkbox.setDisabled(True)
                            chb.checkbox.setStyleSheet(STYLESHEET_CHECKBOX)
                            chb.checkbox.setChecked(sh.isNight)
                            self.tree_Tree.setItemWidget(next_shift_item,6,chb)

                            kk = 1

                            for br in sh.SCHEDULED_BREAKS:

                                if br.active:
                                    next_break_item = QTreeWidgetItem(next_shift_item)
                                    next_break_item.setText(0, "->")
                                    next_break_item.setText(1, "->")
                                    next_break_item.setText(2, "->")
                                    next_break_item.setText(3, "перерыв " + str(kk))
                                    next_break_item.setText(4, br.b_time.toString("hh:mm:ss"))
                                    next_break_item.setText(5, br.e_time.toString("hh:mm:ss"))
                                    chb = UDT_CHECKBOX_IN_A_BOX()
                                    chb.checkbox.setDisabled(True)
                                    chb.checkbox.setStyleSheet(STYLESHEET_CHECKBOX)
                                    chb.checkbox.setChecked(br.isDinner)
                                    self.tree_Tree.setItemWidget(next_break_item, 7, chb)
                                    kk += 1

                    if shift_plan == 2: # 12H

                        if sh.shift_type_id == 4 or sh.shift_type_id == 5:

                            next_shift_item = QTreeWidgetItem(self.treeitem_Shifts)
                            #next_shift_item.setText(0, str(sh.shift_number_w_day))
                            #next_shift_item.setText(1, sh.shiftCaption)
                            next_shift_item.setText(0, sh.shiftCaption)
                            next_shift_item.setText(1, sh.b_time.toString("hh:mm:ss"))
                            next_shift_item.setText(2, sh.e_time.toString("hh:mm:ss"))
                            chb = UDT_CHECKBOX_IN_A_BOX()
                            chb.checkbox.setDisabled(True)
                            chb.checkbox.setStyleSheet(STYLESHEET_CHECKBOX)
                            chb.checkbox.setChecked(sh.isNight)
                            self.tree_Tree.setItemWidget(next_shift_item,6,chb)

                            kk = 1

                            for br in sh.SCHEDULED_BREAKS:

                                if br.active:
                                    next_break_item = QTreeWidgetItem(next_shift_item)
                                    next_break_item.setText(0, "->")
                                    next_break_item.setText(1, "->")
                                    next_break_item.setText(2, "->")
                                    next_break_item.setText(3, "перерыв " + str(kk))
                                    next_break_item.setText(4, br.b_time.toString("hh:mm:ss"))
                                    next_break_item.setText(5, br.e_time.toString("hh:mm:ss"))
                                    chb = UDT_CHECKBOX_IN_A_BOX()
                                    chb.checkbox.setDisabled(True)
                                    chb.checkbox.setStyleSheet(STYLESHEET_CHECKBOX)
                                    chb.checkbox.setChecked(br.isDinner)
                                    self.tree_Tree.setItemWidget(next_break_item, 7, chb)
                                    kk += 1


            self.tree_Tree.expandAll()


            self.appData.updateDayViewer = False



        # ----------------------------------------------------------------------

        if self.appData.viewer_DAY.date is not None and self.appData.CD.date is not None:
            if self.appData.viewer_DAY.date > self.appData.CD.date:
                if self.appData.ACTIVE_USER.permission_edit:
                    self.button_LaunchEditor.setEnabled(True)
                    self.button_ApplyChanges.setEnabled(True)
                else:
                    self.button_LaunchEditor.setEnabled(False)
                    self.button_ApplyChanges.setEnabled(False)
            else:
                self.button_LaunchEditor.setEnabled(False)
                self.button_ApplyChanges.setEnabled(False)
        else:
            self.button_LaunchEditor.setEnabled(False)
            self.button_ApplyChanges.setEnabled(False)


        #self.table_HeadTable.model().layoutChanged.emit()
        #self.tree_Tree.model().layoutChanged.emit()


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnLaunchEditor(self):

        self.appData.editor_DAY = copy(self.appData.viewer_DAY)

        dlg = WINDOW_DAY_DATA_EDITOR_DIALOG(self.appData)

        dlg.move(
            self.appData.window_MainWindow.x() + self.appData.window_MainWindow.width() / 2 - dlg.width() / 2,
            self.appData.window_MainWindow.y() + self.appData.window_MainWindow.height() / 2 - dlg.height() / 2
        )


        dlg.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnApplyChanges(self):

        self.appData.window_MainWindow.signal_WriteDataForSelectedDay.emit()    # -> worker_DBAccess.msgprc_OnWriteDataForSelectedDay

    ####################################################################################################################
