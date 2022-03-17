########################################################################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot


from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox

from copy import copy

########################################################################################################################

from udt_user import UDT_USER

########################################################################################################################
# описание класса:
#
########################################################################################################################

class WINDOW_AUTORIZATION_DIALOG(QDialog):

    ####################################################################################################################

    def __init__(self, app_data, bg_win=None):

        super().__init__()

        self.appData = app_data

        fixed_width = 400
        fixed_height = 200

        self.setFixedWidth(fixed_width)
        self.setFixedHeight(fixed_height)

        if bg_win is not None:
            self.setGeometry(bg_win.x() + (bg_win.width()-fixed_width)/2, bg_win.y()+(bg_win.height()-fixed_height)/2, fixed_width, fixed_height)

        self.setLayout(QVBoxLayout())

        groupbox_Data = QGroupBox()
        groupbox_Buttons = QGroupBox()

        self.layout().addWidget(groupbox_Data)
        self.layout().addWidget(groupbox_Buttons)

        self.combobox_User = QComboBox()
        self.edit_Password = QLineEdit()

        self.edit_Password.setEchoMode(QLineEdit.Password)

        # ------------------------------------------------------------

        groupbox_Data.setLayout(QVBoxLayout())

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Пользователь"))
        wdg.layout().addWidget(self.combobox_User)
        wdg.layout().itemAt(0).widget().setFixedWidth(100)
        wdg.layout().itemAt(1).widget().setFixedWidth(200)

        groupbox_Data.layout().addWidget(wdg)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Пароль"))
        wdg.layout().addWidget(self.edit_Password)
        wdg.layout().itemAt(0).widget().setFixedWidth(100)
        wdg.layout().itemAt(1).widget().setFixedWidth(200)

        groupbox_Data.layout().addWidget(wdg)
        groupbox_Data.layout().addStretch(1)





        # ------------------------------------------------------------

        groupbox_Buttons.setLayout(QHBoxLayout())
        groupbox_Buttons.layout().addStretch(1)

        btn = QPushButton()
        btn.setText("OK")
        btn.clicked.connect(self.msgprc_OnOkButtonClick)
        btn.setEnabled(not self.appData.LOGGED_IN)

        groupbox_Buttons.layout().addWidget(btn)

        btn = QPushButton()
        btn.setText("Выход из системы")
        btn.clicked.connect(self.msgprc_OnLogoutButtonClick)
        btn.setEnabled(self.appData.LOGGED_IN)

        groupbox_Buttons.layout().addWidget(btn)

        btn = QPushButton()
        btn.setText("Отмена")
        btn.clicked.connect(self.msgprc_OnCancelButtonClick)

        groupbox_Buttons.layout().addWidget(btn)

        # ------------------------------------------------------------



        # ------------------------------------------------------------

        self.initUI()
        self.initData()

        self.combobox_User.currentIndexChanged.connect(self.msgprc_OnSelectUser)

    ####################################################################################################################

    def initUI(self):

        self.setWindowTitle("Авторизация")
        self.setWindowIcon(self.appData.icon_MainWindowIcon)

    ####################################################################################################################

    def initData(self):

        self.user = copy(self.appData.ACTIVE_USER)

        target_index = 0

        if self.appData.USERS.count() > 0:

            for k, usr in enumerate(self.appData.USERS):
                self.combobox_User.addItem(self.appData.USERS[k].caption, self.appData.USERS[k].id)
                self.combobox_User.setItemData(k, self.appData.USERS[k].id, Qt.UserRole)
                if self.user.id == self.appData.USERS[k].id:
                    target_index = k

            if self.user.id is not None:
                self.combobox_User.setCurrentIndex(target_index)
            else:
                self.combobox_User.setCurrentIndex(0)
                self.user = copy(self.appData.USERS[0])


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnOkButtonClick(self):

        pw = self.edit_Password.text()

        if pw == self.user.password:
            self.appData.ACTIVE_USER = copy(self.user)
            self.appData.LOGGED_IN = True

            msgbox = QMessageBox(parent=self)
            msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
            msgbox.setWindowTitle("Инфо")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(
                "Успешно")
            msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

            self.close()

        else:
            #self.appData.ACTIVE_USER = copy(UDT_USER()) # like "empty" user
            #self.appData.LOGGED_IN = False
            # messagebox

            msgbox = QMessageBox(parent=self)
            msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
            msgbox.setWindowTitle("Ошибка")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(
                "Авторизация невозможна")
            msgbox.setDetailedText("Попробуйте повторить попытку."
                                   "")
            msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
            msgbox.setStandardButtons(QMessageBox.Ok)

            for btn in msgbox.buttons():
                btn_role = msgbox.buttonRole(btn)
                if msgbox.buttonRole(btn) == QMessageBox.ActionRole:
                    btn.click()
                    break

            msgbox.exec_()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnLogoutButtonClick(self):


        self.appData.ACTIVE_USER = copy(UDT_USER())
        self.appData.LOGGED_IN = False

        msgbox = QMessageBox(parent=self)   # is parent is set the dialog is centered to the center of parent
        msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
        msgbox.setWindowTitle("Инфо")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setText(
            "Вы вышли из системы")
        msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()

        self.close()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnCancelButtonClick(self):

        self.close()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnSelectUser(self):

        id = self.combobox_User.itemData(self.combobox_User.currentIndex(), Qt.UserRole)

        target_index = 0

        for k, usr in enumerate(self.appData.USERS):
            if usr.id == id:
                target_index = k
                break

        self.user = copy(self.appData.USERS[target_index])

        dummy = 1

    ####################################################################################################################




