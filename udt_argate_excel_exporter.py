########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime


########################################################################################################################

from exporter import EXPORTER

########################################################################################################################
# описание класса:
# - только производит экспорт в MSExcel
# - отдельный поток требуется, потому что это работает медленно
########################################################################################################################

class UDT_ARGATE_EXCEL_EXPORTER(QObject):

    signal_Done = pyqtSignal()

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data
        self.exp = EXPORTER()

        super().__init__()

        self.signal_Done.connect(self.deleteLater)

    ####################################################################################################################

    @pyqtSlot()
    def generateReportType1(self):

        q_res, filepath, filename = self.exp.exportToExcel_ReportType1(self.appData)

        self.appData.window_MainWindow.signal_ExcelFileT1_Done.emit(q_res, filepath, filename)
        self.signal_Done.emit()

    ####################################################################################################################

    @pyqtSlot()
    def generateReportType2(self):

        q_res, filepath, filename = self.exp.exportToExcel_ReportType2(self.appData)

        self.appData.window_MainWindow.signal_ExcelFileT2_Done.emit(q_res, filepath, filename)
        self.signal_Done.emit()

    ####################################################################################################################

