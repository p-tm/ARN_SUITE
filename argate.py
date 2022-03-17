########################################################################################################################

import sys

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication

from udt_argate_app_data import UDT_ARGATE_APP_DATA
from window_argate_main_window import WINDOW_ARGATE_MAIN_WINDOW

from thread_argate_dispatcher import THREAD_ARGATE_DISPATCHER
from thread_check_network import THREAD_CHECK_NETWORK
from thread_field_station_connect import THREAD_FIELD_STATION_CONNECT
from thread_argate_db_connect import THREAD_ARGATE_DB_CONNECT
from thread_argate_mcycle import THREAD_ARGATE_MCYCLE
from thread_argate_excel_exporter import THREAD_ARGATE_EXCEL_EXPORTER
from thread_mail_sender import THREAD_MAIL_SENDER


########################################################################################################################
# описание класса:
# приложение "сервер" - опрашивает field i/o,
# обрабатывает данные,
# пишет данные в БД
########################################################################################################################

# if __name__ == "__main__":

appData = UDT_ARGATE_APP_DATA()


# threads

appData.thread_Dispatcher = THREAD_ARGATE_DISPATCHER()
appData.thread_CheckNetwork = THREAD_CHECK_NETWORK()
appData.thread_FieldAccess = THREAD_FIELD_STATION_CONNECT()
appData.thread_DBAccess = THREAD_ARGATE_DB_CONNECT()
appData.thread_MCycle = THREAD_ARGATE_MCYCLE()
#appData.thread_ExcelExporter = THREAD_ARGATE_EXCEL_EXPORTER()
#appData.thread_MailSender = THREAD_MAIL_SENDER()


# main app

appData.application_TheApp = QApplication(sys.argv)
appData.str_AppDir = appData.application_TheApp.applicationDirPath()
appData.str_ResDir = appData.str_AppDir
appData.window_MainWindow = WINDOW_ARGATE_MAIN_WINDOW(appData)

sys.exit(appData.application_TheApp.exec_())

# for file verson info *.txt file try
# pyi-grab_version cap.exe
# cap.exe - is just an example file to grab info from

# pyinstaller --onefile --distpath ./dist/ARNEG_ESMS/ARGATE --icon=app_icon.ico --version-file=argate_vinfo.txt argate.py
# pyinstaller --onefile --noconsole --distpath ./dist/ARNEG_ESMS/ARGATE --icon=app_icon.ico --version-file=argate_vinfo.txt argate.py

