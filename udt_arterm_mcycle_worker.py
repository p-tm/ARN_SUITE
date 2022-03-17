########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtCore import QModelIndex

from PyQt5.QtWidgets import QMessageBox

from copy import copy


########################################################################################################################

from enums import *





########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class UDT_ARTERM_MCYCLE_WORKER(QObject):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.counter = 0

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnMainCycle(self):









        #

        tmp_yellow = False
        tmp_red = False

        for mti in self.appData.CD.MT_INFO:
            mti.update()
            tmp_yellow = tmp_yellow or mti.com_yellow
            tmp_red = tmp_red or mti.com_red

        self.appData.CD.LAMP_WORKSHOP_YELLOW = tmp_yellow
        self.appData.CD.LAMP_WORKSHOP_RED = tmp_red

        #

        self.appData.LAMP_BLINKER.update()

        #
        self.appData.DB_CONN_SUPERVISOR.read_time = self.appData.CD.time

        self.appData.DB_CONN_SUPERVISOR.update()


        #

        self.appData.window_MainWindow.signal_UpdateUI.emit()   #  # UDT_ARTERM_MAIN_WINDOW::msgprc_OnUpdateWindow

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnGetDataForSelectedDayReady(self, success):

        if success:

            self.appData.viewer_DAY = copy(self.appData.buffer_DAY)
            #self.appData.editor_DAY = copy(self.appData.buffer_DAY)
            self.appData.updateDayViewer = True

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnWriteDataForSelectedDayDone(self, success):

        pass

        if success:

            pass


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateVar_AllVars(self):

        self.appData.viewer_DAY = copy(self.appData.editor_DAY)
        self.appData.updateDayViewer = True

        #self.appData.window_MainWindow.signal_UpdateUI.emit()

    ####################################################################################################################

    #@pyqtSlot()
    #def msgprc_OnDbConnOK(self):
    #
    #    self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True
    #
    #####################################################################################################################
    #
    #@pyqtSlot()
    #def msgprc_OnDbConnFail(self):
    #
    #    self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionSuccess(self):

        self.appData.dbConnected = True
        #print("связь с БД установлена")
        self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True
        self.appData.model_DBAccessTrackerBack.append(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - OK")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionFailure(self):

        self.appData.dbConnected = False
        #print("невозможно установить связь с БД")
        self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False
        self.appData.window_MainWindow.signal_ReportOfDBConnectionFailure.emit()
        self.appData.model_DBAccessTrackerBack.append(
            QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "database_connect() - failed")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnInitialDataReadDone(self, success):

        if success:

            #print("start data received " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True

            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() - OK")

            self.appData.window_MainWindow.signal_SingleUpdateArbmonSettings.emit()

        else:
            #print("start data failed " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False

            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_initial_data() - failed")

            self.appData.window_MainWindow.signal_ReportOfInitialDataReadFailure.emit()

        #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnRTDataReadDone(self, success):

        if success:
            #print("RT data received " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() - OK")
        else:
            #print("RT data failed " + QDateTime.currentDateTime().toString("hh:mm:ss.zzz"))
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False
            #self.appData.model_DBAccessTrackerBack.append(
            #    QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "read_realtime_data() - failed")

        #self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

    ####################################################################################################################






