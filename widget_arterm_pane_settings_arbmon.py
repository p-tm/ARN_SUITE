########################################################################################################################

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime, QDate, QTime


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QIcon


########################################################################################################################


########################################################################################################################
# описание класса:
#
#
########################################################################################################################

class WIDGET_ARTERM_PANE_SETTINGS_ARBMON(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QVBoxLayout()
        self.setLayout(self.layout_CoreLayout)

        self.groupbox_ArbmonSettings = QGroupBox()
        self.groupbox_ArbmonSettings.setLayout(QVBoxLayout())

        self.layout_CoreLayout.addWidget(self.groupbox_ArbmonSettings)


        self.edit_MS_CHANGE_ALARM_WIDGET = QLineEdit()
        self.edit_MS_RUNNING_CAPTION_TICK = QLineEdit()
        self.edit_MS_SHOW_WORKSHOP = QLineEdit()
        self.edit_MS_SHOW_DIAGRAMS = QLineEdit()

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Период смены аварийного сообщения"))
        wdg.layout().addWidget(self.edit_MS_CHANGE_ALARM_WIDGET)
        wdg.layout().addWidget(QLabel("мс"))
        wdg.layout().addStretch(1)
        wdg.layout().itemAt(0).widget().setFixedWidth(250)
        wdg.layout().itemAt(1).widget().setFixedWidth(100)
        wdg.layout().itemAt(2).widget().setFixedWidth(40)
        self.groupbox_ArbmonSettings.layout().addWidget(wdg)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Период прокрутки бегущей строки"))
        wdg.layout().addWidget(self.edit_MS_RUNNING_CAPTION_TICK)
        wdg.layout().addWidget(QLabel("мс"))
        wdg.layout().addStretch(1)
        wdg.layout().itemAt(0).widget().setFixedWidth(250)
        wdg.layout().itemAt(1).widget().setFixedWidth(100)
        wdg.layout().itemAt(2).widget().setFixedWidth(40)
        self.groupbox_ArbmonSettings.layout().addWidget(wdg)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Период демонстрации \"плана цеха\""))
        wdg.layout().addWidget(self.edit_MS_SHOW_WORKSHOP)
        wdg.layout().addWidget(QLabel("мс"))
        wdg.layout().addStretch(1)
        wdg.layout().itemAt(0).widget().setFixedWidth(250)
        wdg.layout().itemAt(1).widget().setFixedWidth(100)
        wdg.layout().itemAt(2).widget().setFixedWidth(40)
        self.groupbox_ArbmonSettings.layout().addWidget(wdg)

        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addWidget(QLabel("Период демонстрации диаграмм"))
        wdg.layout().addWidget(self.edit_MS_SHOW_DIAGRAMS)
        wdg.layout().addWidget(QLabel("мс"))
        wdg.layout().addStretch(1)
        wdg.layout().itemAt(0).widget().setFixedWidth(250)
        wdg.layout().itemAt(1).widget().setFixedWidth(100)
        wdg.layout().itemAt(2).widget().setFixedWidth(40)
        self.groupbox_ArbmonSettings.layout().addWidget(wdg)

        self.groupbox_ArbmonSettings.layout().addStretch(1)

        self.button_SaveToDB = QPushButton()
        self.button_SaveToDB.setText("Сохранить")


        wdg = QWidget()
        wdg.setLayout(QHBoxLayout())
        wdg.layout().addStretch(1)
        wdg.layout().addWidget(self.button_SaveToDB)

        self.layout_CoreLayout.addWidget(wdg)
        self.layout_CoreLayout.addStretch(1)


        self.button_SaveToDB.clicked.connect(self.msgprc_OnSaveToDBClick)


        self.initUI()
        self.initData()

    ####################################################################################################################

    def initUI(self):

        pass

    ####################################################################################################################

    def initData(self):

        self.edit_MS_CHANGE_ALARM_WIDGET.setText(str(self.appData.settings.ms_CHANGE_ALARM_WIDGET))
        self.edit_MS_RUNNING_CAPTION_TICK.setText(str(self.appData.settings.ms_RUNNING_CAPTION_TICK))
        self.edit_MS_SHOW_WORKSHOP.setText(str(self.appData.settings.ms_SHOW_WORKSHOP))
        self.edit_MS_SHOW_DIAGRAMS.setText(str(self.appData.settings.ms_SHOW_DIAGRAMS))

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnSaveToDBClick(self):

        self.appData.settings.ms_CHANGE_ALARM_WIDGET = int(self.edit_MS_CHANGE_ALARM_WIDGET.text())
        self.appData.settings.ms_RUNNING_CAPTION_TICK = int(self.edit_MS_RUNNING_CAPTION_TICK.text())
        self.appData.settings.ms_SHOW_WORKSHOP = int(self.edit_MS_SHOW_WORKSHOP.text())
        self.appData.settings.ms_SHOW_DIAGRAMS = int(self.edit_MS_SHOW_DIAGRAMS.text())

        self.appData.window_MainWindow.signal_WriteArbmonSettings.emit()

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnWriteArbmonSettingsDone(self, success):

        if success:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_arbmon_settings() - OK")
        else:
            self.appData.model_DBAccessTrackerBack.append(
                QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - " + "write_arbmon_settings() - OK")

        self.appData.window_MainWindow.signal_UpdateDBAccessTracker.emit()

        if success:

            msgbox = QMessageBox()
            msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
            msgbox.setWindowTitle("Инфо")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setText(
                "Запись настроек для утилиты центрального монитора\n"
                "произведена успешно")
            msgbox.setStyleSheet("QLabel{qproperty-alignment:AlignCenter;}")
            msgbox.setDetailedText(""
                                   "Для активации введённых настроек необходимо перезапустить"
                                   "утилиту центрального монитора")
            msgbox.setStandardButtons(QMessageBox.Ok)

            for btn in msgbox.buttons():
                btn_role = msgbox.buttonRole(btn)
                if msgbox.buttonRole(btn) == QMessageBox.ActionRole:
                    btn.click()
                    break
                    #btn.setDisabled(True)
                    #btn.setText("-")
                #if msgbox.buttonRole(btn) == QMessageBox.RejectRole:
                #    btn.setText("Закрыть")

            msgbox.exec_()

        else:

            msgbox = QMessageBox()
            msgbox.setWindowIcon(self.appData.icon_MainWindowIcon)
            msgbox.setWindowTitle("Ошибка")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(
                "Запись настроек для утилиты центрального монитора\n"
                "прошла неудачно")
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
    def msgprc_OnUpdateWindow(self):

        if self.appData.ACTIVE_USER.permission_edit:
            self.button_SaveToDB.setEnabled(True)
        else:
            self.button_SaveToDB.setEnabled(False)


        #self.edit_MS_CHANGE_ALARM_WIDGET.setText(str(self.appData.settings.ms_CHANGE_ALARM_WIDGET))
        #self.edit_MS_RUNNING_CAPTION_TICK.setText(str(self.appData.settings.ms_RUNNING_CAPTION_TICK))
        #self.edit_MS_SHOW_WORKSHOP.setText(str(self.appData.settings.ms_SHOW_WORKSHOP))
        #self.edit_MS_SHOW_DIAGRAM.setText(str(self.appData.settings.ms_SHOW_WORKSHOP))
        # надо только один раз обновить хоть это и неправильно

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnSingleUpdateWindow(self):

        self.initData()

    ####################################################################################################################



