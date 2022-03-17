########################################################################################################################

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap


########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class WINDOW_ARTERM_ABOUT_DIALOG(QDialog):

    ####################################################################################################################

    def __init__(self,app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.widget_InfoPanel = QWidget()
        self.widget_ButtonPanel = QWidget()

        self.layout_InfoPanelLayout = QHBoxLayout()
        self.widget_InfoPanel.setLayout(self.layout_InfoPanelLayout)

        self.layout_ButtonPanelLayout = QHBoxLayout()
        self.widget_ButtonPanel.setLayout(self.layout_ButtonPanelLayout)

        self.label_Info = QLabel()
        self.picture_Logo = QLabel()

        self.button_Close = QPushButton()


        self.initUI()
        self.connectSignals()

    ####################################################################################################################

    def initUI(self):

        self.setWindowTitle("О программе...")
        #str = self.appData.application_TheApp.applicationDirPath()
        self.setWindowIcon(self.appData.icon_MainWindowIcon)

        pic = QPixmap(self.appData.str_ResDir + "/window_icon.png")
        self.picture_Logo.setPixmap(pic.scaled(80, 80))

        w_flags = self.windowFlags()
        w_flags = w_flags & ~Qt.WindowContextHelpButtonHint

        self.setWindowFlags(w_flags)

        self.setFixedSize(200, 200)

        self.layout_InfoPanelLayout.addWidget(self.picture_Logo)
        self.layout_InfoPanelLayout.addWidget(self.label_Info)

        self.layout_ButtonPanelLayout.addStretch(1)
        self.layout_ButtonPanelLayout.addWidget(self.button_Close)
        self.layout_ButtonPanelLayout.addStretch(1)

        self.layout_CoreLayout.addWidget(self.widget_InfoPanel)
        self.layout_CoreLayout.addStretch(1)
        self.layout_CoreLayout.addWidget(self.widget_ButtonPanel)

        info_txt = "ООО \"АРНЕГ\"\n\n" +\
              "Система мониторинга за состоянием оборудования\n\n" +\
              "(c) 2021 г."

        self.label_Info.setText(info_txt)
        self.label_Info.setAlignment(Qt.AlignCenter)

        self.button_Close.setText("Закрыть")

        self.button_Close.setMinimumWidth(60)
        self.button_Close.setMinimumHeight(30)

        self.setMinimumWidth(400)
        self.setMinimumHeight(200)

        #self.picture_Logo.scaledToWidth(50)
        #self.picture_Logo.scaledToHeight(50)
        self.picture_Logo.setGeometry(20,20,20,20)



    ####################################################################################################################

    def connectSignals(self):

        self.button_Close.pressed.connect(self.msgprc_OnClose)

    ####################################################################################################################

    def msgprc_OnClose(self):

        self.close()

    ####################################################################################################################