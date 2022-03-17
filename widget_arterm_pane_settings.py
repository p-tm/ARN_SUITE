########################################################################################################################

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton




########################################################################################################################




########################################################################################################################
# описание класса:
#
#
########################################################################################################################

class WIDGET_ARTERM_PANE_SETTINGS(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.initUI()



    ####################################################################################################################

    def initUI(self):

        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel())
        #self.layout().addWidget(QGroupBox())
        self.layout().addStretch(1)

        self.layout().itemAt(0).widget().setText("на данный момент настроек нет...")
        #gb = self.layout().itemAt(0).widget()

        #gb.setTitle("Сохранение отчётов")
        #gb.setLayout(QVBoxLayout())
        #gb.layout().addWidget(QCheckBox())
        #gb.layout().addWidget(QLabel())
        #gb.layout().addWidget(QWidget())
        #gb.layout().addStretch(1)




        # Groupbox "Сохранение отчётов"

        #self.checkbox_KeepOnServer = gb.layout().itemAt(0).widget()
        #self.label_FilePathEdit = gb.layout().itemAt(1).widget()
        #
        #wdg = gb.layout().itemAt(2).widget()
        #wdg.setLayout(QHBoxLayout())
        #wdg.layout().addWidget(QLineEdit())
        #wdg.layout().addWidget(QPushButton())
        #
        #self.lineedit_FilePath = wdg.layout().itemAt(0).widget()
        #self.button_FilePathDialog = wdg.layout().itemAt(1).widget()
        #
        #
        #self.checkbox_KeepOnServer.setText("Сохранять копии отчётов на сервере")
        #self.label_FilePathEdit.setText("Папка для хранения копий отчётов")
        #self.button_FilePathDialog.setText("...")
        #
        #self.button_FilePathDialog.setFixedWidth(30)
        #
        ## initialization
        #
        #self.checkbox_KeepOnServer.setChecked(self.appData.settings.keepCopyOfReportFileOnServer)



    ####################################################################################################################
