########################################################################################################################

import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QDateTime

########################################################################################################################

from udt_argate_excel_exporter import UDT_ARGATE_EXCEL_EXPORTER
from udt_mail_sender import UDT_MAIL_SENDER

########################################################################################################################

class UDT_REPORT_GENERATION_SUPERVISOR(QObject):

    REPORT_TYPE_T1  = 1
    REPORT_TYPE_T2  = 2

    ####################################################################################################################

    def __init__(self, app_data, rt):

        super().__init__()

        self.appData = app_data
        self.rtype = rt
        self.sendEmail = False
        self.saveCopy = False
        self.filePath = ""
        self.fileName = ""

        self.busy = False
        self.state = 0      # 0 = not busy
                            # 1 = prepare
                            # 2 = query to DB is active
                            # 3 = prepare
                            # 4 = export to Excel is active
                            # 5 = prepare
                            # 6 = sending email is active
                            # 7 = email is sent

    ####################################################################################################################
    def startGeneration(self):

        #print("start generation - 1")
        self.busy = True
        self.state = 1

        self.readTableFromDB()
        #print("start generation - 2")
    ####################################################################################################################
    def readTableFromDB(self):

        #print("read table from db - 1")

        self.state = 2

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1:
            self.appData.window_MainWindow.signal_DBRead_TblReportT1.emit()
        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T2:
            self.appData.window_MainWindow.signal_DBRead_TblReportT2.emit()

        #print("read table from db - 2")

    ####################################################################################################################
    def startExportToExcel(self):

        #print("start export to excel - 1")

        self.state = 4

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1:

            self.thread_Exporter_t1 = QThread()
            self.exporter_t1 = UDT_ARGATE_EXCEL_EXPORTER(self.appData)
            self.exporter_t1.moveToThread(self.thread_Exporter_t1)

            self.thread_Exporter_t1.started.connect(self.exporter_t1.generateReportType1)
            self.thread_Exporter_t1.finished.connect(self.thread_Exporter_t1.deleteLater)
            self.exporter_t1.destroyed.connect(self.thread_Exporter_t1.quit)
            self.thread_Exporter_t1.start()

            #self.thread_Exporter_t1.finished.connect() что то ещё типа разблокировать кнопку

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T2:

            self.thread_Exporter_t2 = QThread()
            self.exporter_t2 = UDT_ARGATE_EXCEL_EXPORTER(self.appData)
            self.exporter_t2.moveToThread(self.thread_Exporter_t2)

            self.thread_Exporter_t2.started.connect(self.exporter_t2.generateReportType2)
            self.thread_Exporter_t2.finished.connect(self.thread_Exporter_t2.deleteLater)
            self.exporter_t2.destroyed.connect(self.thread_Exporter_t2.quit)
            self.thread_Exporter_t2.start()

            #self.thread_Exporter_t2.finished.connect() что то ещё типа разблокировать кнопку


    ####################################################################################################################
    def startSendEmail(self):

        state = 6

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1:

            #self.appData.window_MainWindow.signal_T1_SendEmail.emit(self.filePath, self.fileName)

            self.thread_MailSender_t1 = QThread()
            self.sender_t1 = UDT_MAIL_SENDER(self.appData)
            self.sender_t1.moveToThread(self.thread_MailSender_t1)

            self.appData.window_MainWindow.signal_T1_SendEmail.connect(self.sender_t1.msgprc_OnSendEmail)
            self.sender_t1.signal_EmailSent.connect(self.msgprc_OnEmailSentT1)

            self.thread_MailSender_t1.started.connect(lambda: self.appData.window_MainWindow.signal_T1_SendEmail.emit(self.filePath,self.fileName))
            self.thread_MailSender_t1.finished.connect(self.thread_MailSender_t1.deleteLater)
            self.sender_t1.destroyed.connect(self.thread_MailSender_t1.quit)
            self.thread_MailSender_t1.start()

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T2:


            self.thread_MailSender_t2 = QThread()
            self.sender_t2 = UDT_MAIL_SENDER(self.appData)
            self.sender_t2.moveToThread(self.thread_MailSender_t2)

            self.appData.window_MainWindow.signal_T2_SendEmail.connect(self.sender_t2.msgprc_OnSendEmail)
            self.sender_t2.signal_EmailSent.connect(self.msgprc_OnEmailSentT2)

            self.thread_MailSender_t2.started.connect(lambda: self.appData.window_MainWindow.signal_T2_SendEmail.emit(self.filePath,self.fileName))
            self.thread_MailSender_t2.finished.connect(self.thread_MailSender_t2.deleteLater)
            self.sender_t2.destroyed.connect(self.thread_MailSender_t2.quit)
            self.thread_MailSender_t2.start()


    ####################################################################################################################
    def finishGeneration(self):

        self.busy = False
        self.state = 0

        self.sendEmail = self.saveCopy = False

        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1:
            self.appData.window_MainWindow.signal_ReportT1Finished.emit()
        if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T2:
            self.appData.window_MainWindow.signal_ReportT2Finished.emit()

    ####################################################################################################################
    @pyqtSlot(bool,bool)
    def msgprc_OnStartGeneration(self, send_email, save_copy):

        self.sendEmail = send_email
        self.saveCopy = save_copy

        #if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T1:
        #    self.appData.widget_TabPaneTests.button_ART1_Generate.setEnabled(False)
        #    self.appData.widget_TabPaneTests.button_ART1_GenerateAndSend.setEnabled(False)
        #if self.rtype == UDT_REPORT_GENERATION_SUPERVISOR.REPORT_TYPE_T12:
        #    self.appData.widget_TabPaneTests.button_ART2_Generate.setEnabled(False)
        #    self.appData.widget_TabPaneTests.button_ART2_GenerateAndSend.setEnabled(False)

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - запрос отчёта тип #" + str(self.rtype)

        self.appData.model_RepGenTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
            self.appData.model_RepGenTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker

        self.startGeneration()

    ####################################################################################################################
    @pyqtSlot(bool)
    def msgprc_OnTableReceived(self, success):

        self.state = 3

        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - отчёт тип #" + str(self.rtype) +\
            " - таблица считана"

        self.appData.model_RepGenTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
            self.appData.model_RepGenTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker

        self.startExportToExcel()

    ####################################################################################################################
    @pyqtSlot(bool,str,str)
    def msgprc_OnExcelFileReady(self, success, fp, fn):

        self.state = 5


        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - отчёт тип #" + str(self.rtype) +\
            " - файл Excel сгенерирован"

        self.appData.model_RepGenTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
            self.appData.model_RepGenTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker

        self.filePath = fp
        self.fileName = fn

        if self.sendEmail:
            self.startSendEmail()
        else:                           # keep file in this case
            self.finishGeneration()

    ####################################################################################################################
    @pyqtSlot(bool)
    def msgprc_OnEmailSentT1(self, success):

        self.state = 7

        #track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - отчёт тип #" + str(self.rtype) +\
        #    " - email отправлен"
        #
        #self.appData.model_RepGenTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        #    self.appData.model_RepGenTrackerView.append(track_msg)
        #self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker

        full_file_name = self.filePath + "/" + self.fileName

        if not self.saveCopy:
            os.remove(full_file_name)

        self.finishGeneration()

    ####################################################################################################################
    @pyqtSlot(bool)
    def msgprc_OnEmailSentT2(self, success):

        self.state = 7

        #track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - отчёт тип #" + str(self.rtype) +\
        #    " - email отправлен"
        #
        #self.appData.model_RepGenTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        #    self.appData.model_RepGenTrackerView.append(track_msg)
        #self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateReportsGenerationTracker

        full_file_name = self.filePath + "/" + self.fileName

        if not self.saveCopy:
            os.remove(full_file_name)

        self.finishGeneration()

    ####################################################################################################################




