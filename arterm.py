########################################################################################################################

import sys

from PyQt5.QtWidgets import QApplication

########################################################################################################################

from udt_arterm_app_data import UDT_ARTERM_APP_DATA
from window_arterm_main_window import WINDOW_ARTERM_MAIN_WINDOW



from thread_arterm_dispatcher import THREAD_ARTERM_DISPATCHER
from thread_arterm_db_connect import THREAD_ARTERM_DB_CONNECT
from thread_arterm_mcycle import THREAD_ARTERM_MCYCLE

########################################################################################################################
# описание класса:
# приложение "терминал" - рабочее место пользователя, позволяет "входить" в систему
# - прооизводить настройки
# - текущий мониторинг
########################################################################################################################

# if __name__ == "__main__":

appData = UDT_ARTERM_APP_DATA()

# threads

appData.thread_Dispatcher = THREAD_ARTERM_DISPATCHER()
appData.thread_DBAccess = THREAD_ARTERM_DB_CONNECT()
appData.thread_MCycle = THREAD_ARTERM_MCYCLE()

# main app

appData.application_TheApp = QApplication(sys.argv)
appData.str_AppDir = appData.application_TheApp.applicationDirPath()
appData.str_ResDir = appData.str_AppDir
appData.window_MainWindow = WINDOW_ARTERM_MAIN_WINDOW(appData)


sys.exit(appData.application_TheApp.exec_())

# pyinstaller --onefile --noconsole --distpath ./dist/ARNEG_ESMS/ARTERM --icon=app_icon.ico --version-file=arterm_vinfo.txt arterm.py




