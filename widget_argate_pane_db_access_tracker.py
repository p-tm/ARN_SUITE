########################################################################################################################
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog

########################################################################################################################

from udt_tracker_exporter import UDT_TRACKER_EXPORTER


########################################################################################################################
# описание класса:
# - это виджет, который кладётся на вкладку ""
#
########################################################################################################################

class WIDGET_ARGATE_PANE_DB_ACCESS_TRACKER(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        #self.layout_CoreLayout = QGridLayout()
        self.setLayout(QVBoxLayout())

        self.listbox_Tracker = QListView()
        self.listbox_Tracker.setModel(self.appData.model_DBAccessTrackerView)
        self.listbox_Tracker.setAlternatingRowColors(True)

        self.layout().addWidget(self.listbox_Tracker)

        #self.layout_CoreLayout.addWidget(self.list_TrackerList, 0, 0, 1, 1)
        #self.layout_CoreLayout.addWidget(self.widget_ButtonPanel, 1, 0, 1, 1)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addStretch(1)

        btn = QPushButton()
        btn.setText("Пауза")
        btn.clicked.connect(self.msgprc_OnPauseButtonClicked)
        wdg.layout().addWidget(btn)

        self.button_Pause = btn

        btn = QPushButton()
        btn.setText("Продолжить")
        btn.clicked.connect(self.msgprc_OnResumeButtonClicked)
        wdg.layout().addWidget(btn)

        self.button_Resume = btn

        btn = QPushButton()
        btn.setText("Экспорт")
        btn.clicked.connect(self.msgprc_OnExportButtonClicked)
        wdg.layout().addWidget(btn)

        self.button_Export = btn

        self.layout().addWidget(wdg)

        # ---------------------------------------------------------

        self.paused = False
        self.button_Resume.setEnabled(False)
        self.button_Export.setEnabled(False)

        #self.cnt_MissedTrackerRecords = 0

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgprc_OnDBConnected(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTrackerBack.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_DBAccessTrackerBack.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnDBConnectionFailed(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTrackerBack.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_DBAccessTrackerBack.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnDBWriteSuccessful(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTrackerBack.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #
    #    if len( self.appData.model_DBAccessTrackerBack.theList ) > 100:
    #        self.appData.model_DBAccessTracker.theList.pop(0)
    #
    #    self.appData.model_DBAccessTrackerBack.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnDBWriteFailed(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTracker.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_DBAccessTracker.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnDBReadSuccessful(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTrackerBack.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_DBAccessTrackerBack.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnDBReadFailed(self, str):
    #
    #    text = str
    #
    #    self.appData.model_DBAccessTrackerBack.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_DBAccessTrackerBack.layoutChanged.emit()
    #    self.listbox_Tracker.scrollToBottom()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnPauseButtonClicked(self):

        self.paused = True

        self.button_Pause.setEnabled(False)
        self.button_Resume.setEnabled(True)
        self.button_Export.setEnabled(True)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnResumeButtonClicked(self):

        self.paused = False

        self.button_Pause.setEnabled(True)
        self.button_Resume.setEnabled(False)
        self.button_Export.setEnabled(False)

        n = self.appData.model_DBAccessTrackerView.capacity

        if self.appData.model_DBAccessTrackerBack.count() > n:
            self.appData.model_DBAccessTrackerView.theList[:] = self.appData.model_DBAccessTrackerBack.theList[-n:]
        else:
            self.appData.model_DBAccessTrackerView.theList[:] = self.appData.model_DBAccessTrackerBack.theList[:]

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnExportButtonClicked(self):

        dialog = QFileDialog()

        fname, fmask = dialog.getSaveFileName(parent=self,caption="Экспорт",filter="Text file (*.txt)")

        if fname != "":

            self.button_Export.setEnabled(False)

            self.thread_Exporter = QThread()
            self.exporter = UDT_TRACKER_EXPORTER(self.appData.model_DBAccessTrackerBack.theList, fname)
            self.exporter.moveToThread(self.thread_Exporter)

            self.thread_Exporter.started.connect(self.exporter.exportToFile)
            self.thread_Exporter.finished.connect(self.thread_Exporter.deleteLater)
            self.exporter.destroyed.connect(self.thread_Exporter.quit)
            self.thread_Exporter.start()

            self.thread_Exporter.finished.connect(lambda: self.button_Export.setEnabled(True))



    ####################################################################################################################


