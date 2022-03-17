########################################################################################################################

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

########################################################################################################################

from const import *

########################################################################################################################

if GC.__FOUR_MON__:

    STYLESHEET_LABEL_TYPE_1 = """
        QLabel {
            color: #FF0000;
            font-size: 60px;
        }
    """

elif GC.__FOUR_MON_4K__:

    STYLESHEET_LABEL_TYPE_1 = """
        QLabel {
            color: #FF0000;
            font-size: 120px;
        }
    """

else:

    STYLESHEET_LABEL_TYPE_1 = """
            QLabel {
                color: #FF0000;
                font-size: 24px;
            }
        """

########################################################################################################################

if GC.__FOUR_MON__:

    STYLESHEET_LABEL_TYPE_2 = """
        QLabel {
            color: #0000FF;
            font-size: 60px;
        }
    """

elif GC.__FOUR_MON_4K__:

    STYLESHEET_LABEL_TYPE_2 = """
        QLabel {
            color: #0000FF;
            font-size: 120px;
        }
    """

else:

    STYLESHEET_LABEL_TYPE_2 = """
            QLabel {
                color: #0000FF;
                font-size: 24px;
            }
        """

########################################################################################################################
#
# это окно без кнопок по идее
# и в настоящее время имеется два типа:
########################################################################################################################

class WINDOW_ARBMON_NONMODAL_MSGBOX(QWidget):

    DB_DATA_FAILURE = 1
    DB_READ_FAILURE = 2

    instance_counter = 0

    ####################################################################################################################

    def __init__(self, type=0, bg_win=None):

        super().__init__()

        WINDOW_ARBMON_NONMODAL_MSGBOX.instance_counter += 1

        self.body_text = "тестовый текст"

        if GC.__FOUR_MON__:
            fixed_width = 1000
            fixed_height = 600
        elif GC.__FOUR_MON_4K__:
            fixed_width = 2000
            fixed_height = 1200
        else:
            fixed_width = 400
            fixed_height = 200

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Msgbox")

        self.setFixedWidth(fixed_width)
        self.setFixedHeight(fixed_height)

        if bg_win is not None:
            self.setGeometry(bg_win.x() + (bg_win.width()-fixed_width)/2, bg_win.y()+(bg_win.height()-fixed_height)/2, fixed_width, fixed_height)

        if type == self.DB_DATA_FAILURE:

            self.createType1()

        if type == self.DB_READ_FAILURE:

            self.createType2()

        self.move(self.x(), self.y() - self.height()/2 +
                  (WINDOW_ARBMON_NONMODAL_MSGBOX.instance_counter - 1) * (self.height() + 10))

    ####################################################################################################################

    def __del__(self):

        WINDOW_ARBMON_NONMODAL_MSGBOX.instance_counter -= 1
        super().__del__()

    ####################################################################################################################

    def createType1(self):

        self.body_text = "Сервер не работает"

        self.setLayout(QVBoxLayout())

        gb = QGroupBox()
        gb.setLayout(QVBoxLayout())
        gb.layout().setAlignment(Qt.AlignCenter)

        gb.layout().addWidget(QLabel(self.body_text))

        self.layout().addWidget(gb)

        #self.move(self.x(),self.y()-self.height()/2 + (WINDOW_ARBMON_NONMODAL_MSGBOX.instance_counter - 1)*self.height()/2 )

        gb.layout().itemAt(0).widget().setStyleSheet(STYLESHEET_LABEL_TYPE_1)

    ####################################################################################################################

    def createType2(self):

        self.body_text = "Нет связи с сервером"

        self.setLayout(QVBoxLayout())

        gb = QGroupBox()
        gb.setLayout(QVBoxLayout())
        gb.layout().setAlignment(Qt.AlignCenter)

        gb.layout().addWidget(QLabel(self.body_text))

        self.layout().addWidget(gb)

        #self.move(self.x(),self.y()+self.height()/2)

        gb.layout().itemAt(0).widget().setStyleSheet(STYLESHEET_LABEL_TYPE_2)

    ####################################################################################################################
