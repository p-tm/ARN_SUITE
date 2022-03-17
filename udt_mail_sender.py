########################################################################################################################

import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime

from PyQt5.QtWidgets import QMessageBox

import smtplib
import ssl
import email
import imaplib
import time

# pip install PySocks
import socks

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


########################################################################################################################



########################################################################################################################
# описание класса:
# - только производит коннект с почтовым сервером
# - и отправку почты
# - отдельный поток требуется, потому что это работает медленно
########################################################################################################################

class UDT_MAIL_SENDER(QObject):

    signal_Done = pyqtSignal() # вспомогат сигнал для нормального завершения потока
    signal_EmailSent = pyqtSignal(bool)

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data

        super().__init__()

        self.signal_Done.connect(self.deleteLater)

    ####################################################################################################################

    def TRACK(self, track_msg):

        self.appData.model_RepGenTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
            self.appData.model_RepGenTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()

    ####################################################################################################################

    @pyqtSlot(str,str)
    def msgprc_OnSendEmail(self, filepath, filename):


        port = 465
        #port = 25
        #port = 587

        # sender_account = "arn_sender@mail.ru"
        # sender_account_password = "test_email"
        # smtp_server = "smtp.mail.ru"

        # sender_account = "arn.sender@gmail.com"
        # sender_account_password = "test_email"
        # smtp_server = "smtp.gmail.com"

        sender_account = "monitoring.machine@arneg.ru"
        #sender_account1 = "monitoring.machine"
        sender_account_password = "Dsy!p29@"
        #smtp_server = "relay.arneg.org"
        smtp_server = "smtps.arneg.org"

        ra = self.appData.settings.destEmail
        ra1 = ra.split(",")
        receiver_account = list([])

        for addr in ra1:
            addr1 = addr.strip()
            receiver_account.append(addr1)


        #receiver_account = self.appData.settings.destEmail

        #message = """\
        #Subject: test email
        #
        #test email from ARNEG without attachments"""

        message = MIMEMultipart()
        message["From"] = sender_account
        message["To"] = ra # receiver_account
        message["Subject"] = "система мониторинга " + filename

        #message_body = "test message with attachment"
        message_body = "Система мониторинга за состоянием оборудования - отчёт\n\n" +\
            "(это письмо сгенерировано автоматически, не отвечайте на него)"

        full_file_name = filepath + "/" + filename

        message.attach(MIMEText(message_body, "plain"))

        attachment = open(full_file_name, "rb")
        part = MIMEBase("application", "octet_stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",f"attachment; filename={filename}",)

        message.attach(part)
        text = message.as_string()

        attachment.close()


        #context = ssl.create_default_context()
        #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        #socks.setdefaultproxy(socks.HTTP, '172.31.254.220', 8080)
        #socks.setdefaultproxy(socks.HTTP, '89.109.254.122', 8080)
        #socks.setdefaultproxy(socks.SOCKS5, '172.31.254.220', 8080)
        #socks.wrapmodule(smtplib)

        server = None

        try:
            #server = smtplib.SMTP(host=smtp_server, port=port)
            server = smtplib.SMTP_SSL(host=smtp_server, port=port)
            #server.set_debuglevel(True)
            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "подключение к smtp серверу OK"
            self.TRACK(track_msg)
        except Exception as e:
            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
            self.TRACK(track_msg)
        else:
            try:
                server.ehlo()
                track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "handshaking OK"
                self.TRACK(track_msg)
            except Exception as e:
                track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
                self.TRACK(track_msg)
            else:
                try:
                    pass
                    #server.starttls()
                    #track_msg = QDateTime.currentDateTime().toString(
                    #    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "TLS-шифрование включено " + " (+)"
                    #self.TRACK(track_msg)
                except Exception as e:
                    track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
                    self.TRACK(track_msg)
                else:
                    try:
                        pass
                        #server.ehlo()
                        #track_msg = QDateTime.currentDateTime().toString(
                        #    "dd.MM.yyyy hh:mm:ss.zzz") + " - " + "повторный handshaking OK"
                        #self.TRACK(track_msg)
                    except Exception as e:
                        track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
                        self.TRACK(track_msg)
                    else:
                        try:
                            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "попытка войти в аккаунт"
                            self.TRACK(track_msg)
                            server.login(sender_account, sender_account_password)
                            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "вход в аккаунт OK"
                            self.TRACK(track_msg)
                        except smtplib.SMTPAuthenticationError as e:
                            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "The server didn’t accept the username/password combination" + " (-)"
                            self.TRACK(track_msg)
                            #if server is not None:
                            #    server.quit()
                             #   server = None
                        except Exception as e:
                            track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
                            self.TRACK(track_msg)
                            #if server is not None:
                            #    server.quit()
                            #    server = None
                        else:


                            try:

                                server.sendmail(sender_account, receiver_account, text)

                                print("-- письмо отправлено --")
                                track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - email отправлен (+)"
                                self.TRACK(track_msg)

                            #except smtplib.SMTPAuthenticationError as e:

                            #    print("-- проблема при авторизации --")
                            #    print(e)

                            #    track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"


                            except Exception as e:
                                #print("-- проблема 1 ")
                                #print("-- проблема: " + e)

                                track_msg = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + str(e) + " (-)"
                                self.TRACK(track_msg)




                            #except smtplib.SMTPRecipientsRefused as e:
                            #    dummy = 0
                            #except smtplib.SMTPHeloError as e:
                            #    dummy = 0
                            #except smtplib.SMTPSenderRefused as e:
                            #    dummy = 0
                            #except smtplib.SMTPDataError as e:
                            #    dummy = 0
                            #except smtplib.SMTPNotSupportedError as e:
                            #    dummy = 0
                            finally:
                                if server is not None:
                                    server.quit()

        #if self.appData.settings.keepCopyOfReportFileOnServer == 0:
        #    os.remove(full_file_name)

        #if self.appData.eod_GEN_REP_SEQ_STATE == 0:         # not end-of-day
        #    if self.appData.eos_GEN_REP_SEQ_STATE == 3:     #
        #        self.appData.eos_GEN_REP_SEQ_STATE == 0     # end of REPORT_T2
        #elif self.appData.eod_GEN_REP_SEQ_STATE == 1:       # is end-of-day and waits for end of REPORT_T2
        #    if self.appData.eos_GEN_REP_SEQ_STATE == 3:     #
        #        self.appData.eos_GEN_REP_SEQ_STATE == 0     # end of REPORT_T2
        #        self.appData.worker_MCycle.signal_DBRead_TblReportT1.emit(1)    # start REPORT_T1 @ end-of-day
        #        self.appData.eod_GEN_REP_SEQ_STATE == 2     # WAIT until REPORT_T1 is generated and sent
        #elif  self.appData.eod_GEN_REP_SEQ_STATE == 3:
        #    self.appData.eod_GEN_REP_SEQ_STATE = 0          # end of REPORT_T1 @ end-of-day



        #self.appData.model_RepGenTrackerBack.append(track_msg)
        #if not self.appData.widget_TabPaneReportsGenerationTracker.paused:
        #    self.appData.model_RepGenTrackerView.append(track_msg)
        #self.appData.window_MainWindow.signal_UpdateReportsGenerationTracker.emit()


        #imap = imaplib.IMAP4_SSL("imap.arneg.org", 993)
        #imap.login(sender_account, sender_account_password)
        #imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), text.encode('utf8'))
        #imap.logout()


        q_res = True

        self.signal_EmailSent.emit(q_res)
        self.signal_Done.emit()






