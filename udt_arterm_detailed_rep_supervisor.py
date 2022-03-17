########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QDateTime

########################################################################################################################

from udt_arterm_excel_exporter import UDT_ARTERM_EXCEL_EXPORTER


########################################################################################################################

class UDT_ARTERM_DETAILED_REP_SUPERVISOR(QObject):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.filePath = ""
        self.fileName = ""

        self.busy = False
        self.state = 0      # 0 = not busy (idle)
                            # 1 = prepare
                            # 2 = query to DB is active
                            # 3 = prepare
                            # 4 = export to Excel is active

    ####################################################################################################################

    def startGeneration(self):

        self.busy = True
        self.state = 1

        self.readTableFromDB()

    ####################################################################################################################

    def readTableFromDB(self):

        self.state = 2

        self.appData.window_MainWindow.signal_DBRead_TblDetailedRep.emit()  # -> worker_DBAccess.msgprc_OnReadTableDetailedReport()

    ####################################################################################################################

    def startExportToExcel(self):

        self.state = 4

        self.thread_DetailedRepExporter = QThread()
        self.exporter_DetailedRep = UDT_ARTERM_EXCEL_EXPORTER(self.appData)
        self.exporter_DetailedRep.moveToThread(self.thread_DetailedRepExporter)

        self.thread_DetailedRepExporter.started.connect(self.exporter_DetailedRep.generateReport)
        self.thread_DetailedRepExporter.finished.connect(self.thread_DetailedRepExporter.deleteLater)
        self.exporter_DetailedRep.destroyed.connect(self.thread_DetailedRepExporter.quit)
        self.thread_DetailedRepExporter.start()

    ####################################################################################################################

    def finishGeneration(self):

        self.busy = False
        self.state = 0

        self.appData.window_MainWindow.signal_ReportFinished.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnStartGeneration(self):

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - запрос отчёта"

        # тут просто по аналогии будет два трекера, хотя кнопка "Пауза" тут отсутствует (нет функции паузы)

        self.appData.model_DetailedRepTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        if not False:
            self.appData.model_DetailedRepTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker


        track_msg = "(+) процесс формирования отчёта может быть очень длительным, пожалуйста, подождите..."

        # тут просто по аналогии будет два трекера, хотя кнопка "Пауза" тут отсутствует (нет функции паузы)

        self.appData.model_DetailedRepTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        if not False:
            self.appData.model_DetailedRepTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker


        self.startGeneration()

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnTableReceived(self, success):

        self.state = 3

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - отчёт" +\
            " - таблица считана"

        self.appData.model_DetailedRepTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        if not False:
            self.appData.model_DetailedRepTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker !!!

        self.startExportToExcel()

    ####################################################################################################################

    @pyqtSlot(bool,str,str)
    def msgprc_OnExcelFileReady(self, success, fp, fn):

        self.state = 5

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") +\
            " - файл Excel сгенерирован"

        self.appData.model_DetailedRepTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        if not False:
            self.appData.model_DetailedRepTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker !!!

        self.filePath = fp
        self.fileName = fn

        self.finishGeneration()


    ####################################################################################################################



