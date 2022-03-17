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
# -
#
########################################################################################################################

class WIDGET_ARGATE_PANE_APP_TRACKER(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        #self.layout_CoreLayout = QGridLayout()
        self.setLayout(QVBoxLayout())

        self.listbox_Tracker = QListView()
        self.listbox_Tracker.setModel(self.appData.model_AppTrackerView)
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

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnThreadDispatcherStarted(self, str):

        text = str

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnCheckNetworkThreadStarted(self, str):

        text = str

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnFieldAccessThreadStarted(self, str):

        text = str

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnDBAccessThreadStarted(self, str):

        text = str

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    @pyqtSlot(str)
    def msgproc_OnT1ThreadStarted(self, str):

        text = str

        #self.appData.model_AppTracker.theList.append(
        #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        #self.appData.model_AppTracker.layoutChanged.emit()

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text

        self.appData.model_AppTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneAppTracker.paused:
            self.appData.model_AppTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateAppTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateAppTracker

    ####################################################################################################################

    #@pyqtSlot(str)
    #def msgproc_OnExcelExporterThreadStarted(self, str):
    #    text = str
    #
    #    self.appData.model_AppTracker.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_AppTracker.layoutChanged.emit()
    #
    #####################################################################################################################
    #
    #@pyqtSlot(str)
    #def msgproc_OnMailSenderThreadStarted(self, str):
    #    text = str
    #
    #    self.appData.model_AppTracker.theList.append(
    #        QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
    #    self.appData.model_AppTracker.layoutChanged.emit()

    ####################################################################################################################

    @pyqtSlot(str)
    def msgprc_OnDBConnected(self, str):

        text = str

        self.appData.model_AppTracker.theList.append(
            QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + text)
        self.appData.model_AppTracker.layoutChanged.emit()

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

        fname, fmask = dialog.getSaveFileName(parent=self, caption="Экспорт", filter="Text file (*.txt)")

        if fname != "":

            self.button_Export.setEnabled(False)

            self.thread_Exporter = QThread()
            self.exporter = UDT_TRACKER_EXPORTER(self.appData.model_AppTrackerBack.theList, fname)
            self.exporter.moveToThread(self.thread_Exporter)

            self.thread_Exporter.started.connect(self.exporter.exportToFile)
            self.thread_Exporter.finished.connect(self.thread_Exporter.deleteLater)
            self.exporter.destroyed.connect(self.thread_Exporter.quit)
            self.thread_Exporter.start()

            self.thread_Exporter.finished.connect(lambda: self.button_Export.setEnabled(True))

    ####################################################################################################################

