########################################################################################################################

import sys

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication

########################################################################################################################

from const import *

from udt_arbmon_app_data import UDT_ARBMON_APP_DATA
from window_arbmon_main_window import WINDOW_ARBMON_MAIN_WINDOW

from thread_arbmon_dispatcher import THREAD_ARBMON_DISPATCHER
from thread_arbmon_db_connect import THREAD_ARBMON_DB_CONNECT
from thread_arbmon_mcycle import THREAD_ARBMON_MCYCLE


########################################################################################################################
# описание класса:
########################################################################################################################

appData = UDT_ARBMON_APP_DATA()

# threads

appData.thread_Dispatcher = THREAD_ARBMON_DISPATCHER()
appData.thread_DBAccess = THREAD_ARBMON_DB_CONNECT()
appData.thread_MCycle = THREAD_ARBMON_MCYCLE()

# main app

GC.initialize()

appData.application_TheApp = QApplication(sys.argv)
appData.str_AppDir = appData.application_TheApp.applicationDirPath()
appData.str_ResDir = appData.str_AppDir
appData.window_MainWindow = WINDOW_ARBMON_MAIN_WINDOW(appData)

sys.exit(appData.application_TheApp.exec_())

# pyinstaller --onefile --noconsole --distpath ./dist/ARNEG_ESMS/ARBMON --icon=app_icon.ico --version-file=arbmon_vinfo.txt arbmon.py