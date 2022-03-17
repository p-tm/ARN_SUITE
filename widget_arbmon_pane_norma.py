########################################################################################################################
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRect, QRectF

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel


from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtGui import QPixmap

########################################################################################################################

from const import *
from enums import *
from udt_rect_text_field import UDT_RECT_TEXT_FIELD

########################################################################################################################
# описание класса:
# - на этом виджете придётся рисовать вручную )))
#
########################################################################################################################

class WIDGET_ARBMON_PANE_NORMA(QWidget):

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.tabCaption = "норм"

        self.main_string = UDT_RECT_TEXT_FIELD()
        self.clock_string = UDT_RECT_TEXT_FIELD()
        self.logo_label = QPixmap(self.appData.str_ResDir + "/logo_arneg_russia.png")

        self.content = "СИСТЕМА МОНИТОРИНГА ЗА СОСТОЯНИЕМ ОБОРУДОВАНИЯ \"АРНЕГ\""
        self.initialString = self.content + "                                                              "
        self.actualString = self.initialString

        self.initUI()

    ####################################################################################################################

    def initUI(self):

        self.main_string.frame.relX0 = 0.5
        self.main_string.frame.relY0 = 0.505
        if GC.__FOUR_MON__:
            self.main_string.frame.relWidth = 2.1
        elif GC.__FOUR_MON_4K__:
            self.main_string.frame.relWidth = 4.2
        else:
            self.main_string.frame.relWidth = 1.05
        self.main_string.frame.relHeight = 1.0
        if GC.__FOUR_MON__:
            self.main_string.frame.pxThickness = 2
        elif GC.__FOUR_MON_4K__:
            self.main_string.frame.pxThickness = 4
        else:
            self.main_string.frame.pxThickness = 2
        self.main_string.frame.color = QColor("#00FF00")
        self.main_string.frame.visible = True
        self.main_string.text.text = "СИСТЕМА МОНИТОРИНГА ЗА СОСТОЯНИЕМ ОБОРУДОВАНИЯ \"АРНЕГ\""
        self.main_string.text.color = QColor("#00FF00")
        if GC.__FOUR_MON__:
            self.main_string.text.pxSize = 72
        elif GC.__FOUR_MON_4K__:
            self.main_string.text.pxSize = 154
        else:
            self.main_string.text.pxSize = 36
        self.main_string.text.bold = True

        self.clock_string.frame.relX0 = 1.0 - 0.08/2.0
        self.clock_string.frame.relY0 = 0.88
        self.clock_string.frame.relWidth = 0.08
        self.clock_string.frame.relHeight = 0.2
        self.clock_string.frame.visible = False
        self.clock_string.text.text = "00:00:00"
        self.clock_string.text.color = QColor("#00FF00")
        if GC.__FOUR_MON__:
            self.clock_string.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.clock_string.text.pxSize = 120
        else:
            self.clock_string.text.pxSize = 18
        self.clock_string.text.bold = False

    ####################################################################################################################

    def paintEvent(self, event):


        cur_w = self.width()
        cur_h = self.height()

        painter = QPainter(self)

        self.main_string.draw(painter, bw=cur_w, bh=cur_h)

        self.clock_string.draw(painter, bw=cur_w, bh=cur_h)

        source = QRectF(0, 0, 1000, 1000)
        if GC.__FOUR_MON__:
            target = QRectF(2, cur_h - 50, 1000, 1000)
        elif GC.__FOUR_MON_4K__:
            target = QRectF(2, cur_h - 125, 2000, 2000)
        else:
            target = QRectF(2, cur_h - 40, 600, 600)
        painter.drawPixmap(target, self.logo_label, source)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):


        self.main_string.text.text = self.actualString

        txt = self.appData.CD.time.toString("hh:mm:ss")

        self.clock_string.text.text = txt

        self.update()

    ####################################################################################################################
