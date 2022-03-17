#################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QDateTime, QDate, QTime

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor

#################################################################

from enums import *


#################################################################
# описание класса:
#
#################################################################

class UDT_TABLE_CELL_DATA():    # along with data itself
                                # incapsulates other attributes

    def __init__(self, t = ENM_TABLE_DATA_TYPE.UNKNOWN, v = None):

        self.type = t
        self.value = v
        self.editable = False    # for probable future use
        self.editorType = None
        self.textColor = QColor(0, 0, 0)
        self.bgColor = QColor(255, 255, 255)
        self.textAlignment = Qt.AlignLeft | Qt.AlignVCenter # Qt.AlignTop

#################################################################

class UDT_TABLE_CELL():

    def __init__(self, r, c, d, ew = None):

        self.row = r
        self.col = c
        self.data = d  # UDT_TABLE_CELL_DATA()

        self.width = 60
        self.height = 10

        self.editorWidget = ew

#################################################################

class UDT_TABLE_HEADER(list):   # list of ?

    def __init__(self):
        super().__init__()


#################################################################

class UDT_TABLE_RECORD(list):   # list of UDT_TABLE_CELL

    def __init__(self):
        super().__init__()

    def size(self):
        return len(self)

#################################################################

class UDT_TABLE(list):          # list of UDT_TABLE_RECORD


    def __init__(self):
        super().__init__()



#################################################################
# вроде бы, тут необходимо обязательно переопределить четыре метода:
# - data()
# - rowCount()
# - columnCount()
# - headerData()
#################################################################

class UDT_TABLE_MODEL(QAbstractTableModel):


    def __init__(self):

        super().__init__()
        self.header = UDT_TABLE_HEADER()   # list of ... whatever ... I suppose string
        self.body = UDT_TABLE()            # list of UDT_TABLE_RECORD()


    def data(self, index, role):

        cell = self.body[index.row()][index.column()]

        rr = index.row()
        cc = index.column()

        if role == Qt.DisplayRole:

            cell_text = ""

            if cell.data.value is not None:

                if cell.data.type == ENM_TABLE_DATA_TYPE.INT:
                    cell_text = str(cell.data.value)
                if cell.data.type == ENM_TABLE_DATA_TYPE.STRING:
                    cell_text = cell.data.value
                if cell.data.type == ENM_TABLE_DATA_TYPE.DATE:
                    cell_text = cell.data.value.toString("dd.MM.yyyy")
                if cell.data.type == ENM_TABLE_DATA_TYPE.TIME:
                    #if cell.data.value == QTime(0, 0, 0 ,0):
                    #    cell_text = "--"
                    #else:
                    cell_text = cell.data.value.toString("hh:mm:ss")

            else:
                #cell_text = "данные не готовы"
                cell_text = ""

            return cell_text

        if role == Qt.SizeHintRole:

            return QSize(cell.width, cell.height)   # не работает !!!

        if role == Qt.ForegroundRole:

            return cell.data.textColor

        if role == Qt.TextAlignmentRole:

            return int(cell.data.textAlignment)

        return QVariant()


    def rowCount(self, index):
        return len(self.body)

    def columnCount(self, index):
        return len(self.header)

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            #return self.header[section]
            return ""
        if role == Qt.DecorationRole:
            return None
        if role == Qt.SizeHintRole:
            if section == 0:
                return QSize(120, 15) # ??
            if section == 1:
                return QSize(30, 15)
            if section == 2:
                return QSize(200, 15)
            if section == 3:
                return QSize(200, 15)
        if role == Qt.FontRole:
            return QFont("Courier") # ??
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft # ??

        return QVariant()
