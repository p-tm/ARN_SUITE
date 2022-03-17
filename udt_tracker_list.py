#################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractListModel

from PyQt5.QtGui import QColor

#################################################################
# описание класса:                                              #
#                                                               #
#################################################################

class UDT_TRACKER_LIST(QAbstractListModel):

    def __init__(self, cap=None):

        super().__init__()

        self.theList = list([])
        if cap is not None:
            self.capacity = cap
        else:
            self.capacity = 10000

    def data(self, index, role):

        if role == Qt.DisplayRole:
            text = self.theList[index.row()]
            return text
        if role == Qt.ForegroundRole:
            failed = self.theList[index.row()].find("failed") >= 0
            error = self.theList[index.row()].find("error") >= 0
            ok = self.theList[index.row()].find("OK") >= 0
            good = self.theList[index.row()].find("(+)") >= 0
            bad = self.theList[index.row()].find("(-)") >= 0
            if failed or bad or error:
                return QColor("#B00000")
            elif ok or good:
                return QColor("#008000")
            else:
                return QColor("#000000")

    #def rowsInList(self):
    #    return len(self.theList)

    def rowCount(self, index):
        return len(self.theList)

    def count(self):
        return len(self.theList)

    def append(self, item):

        self.theList.append(item)
        if len(self.theList) > self.capacity:
            self.theList.pop(0)



