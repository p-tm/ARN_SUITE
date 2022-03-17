########################################################################################################################

from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import pyqtSlot


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QCheckBox

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush



########################################################################################################################

from udt_lamp import *
from udt_lamp_in_a_box import UDT_LAMP_IN_A_BOX



########################################################################################################################
# описание класса:
# - виджет для вкладки "Мониторинг полевого оборудования"
#
########################################################################################################################

TREEWIDGET_STYLESHEET = """
                QTreeView::item {
                    background-color: rgb(240,240,240);
                    border-left: 1px solid rgb(192,192,192);
                }

                QTreeView::item:alternate {
                    background: rgb(255,255,255);
                }

                QTreeView::item::selected {
                    background-color: rgb(128,192,220);
                    color: rgb(0,0,0);
                }

                QTreeView QHeaderView:section {
                   background-color: rgb(255,255,255);
                   color: rgb(0,0,0);
                   border-left: 1px solid rgb(192,192,192);
               }

                QTreeView::branch {
                   background: rgb(255,0,0);
                }

                QTreeView::branch::selected {
                    background: rgb(128,192,220);
                }                

        #        QTreeView::branch:alternate {
        #            background: rgb(255,255,0);
        #        }
        #
                """

STYLESHEET_TABLE_CELL_LABEL_TIME = """
    QLabel {
        color: #404040;
        padding-left: 20px;
        padding-top: 0px;
        padding-right: 0px;
        padding-bottom: 0px
    }
"""

########################################################################################################################

class UDT_ALL_WIDGETS_FOR_MT():

    def __init__(self, lamp_shape):

        self.lamp_ONL1 = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.GREEN, sh=lamp_shape, pl=0)
        self.lamp_ALR_SUM = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW, sh=lamp_shape, pl=1)
        self.lamp_STP_SUM = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)
        self.lamp_ONL2 = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.GREEN, sh=lamp_shape, pl=0)
        self.lamp_ALR_FAILURE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW, sh=lamp_shape, pl=1)
        self.lamp_ALR_MATERIAL = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW, sh=lamp_shape, pl=1)
        self.lamp_STP_FAILURE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)
        self.lamp_STP_MATERIAL = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)
        self.lamp_STP_PROCESS = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)
        self.lamp_STP_QUALITY = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)

        self.lamps = [self.lamp_ONL1,
                      self.lamp_ALR_SUM,
                      self.lamp_STP_SUM,
                      self.lamp_ONL2,
                      self.lamp_ALR_FAILURE,
                      self.lamp_ALR_MATERIAL,
                      self.lamp_STP_FAILURE,
                      self.lamp_STP_MATERIAL,
                      self.lamp_STP_PROCESS,
                      self.lamp_STP_QUALITY]

        self.time_ALR_FAILURE = QLabel()
        self.time_ALR_MATERIAL = QLabel()
        self.time_STP_FAILURE = QLabel()
        self.time_STP_MATERIAL = QLabel()
        self.time_STP_PROCESS = QLabel()
        self.time_STP_QUALITY = QLabel()

        self.times = [QLabel(),
                      QLabel(),
                      QLabel(),
                      QLabel(),
                      self.time_ALR_FAILURE,
                      self.time_ALR_MATERIAL,
                      self.time_STP_FAILURE,
                      self.time_STP_MATERIAL,
                      self.time_STP_PROCESS,
                      self.time_STP_QUALITY]

        self.time_ALR_FAILURE.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)
        self.time_ALR_MATERIAL.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)
        self.time_STP_FAILURE.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)
        self.time_STP_MATERIAL.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)
        self.time_STP_PROCESS.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)
        self.time_STP_QUALITY.setStyleSheet(STYLESHEET_TABLE_CELL_LABEL_TIME)


########################################################################################################################

class UDT_STYLED_ITEM_DELEGATE(QStyledItemDelegate):

    def sizeHint(self, option, index):

        s = super().sizeHint(option, index)

        #if index.parent().isValid():
        #    s.setHeight(10)
        #else:
        #    s.setHeight(80)
        #return s



########################################################################################################################

class WIDGET_ARTERM_PANE_FIELD_MONITOR(QWidget):

    ####################################################################################################################

    def __init__(self, app_data, lamp_shape):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QGridLayout()
        self.setLayout(self.layout_CoreLayout)

        self.tree_Tree = QTreeWidget()

        self.tree_Tree.setColumnCount(6)

        self.tree_Tree.setColumnWidth(0, 3)
        self.tree_Tree.setColumnWidth(1, 3)
        self.tree_Tree.setColumnWidth(2, 3)
        self.tree_Tree.setColumnWidth(3, 320)
        self.tree_Tree.setColumnWidth(4, 60)
        self.tree_Tree.setColumnWidth(5, 200)




        self.tree_Tree.setTreePosition(3)
        self.startItemCell = self.tree_Tree.treePosition()



        self.tree_Tree.setHeaderLabels(["С","Т","П","Станок","Сост.","Время с момента нажатия кнопки"])
        #sstr = self.tree_Tree.header().data[0][0]


        self.treeitem_Workshop = QTreeWidgetItem(self.tree_Tree)
        self.treeitem_Workshop.setText(self.startItemCell,"Участок металлообработки")
        #self.treeitem_Workshop.setIcon(0,QIcon("C:/Users/Pavel/AppData/Local/Programs/Python/Python38/logo_arneg_russia.png"))
        #self.treeitem_Workshop.setText(self.startItemCell + 3, "qwe")

        #self.tree_Tree.addTopLevelItem(self.treeitem_Workshop)

        self.treeitem_MT01 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT02 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT03 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT04 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT05 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT06 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT07 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT08 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT09 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT10 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT11 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT12 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT13 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT14 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT15 = QTreeWidgetItem(self.treeitem_Workshop)
        self.treeitem_MT16 = QTreeWidgetItem(self.treeitem_Workshop)



        self.treeitem_MT01_ONLINE = QTreeWidgetItem(self.treeitem_MT01)
        self.treeitem_MT01_ALR = QTreeWidgetItem(self.treeitem_MT01)
        self.treeitem_MT01_STP = QTreeWidgetItem(self.treeitem_MT01)

        self.treeitem_MT02_ONLINE = QTreeWidgetItem(self.treeitem_MT02)
        self.treeitem_MT02_ALR = QTreeWidgetItem(self.treeitem_MT02)
        self.treeitem_MT02_STP = QTreeWidgetItem(self.treeitem_MT02)

        self.treeitem_MT03_ONLINE = QTreeWidgetItem(self.treeitem_MT03)
        self.treeitem_MT03_ALR = QTreeWidgetItem(self.treeitem_MT03)
        self.treeitem_MT03_STP = QTreeWidgetItem(self.treeitem_MT03)

        self.treeitem_MT04_ONLINE = QTreeWidgetItem(self.treeitem_MT04)
        self.treeitem_MT04_ALR = QTreeWidgetItem(self.treeitem_MT04)
        self.treeitem_MT04_STP = QTreeWidgetItem(self.treeitem_MT04)

        self.treeitem_MT05_ONLINE = QTreeWidgetItem(self.treeitem_MT05)
        self.treeitem_MT05_ALR = QTreeWidgetItem(self.treeitem_MT05)
        self.treeitem_MT05_STP = QTreeWidgetItem(self.treeitem_MT05)

        self.treeitem_MT06_ONLINE = QTreeWidgetItem(self.treeitem_MT06)
        self.treeitem_MT06_ALR = QTreeWidgetItem(self.treeitem_MT06)
        self.treeitem_MT06_STP = QTreeWidgetItem(self.treeitem_MT06)

        self.treeitem_MT07_ONLINE = QTreeWidgetItem(self.treeitem_MT07)
        self.treeitem_MT07_ALR = QTreeWidgetItem(self.treeitem_MT07)
        self.treeitem_MT07_STP = QTreeWidgetItem(self.treeitem_MT07)

        self.treeitem_MT08_ONLINE = QTreeWidgetItem(self.treeitem_MT08)
        self.treeitem_MT08_ALR = QTreeWidgetItem(self.treeitem_MT08)
        self.treeitem_MT08_STP = QTreeWidgetItem(self.treeitem_MT08)

        self.treeitem_MT09_ONLINE = QTreeWidgetItem(self.treeitem_MT09)
        self.treeitem_MT09_ALR = QTreeWidgetItem(self.treeitem_MT09)
        self.treeitem_MT09_STP = QTreeWidgetItem(self.treeitem_MT09)

        self.treeitem_MT10_ONLINE = QTreeWidgetItem(self.treeitem_MT10)
        self.treeitem_MT10_ALR = QTreeWidgetItem(self.treeitem_MT10)
        self.treeitem_MT10_STP = QTreeWidgetItem(self.treeitem_MT10)

        self.treeitem_MT11_ONLINE = QTreeWidgetItem(self.treeitem_MT11)
        self.treeitem_MT11_ALR = QTreeWidgetItem(self.treeitem_MT11)
        self.treeitem_MT11_STP = QTreeWidgetItem(self.treeitem_MT11)

        self.treeitem_MT12_ONLINE = QTreeWidgetItem(self.treeitem_MT12)
        self.treeitem_MT12_ALR = QTreeWidgetItem(self.treeitem_MT12)
        self.treeitem_MT12_STP = QTreeWidgetItem(self.treeitem_MT12)

        self.treeitem_MT13_ONLINE = QTreeWidgetItem(self.treeitem_MT13)
        self.treeitem_MT13_ALR = QTreeWidgetItem(self.treeitem_MT13)
        self.treeitem_MT13_STP = QTreeWidgetItem(self.treeitem_MT13)

        self.treeitem_MT14_ONLINE = QTreeWidgetItem(self.treeitem_MT14)
        self.treeitem_MT14_ALR = QTreeWidgetItem(self.treeitem_MT14)
        self.treeitem_MT14_STP = QTreeWidgetItem(self.treeitem_MT14)

        self.treeitem_MT15_ONLINE = QTreeWidgetItem(self.treeitem_MT15)
        self.treeitem_MT15_ALR = QTreeWidgetItem(self.treeitem_MT15)
        self.treeitem_MT15_STP = QTreeWidgetItem(self.treeitem_MT15)

        self.treeitem_MT16_ONLINE = QTreeWidgetItem(self.treeitem_MT16)
        self.treeitem_MT16_ALR = QTreeWidgetItem(self.treeitem_MT16)
        self.treeitem_MT16_STP = QTreeWidgetItem(self.treeitem_MT16)







        self.treeitem_MT01_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT01_ALR)
        self.treeitem_MT01_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT01_ALR)
        self.treeitem_MT01_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT01_STP)
        self.treeitem_MT01_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT01_STP)
        self.treeitem_MT01_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT01_STP)
        self.treeitem_MT01_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT01_STP)

        self.treeitem_MT02_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT02_ALR)
        self.treeitem_MT02_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT02_ALR)
        self.treeitem_MT02_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT02_STP)
        self.treeitem_MT02_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT02_STP)
        self.treeitem_MT02_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT02_STP)
        self.treeitem_MT02_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT02_STP)

        self.treeitem_MT03_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT03_ALR)
        self.treeitem_MT03_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT03_ALR)
        self.treeitem_MT03_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT03_STP)
        self.treeitem_MT03_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT03_STP)
        self.treeitem_MT03_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT03_STP)
        self.treeitem_MT03_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT03_STP)

        self.treeitem_MT04_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT04_ALR)
        self.treeitem_MT04_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT04_ALR)
        self.treeitem_MT04_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT04_STP)
        self.treeitem_MT04_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT04_STP)
        self.treeitem_MT04_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT04_STP)
        self.treeitem_MT04_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT04_STP)

        self.treeitem_MT05_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT05_ALR)
        self.treeitem_MT05_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT05_ALR)
        self.treeitem_MT05_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT05_STP)
        self.treeitem_MT05_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT05_STP)
        self.treeitem_MT05_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT05_STP)
        self.treeitem_MT05_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT05_STP)

        self.treeitem_MT06_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT06_ALR)
        self.treeitem_MT06_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT06_ALR)
        self.treeitem_MT06_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT06_STP)
        self.treeitem_MT06_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT06_STP)
        self.treeitem_MT06_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT06_STP)
        self.treeitem_MT06_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT06_STP)

        self.treeitem_MT07_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT07_ALR)
        self.treeitem_MT07_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT07_ALR)
        self.treeitem_MT07_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT07_STP)
        self.treeitem_MT07_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT07_STP)
        self.treeitem_MT07_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT07_STP)
        self.treeitem_MT07_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT07_STP)

        self.treeitem_MT08_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT08_ALR)
        self.treeitem_MT08_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT08_ALR)
        self.treeitem_MT08_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT08_STP)
        self.treeitem_MT08_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT08_STP)
        self.treeitem_MT08_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT08_STP)
        self.treeitem_MT08_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT08_STP)

        self.treeitem_MT09_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT09_ALR)
        self.treeitem_MT09_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT09_ALR)
        self.treeitem_MT09_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT09_STP)
        self.treeitem_MT09_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT09_STP)
        self.treeitem_MT09_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT09_STP)
        self.treeitem_MT09_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT09_STP)

        self.treeitem_MT10_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT10_ALR)
        self.treeitem_MT10_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT10_ALR)
        self.treeitem_MT10_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT10_STP)
        self.treeitem_MT10_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT10_STP)
        self.treeitem_MT10_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT10_STP)
        self.treeitem_MT10_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT10_STP)

        self.treeitem_MT11_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT11_ALR)
        self.treeitem_MT11_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT11_ALR)
        self.treeitem_MT11_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT11_STP)
        self.treeitem_MT11_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT11_STP)
        self.treeitem_MT11_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT11_STP)
        self.treeitem_MT11_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT11_STP)

        self.treeitem_MT12_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT12_ALR)
        self.treeitem_MT12_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT12_ALR)
        self.treeitem_MT12_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT12_STP)
        self.treeitem_MT12_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT12_STP)
        self.treeitem_MT12_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT12_STP)
        self.treeitem_MT12_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT12_STP)

        self.treeitem_MT13_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT13_ALR)
        self.treeitem_MT13_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT13_ALR)
        self.treeitem_MT13_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT13_STP)
        self.treeitem_MT13_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT13_STP)
        self.treeitem_MT13_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT13_STP)
        self.treeitem_MT13_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT13_STP)

        self.treeitem_MT14_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT14_ALR)
        self.treeitem_MT14_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT14_ALR)
        self.treeitem_MT14_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT14_STP)
        self.treeitem_MT14_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT14_STP)
        self.treeitem_MT14_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT14_STP)
        self.treeitem_MT14_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT14_STP)

        self.treeitem_MT15_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT15_ALR)
        self.treeitem_MT15_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT15_ALR)
        self.treeitem_MT15_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT15_STP)
        self.treeitem_MT15_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT15_STP)
        self.treeitem_MT15_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT15_STP)
        self.treeitem_MT15_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT15_STP)
        
        self.treeitem_MT16_ALR_FAILURE = QTreeWidgetItem(self.treeitem_MT16_ALR)
        self.treeitem_MT16_ALR_MATERIAL = QTreeWidgetItem(self.treeitem_MT16_ALR)
        self.treeitem_MT16_STP_FAILURE = QTreeWidgetItem(self.treeitem_MT16_STP)
        self.treeitem_MT16_STP_MATERIAL = QTreeWidgetItem(self.treeitem_MT16_STP)
        self.treeitem_MT16_STP_PROCESS = QTreeWidgetItem(self.treeitem_MT16_STP)
        self.treeitem_MT16_STP_QUALITY = QTreeWidgetItem(self.treeitem_MT16_STP)



        #self.tree_Tree.setFirstColumnSpanned(0, QModelIndex(), True)


        #lamp_ONLINE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.GREEN,sh=ENM_LAMP_SHAPE.ROUND,pl=0)
        #lamp_ALR_FAILURE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW,sh=ENM_LAMP_SHAPE.SQUARED,pl=1)
        #lamp_ALR_MATERIAL = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW,sh=ENM_LAMP_SHAPE.SQUARED,pl=1)
        #lamp_STP_FAILURE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW,sh=ENM_LAMP_SHAPE.SQUARED,pl=1)
        #lamp_STP_PROCESS = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW,sh=ENM_LAMP_SHAPE.SQUARED,pl=1)
        #lamp_STP_QUALITY = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW,sh=ENM_LAMP_SHAPE.SQUARED,pl=1)

        #lamp_ONLINE = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.GREEN,pl=1)

        lamp_ALR_SUM = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.YELLOW, sh=lamp_shape, pl=1)
        lamp_STP_SUM = UDT_LAMP_IN_A_BOX(cl=ENM_LAMP_COLOR.RED, sh=lamp_shape, pl=1)

        self.lamps_Workshop = [lamp_ALR_SUM,lamp_STP_SUM]

        self.widgets_MT01 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT02 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT03 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT04 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT05 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT06 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT07 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT08 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT09 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT10 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT11 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT12 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT13 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT14 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT15 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)
        self.widgets_MT16 = UDT_ALL_WIDGETS_FOR_MT(lamp_shape)

        #lamp_ONLINE.lamp.on = True
        #lamp_ALR_FAILURE.lamp.on = True

        self.tree_Tree.setItemWidget(self.treeitem_Workshop, self.startItemCell - 2, self.lamps_Workshop[0])
        self.tree_Tree.setItemWidget(self.treeitem_Workshop, self.startItemCell - 1, self.lamps_Workshop[1])

        lamps = self.widgets_MT01

        self.tree_Tree.setItemWidget(self.treeitem_MT01, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT01, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT01, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT01

        self.tree_Tree.setItemWidget(self.treeitem_MT01_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT01_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT02

        self.tree_Tree.setItemWidget(self.treeitem_MT02, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT02, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT02, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT02

        self.tree_Tree.setItemWidget(self.treeitem_MT02_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT02_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT03

        self.tree_Tree.setItemWidget(self.treeitem_MT03, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT03, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT03, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT03

        self.tree_Tree.setItemWidget(self.treeitem_MT03_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT03_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT04

        self.tree_Tree.setItemWidget(self.treeitem_MT04, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT04, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT04, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT04

        self.tree_Tree.setItemWidget(self.treeitem_MT04_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT04_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT05

        self.tree_Tree.setItemWidget(self.treeitem_MT05, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT05, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT05, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT05

        self.tree_Tree.setItemWidget(self.treeitem_MT05_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT05_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT06

        self.tree_Tree.setItemWidget(self.treeitem_MT06, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT06, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT06, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT06

        self.tree_Tree.setItemWidget(self.treeitem_MT06_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT06_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT07

        self.tree_Tree.setItemWidget(self.treeitem_MT07, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT07, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT07, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT07

        self.tree_Tree.setItemWidget(self.treeitem_MT07_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT07_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT08

        self.tree_Tree.setItemWidget(self.treeitem_MT08, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT08, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT08, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT08

        self.tree_Tree.setItemWidget(self.treeitem_MT08_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT08_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT09

        self.tree_Tree.setItemWidget(self.treeitem_MT09, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT09, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT09, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT09

        self.tree_Tree.setItemWidget(self.treeitem_MT09_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT09_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT10

        self.tree_Tree.setItemWidget(self.treeitem_MT10, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT10, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT10, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT10

        self.tree_Tree.setItemWidget(self.treeitem_MT10_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT10_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT11

        self.tree_Tree.setItemWidget(self.treeitem_MT11, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT11, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT11, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT11

        self.tree_Tree.setItemWidget(self.treeitem_MT11_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT11_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT12

        self.tree_Tree.setItemWidget(self.treeitem_MT12, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT12, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT12, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT12

        self.tree_Tree.setItemWidget(self.treeitem_MT12_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT12_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT13

        self.tree_Tree.setItemWidget(self.treeitem_MT13, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT13, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT13, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT13

        self.tree_Tree.setItemWidget(self.treeitem_MT13_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT13_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT14

        self.tree_Tree.setItemWidget(self.treeitem_MT14, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT14, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT14, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT14

        self.tree_Tree.setItemWidget(self.treeitem_MT14_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT14_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT15

        self.tree_Tree.setItemWidget(self.treeitem_MT15, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT15, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT15, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT15

        self.tree_Tree.setItemWidget(self.treeitem_MT15_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT15_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        lamps = self.widgets_MT16

        self.tree_Tree.setItemWidget(self.treeitem_MT16, self.startItemCell - 3, lamps.lamp_ONL1)
        self.tree_Tree.setItemWidget(self.treeitem_MT16, self.startItemCell - 2, lamps.lamp_ALR_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT16, self.startItemCell - 1, lamps.lamp_STP_SUM)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_ONLINE, self.startItemCell + 1, lamps.lamp_ONL2)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_ALR_FAILURE, self.startItemCell + 1, lamps.lamp_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_ALR_MATERIAL, self.startItemCell + 1, lamps.lamp_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_FAILURE, self.startItemCell + 1, lamps.lamp_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_MATERIAL, self.startItemCell + 1, lamps.lamp_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_PROCESS, self.startItemCell + 1, lamps.lamp_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_QUALITY, self.startItemCell + 1, lamps.lamp_STP_QUALITY)

        times = self.widgets_MT16

        self.tree_Tree.setItemWidget(self.treeitem_MT16_ALR_FAILURE, self.startItemCell + 2, times.time_ALR_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_ALR_MATERIAL, self.startItemCell + 2, times.time_ALR_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_FAILURE, self.startItemCell + 2, times.time_STP_FAILURE)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_MATERIAL, self.startItemCell + 2, times.time_STP_MATERIAL)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_PROCESS, self.startItemCell + 2, times.time_STP_PROCESS)
        self.tree_Tree.setItemWidget(self.treeitem_MT16_STP_QUALITY, self.startItemCell + 2, times.time_STP_QUALITY)


        #self.label_Test1 = QLabel("label #1")
        #self.label_Test2 = QLabel("label #2")
        #self.lamp_Test1 = UDT_LAMP()

        self.initUI()

    ####################################################################################################################

    def initUI(self):

        self.layout_CoreLayout.addWidget(self.tree_Tree, 0, 0, 10, 1)

        #self.layout_CoreLayout.addWidget(self.label_Test1, 0, 1, 1, 1)
        #self.layout_CoreLayout.addWidget(self.label_Test2, 1, 1, 1, 1)
        #self.layout_CoreLayout.addWidget(self.lamp_Test1, 2, 1, 1, 1)



        self.treeitem_MT01.setText(self.startItemCell, "mt01")
        self.treeitem_MT02.setText(self.startItemCell, "mt02")
        self.treeitem_MT03.setText(self.startItemCell, "mt03")
        self.treeitem_MT04.setText(self.startItemCell, "mt04")
        self.treeitem_MT05.setText(self.startItemCell, "mt05")
        self.treeitem_MT06.setText(self.startItemCell, "mt06")
        self.treeitem_MT07.setText(self.startItemCell, "mt07")
        self.treeitem_MT08.setText(self.startItemCell, "mt08")
        self.treeitem_MT09.setText(self.startItemCell, "mt09")
        self.treeitem_MT10.setText(self.startItemCell, "mt10")
        self.treeitem_MT11.setText(self.startItemCell, "mt11")
        self.treeitem_MT12.setText(self.startItemCell, "mt12")
        self.treeitem_MT13.setText(self.startItemCell, "mt13")
        self.treeitem_MT14.setText(self.startItemCell, "mt14")
        self.treeitem_MT15.setText(self.startItemCell, "mt15")
        self.treeitem_MT16.setText(self.startItemCell, "mt16")


        self.treeitem_MT01_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT01_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT01_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT01_ALR_FAILURE.setText(self.startItemCell,"поломка")
        self.treeitem_MT01_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT01_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT01_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT01_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT01_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT02_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT02_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT02_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT02_ALR_FAILURE.setText(self.startItemCell,"поломка")
        self.treeitem_MT02_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT02_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT02_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT02_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT02_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT03_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT03_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT03_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT03_ALR_FAILURE.setText(self.startItemCell,"поломка")
        self.treeitem_MT03_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT03_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT03_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT03_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT03_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT04_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT04_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT04_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT04_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT04_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT04_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT04_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT04_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT04_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT05_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT05_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT05_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT05_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT05_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT05_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT05_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT05_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT05_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT06_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT06_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT06_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT06_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT06_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT06_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT06_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT06_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT06_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT07_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT07_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT07_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT07_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT07_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT07_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT07_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT07_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT07_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT08_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT08_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT08_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT08_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT08_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT08_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT08_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT08_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT08_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT09_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT09_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT09_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT09_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT09_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT09_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT09_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT09_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT09_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT10_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT10_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT10_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT10_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT10_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT10_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT10_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT10_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT10_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT11_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT11_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT11_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT11_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT11_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT11_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT11_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT11_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT11_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT12_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT12_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT12_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT12_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT12_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT12_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT12_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT12_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT12_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT13_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT13_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT13_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT13_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT13_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT13_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT13_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT13_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT13_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT14_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT14_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT14_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT14_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT14_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT14_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT14_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT14_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT14_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT15_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT15_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT15_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT15_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT15_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT15_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT15_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT15_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT15_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_MT16_ONLINE.setText(self.startItemCell, "Включен (связь установлена)")
        self.treeitem_MT16_ALR.setText(self.startItemCell, "Тревога")
        self.treeitem_MT16_STP.setText(self.startItemCell, "Остановка")

        self.treeitem_MT16_ALR_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT16_ALR_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT16_STP_FAILURE.setText(self.startItemCell, "поломка")
        self.treeitem_MT16_STP_MATERIAL.setText(self.startItemCell, "материал")
        self.treeitem_MT16_STP_PROCESS.setText(self.startItemCell, "процесс")
        self.treeitem_MT16_STP_QUALITY.setText(self.startItemCell, "качество")


        self.treeitem_Workshop.setExpanded(True)
        self.treeitem_MT01.setExpanded(False)
        self.treeitem_MT02.setExpanded(False)
        self.treeitem_MT03.setExpanded(False)
        self.treeitem_MT04.setExpanded(False)
        self.treeitem_MT05.setExpanded(False)
        self.treeitem_MT06.setExpanded(False)
        self.treeitem_MT07.setExpanded(False)
        self.treeitem_MT08.setExpanded(False)
        self.treeitem_MT09.setExpanded(False)
        self.treeitem_MT10.setExpanded(False)
        self.treeitem_MT11.setExpanded(False)
        self.treeitem_MT12.setExpanded(False)
        self.treeitem_MT13.setExpanded(False)
        self.treeitem_MT14.setExpanded(False)
        self.treeitem_MT15.setExpanded(False)
        self.treeitem_MT16.setExpanded(False)


        #self.tree_Tree.expandAll()

        # разообраться с этим позже
        #delegate = UDT_STYLED_ITEM_DELEGATE(self.tree_Tree)
        #self.tree_Tree.setItemDelegate(delegate)
        #self.setStyleSheet(TREEWIDGET_STYLESHEET)
        #self.tree_Tree.setAlternatingRowColors(True)

        #self.lamp_Test1.repaint()
        #self.lamp_Test1.update() # оба сигнала работают




        #self.update()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        #

        if self.appData.MACHINE_TOOLS.count() > 0:
            self.treeitem_MT01.setText(self.startItemCell, "01 - " + self.appData.MACHINE_TOOLS[0].tag + " - " + self.appData.MACHINE_TOOLS[0].caption + " (" + self.appData.MACHINE_TOOLS[0].mt_class + ")")
            self.treeitem_MT02.setText(self.startItemCell, "02 - " + self.appData.MACHINE_TOOLS[1].tag + " - " + self.appData.MACHINE_TOOLS[1].caption + " (" + self.appData.MACHINE_TOOLS[1].mt_class + ")")
            self.treeitem_MT03.setText(self.startItemCell, "03 - " + self.appData.MACHINE_TOOLS[2].tag + " - " + self.appData.MACHINE_TOOLS[2].caption + " (" + self.appData.MACHINE_TOOLS[2].mt_class + ")")
            self.treeitem_MT04.setText(self.startItemCell, "04 - " + self.appData.MACHINE_TOOLS[3].tag + " - " + self.appData.MACHINE_TOOLS[3].caption + " (" + self.appData.MACHINE_TOOLS[3].mt_class + ")")
            self.treeitem_MT05.setText(self.startItemCell, "05 - " + self.appData.MACHINE_TOOLS[4].tag + " - " + self.appData.MACHINE_TOOLS[4].caption + " (" + self.appData.MACHINE_TOOLS[4].mt_class + ")")
            self.treeitem_MT06.setText(self.startItemCell, "06 - " + self.appData.MACHINE_TOOLS[5].tag + " - " + self.appData.MACHINE_TOOLS[5].caption + " (" + self.appData.MACHINE_TOOLS[5].mt_class + ")")
            self.treeitem_MT07.setText(self.startItemCell, "07 - " + self.appData.MACHINE_TOOLS[6].tag + " - " + self.appData.MACHINE_TOOLS[6].caption + " (" + self.appData.MACHINE_TOOLS[6].mt_class + ")")
            self.treeitem_MT08.setText(self.startItemCell, "08 - " + self.appData.MACHINE_TOOLS[7].tag + " - " + self.appData.MACHINE_TOOLS[7].caption + " (" + self.appData.MACHINE_TOOLS[7].mt_class + ")")
            self.treeitem_MT09.setText(self.startItemCell, "09 - " + self.appData.MACHINE_TOOLS[8].tag + " - " + self.appData.MACHINE_TOOLS[8].caption + " (" + self.appData.MACHINE_TOOLS[8].mt_class + ")")
            self.treeitem_MT10.setText(self.startItemCell, "10 - " + self.appData.MACHINE_TOOLS[9].tag + " - " + self.appData.MACHINE_TOOLS[9].caption + " (" + self.appData.MACHINE_TOOLS[9].mt_class + ")")
            self.treeitem_MT11.setText(self.startItemCell, "11 - " + self.appData.MACHINE_TOOLS[10].tag + " - " + self.appData.MACHINE_TOOLS[10].caption + " (" + self.appData.MACHINE_TOOLS[10].mt_class + ")")
            self.treeitem_MT12.setText(self.startItemCell, "12 - " + self.appData.MACHINE_TOOLS[11].tag + " - " + self.appData.MACHINE_TOOLS[11].caption + " (" + self.appData.MACHINE_TOOLS[11].mt_class + ")")
            self.treeitem_MT13.setText(self.startItemCell, "13 - " + self.appData.MACHINE_TOOLS[12].tag + " - " + self.appData.MACHINE_TOOLS[12].caption + " (" + self.appData.MACHINE_TOOLS[12].mt_class + ")")
            self.treeitem_MT14.setText(self.startItemCell, "14 - " + self.appData.MACHINE_TOOLS[13].tag + " - " + self.appData.MACHINE_TOOLS[13].caption + " (" + self.appData.MACHINE_TOOLS[13].mt_class + ")")
            self.treeitem_MT15.setText(self.startItemCell, "15 - " + self.appData.MACHINE_TOOLS[14].tag + " - " + self.appData.MACHINE_TOOLS[14].caption + " (" + self.appData.MACHINE_TOOLS[14].mt_class + ")")
            self.treeitem_MT16.setText(self.startItemCell, "16 - " + self.appData.MACHINE_TOOLS[15].tag + " - " + self.appData.MACHINE_TOOLS[15].caption + " (" + self.appData.MACHINE_TOOLS[15].mt_class + ")")

        #

        color_WorkshopItem      = QColor("#D0D0FF")
        color_OddMTitem         = QColor("#F0FFF0")
        color_EvenMTitem        = QColor("#FAFFFA")

        #self.treeitem_Workshop.setBackground(0, color_WorkshopItem)
        #self.treeitem_Workshop.setBackground(1, color_WorkshopItem)
        #self.treeitem_Workshop.setBackground(2, color_WorkshopItem)
        #self.treeitem_Workshop.setBackground(3, color_WorkshopItem)
        #self.treeitem_Workshop.setBackground(4, color_WorkshopItem)
        #self.treeitem_Workshop.setBackground(5, color_WorkshopItem)
        #
        #
        #self.treeitem_MT01.setBackground(0, color_OddMTitem)
        #self.treeitem_MT01.setBackground(1, color_OddMTitem)
        #self.treeitem_MT01.setBackground(2, color_OddMTitem)
        #self.treeitem_MT01.setBackground(3, color_OddMTitem)
        #self.treeitem_MT01.setBackground(4, color_OddMTitem)
        #self.treeitem_MT01.setBackground(5, color_OddMTitem)
        #
        #self.treeitem_MT02.setBackground(0, color_EvenMTitem)
        #self.treeitem_MT02.setBackground(1, color_EvenMTitem)
        #self.treeitem_MT02.setBackground(2, color_EvenMTitem)
        #self.treeitem_MT02.setBackground(3, color_EvenMTitem)
        #self.treeitem_MT02.setBackground(4, color_EvenMTitem)
        #self.treeitem_MT02.setBackground(5, color_EvenMTitem)

        #

        self.lamps_Workshop[0].lamp.on = self.appData.CD.LAMP_WORKSHOP_YELLOW
        self.lamps_Workshop[1].lamp.on = self.appData.CD.LAMP_WORKSHOP_RED

        #

        k = 0

        self.widgets_MT01.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT01.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT01.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT01.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT01.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT01.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT01.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT01.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT01.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT01.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT01.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT01.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT01.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT01.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT01.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT01.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 1

        self.widgets_MT02.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT02.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT02.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT02.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT02.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT02.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT02.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT02.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT02.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT02.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT02.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT02.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT02.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT02.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT02.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT02.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 2

        self.widgets_MT03.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT03.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT03.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT03.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT03.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT03.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT03.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT03.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT03.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT03.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT03.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT03.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT03.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT03.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT03.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT03.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 3

        self.widgets_MT04.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT04.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT04.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT04.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT04.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT04.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT04.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT04.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT04.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT04.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT04.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT04.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT04.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT04.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT04.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT04.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 4

        self.widgets_MT05.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT05.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT05.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT05.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT05.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT05.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT05.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT05.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT05.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT05.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT05.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT05.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT05.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT05.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT05.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT05.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 5

        self.widgets_MT06.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT06.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT06.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT06.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT06.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT06.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT06.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT06.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT06.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT06.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT06.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT06.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT06.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT06.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT06.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT06.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 6

        self.widgets_MT07.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT07.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT07.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT07.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT07.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT07.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT07.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT07.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT07.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT07.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT07.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT07.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT07.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT07.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT07.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT07.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 7

        self.widgets_MT08.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT08.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT08.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT08.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT08.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT08.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT08.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT08.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT08.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT08.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT08.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT08.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT08.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT08.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT08.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT08.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 8

        self.widgets_MT09.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT09.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT09.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT09.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT09.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT09.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT09.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT09.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT09.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT09.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT09.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT09.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT09.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT09.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT09.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT09.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 9

        self.widgets_MT10.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT10.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT10.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT10.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT10.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT10.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT10.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT10.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT10.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT10.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT10.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT10.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT10.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT10.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT10.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT10.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 10

        self.widgets_MT11.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT11.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT11.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT11.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT11.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT11.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT11.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT11.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT11.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT11.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT11.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT11.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT11.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT11.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT11.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT11.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 11

        self.widgets_MT12.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT12.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT12.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT12.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT12.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT12.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT12.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT12.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT12.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT12.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT12.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT12.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT12.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT12.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT12.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT12.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 12

        self.widgets_MT13.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT13.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT13.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT13.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT13.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT13.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT13.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT13.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT13.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT13.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT13.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT13.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT13.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT13.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT13.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT13.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 13

        self.widgets_MT14.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT14.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT14.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT14.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT14.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT14.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT14.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT14.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT14.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT14.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT14.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT14.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT14.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT14.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT14.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT14.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 14

        self.widgets_MT15.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT15.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT15.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT15.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT15.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT15.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT15.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT15.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT15.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT15.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT15.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT15.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT15.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT15.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT15.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT15.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        k = 15

        self.widgets_MT16.lamps[0].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT16.lamps[1].lamp.on = self.appData.CD.MT_INFO[k].com_yellow
        self.widgets_MT16.lamps[2].lamp.on = self.appData.CD.MT_INFO[k].com_red
        self.widgets_MT16.lamps[3].lamp.on = not self.appData.CD.MT_INFO[k].offline
        self.widgets_MT16.lamps[4].lamp.on = self.appData.CD.MT_INFO[k].alr_failure
        self.widgets_MT16.lamps[5].lamp.on = self.appData.CD.MT_INFO[k].alr_material
        self.widgets_MT16.lamps[6].lamp.on = self.appData.CD.MT_INFO[k].stp_failure
        self.widgets_MT16.lamps[7].lamp.on = self.appData.CD.MT_INFO[k].stp_material
        self.widgets_MT16.lamps[8].lamp.on = self.appData.CD.MT_INFO[k].stp_process
        self.widgets_MT16.lamps[9].lamp.on = self.appData.CD.MT_INFO[k].stp_quality

        self.widgets_MT16.times[4].setText(self.appData.CD.MT_STAT[0][k].alr_failure.strHMS())
        self.widgets_MT16.times[5].setText(self.appData.CD.MT_STAT[0][k].alr_material.strHMS())
        self.widgets_MT16.times[6].setText(self.appData.CD.MT_STAT[0][k].stp_failure.strHMS())
        self.widgets_MT16.times[7].setText(self.appData.CD.MT_STAT[0][k].stp_material.strHMS())
        self.widgets_MT16.times[8].setText(self.appData.CD.MT_STAT[0][k].stp_process.strHMS())
        self.widgets_MT16.times[9].setText(self.appData.CD.MT_STAT[0][k].stp_quality.strHMS())

        #

        #self.lamps_MT01.lamp_ONL1.lamp.blinker = self.appData.LAMP_BLINKER.Q
        #self.lamps_MT01.lamp_ALR_SUM.blinker = self.appData.LAMP_BLINKER.Q

        for lmp in self.lamps_Workshop:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT01.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT02.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT03.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT04.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT05.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT06.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT07.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT08.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT09.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT10.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT11.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT12.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT13.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT14.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT15.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q
        for lmp in self.widgets_MT16.lamps:
            lmp.lamp.blinker = self.appData.LAMP_BLINKER.Q

        #

        #self.tree_Tree.update()



        self.tree_Tree.model().layoutChanged.emit()

        #self.update()

    ####################################################################################################################






