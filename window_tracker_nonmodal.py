########################################################################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QDialog, QFileDialog



########################################################################################################################

from udt_tracker_exporter import UDT_TRACKER_EXPORTER


########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WINDOW_TRACKER_NONMODAL(QWidget):

    ####################################################################################################################

    def __init__(self, app_data, tracker_model, bg_win=None):

        super().__init__()

        self.appData = app_data
        self.model = tracker_model

        # ----------------------------------------------------------------------------------
        initial_width = 450
        initial_height = 600

        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Трекер доступа к БД")

        #self.setFixedWidth(fixed_width)
        #self.setFixedHeight(fixed_height)

        if bg_win is not None:
            self.setGeometry(bg_win.x() + (bg_win.width()-initial_width)/2, bg_win.y()+(bg_win.height()-initial_height)/2, initial_width, initial_height)
        # ----------------------------------------------------------------------------------

        self.listbox_Tracker = QListView()
        #self.listbox_Tracker.setModel(self.appData.model_DBAccessTrackerView)
        self.listbox_Tracker.setModel(self.model)
        self.listbox_Tracker.setAlternatingRowColors(True)

        self.setLayout(QVBoxLayout())

        self.layout().addWidget(self.listbox_Tracker)

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

        btn = QPushButton()
        btn.setText("Закрыть")
        btn.clicked.connect(self.msgprc_OnCloseButtonClicked)
        wdg.layout().addWidget(btn)

        self.layout().addWidget(wdg)

        # ----------------------------------------------------------------------------------

        self.paused = False
        self.button_Resume.setEnabled(False)
        self.button_Export.setEnabled(False)

        # ----------------------------------------------------------------------------------


        self.initUI()

        self.cnt_MissedTrackerRecords = 0



    ####################################################################################################################

    def initUI(self):

        pass

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
    def msgprc_OnPauseButtonClicked(self):

        self.paused = True

        self.button_Pause.setEnabled(False)
        self.button_Resume.setEnabled(True)
        self.button_Export.setEnabled(True)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCloseButtonClicked(self):

        self.close()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnExportButtonClicked(self):

        dialog = QFileDialog()
        #dialog.setAcceptMode(QFileDialog.AcceptSave)

        fname, fmask = dialog.getSaveFileName(parent=self,caption="A",filter="Text file (*.txt)")

        #xxx = dialog.result() # почему то не работает
        #yyy = dialog.acceptMode()

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











