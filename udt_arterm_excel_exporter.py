########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

########################################################################################################################

from exporter import EXPORTER



########################################################################################################################
# описание класса:
# - только производит экспорт в MSExcel
# - отдельный поток требуется, потому что это работает медленно
########################################################################################################################


class UDT_ARTERM_EXCEL_EXPORTER(QObject):

    signal_Done = pyqtSignal()

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data
        self.exp = EXPORTER()

        super().__init__()

        self.signal_Done.connect(self.deleteLater)

    ####################################################################################################################

    @pyqtSlot()
    def generateReport(self):

        q_res, filepath, filename = self.exp.exportToExcel_DetailedRep(self.appData)

        self.appData.window_MainWindow.signal_Excel_TblDetailedRep_Done.emit(q_res, filepath, filename)
        self.signal_Done.emit()

    ####################################################################################################################


