########################################################################################################################
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect, QRectF


from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QTextOption
from PyQt5.QtGui import QFont




########################################################################################################################

from const import *

from udt_rect_frame import UDT_RECT_FRAME


########################################################################################################################
# описание класса:
#
########################################################################################################################

class UDT_MACHINE_TOOL_FOOTPRINT():

    def __init__(self):

        self.rectFrame = UDT_RECT_FRAME()

        if GC.__FOUR_MON__:
            self.frameColor = QColor("#0060D0")
        elif GC.__FOUR_MON_4K__:
            self.frameColor = QColor("#00E0E0")
        else:
            self.frameColor = QColor("#0060D0")
        #self.fillColor = QColor("#A0A000")
        self.centralText = "Text"
        self.blinker = False
        self.view = 0   # offline

    def update(self):

        self.rectFrame.update()

    def toQRect(self):

        self.rectFrame.update()

        r = QRect()

        r.setLeft(self.rectFrame.absX0 - self.rectFrame.absWidth/2.0)
        r.setTop(self.rectFrame.absY0 - self.rectFrame.absHeight/2.0)
        r.setWidth(self.rectFrame.absWidth)
        r.setHeight(self.rectFrame.absHeight)

        return r

    def draw(self, painter, bw = None, bh = None):

        if bw is None and bh is None:
            pass
        else:
            self.rectFrame.baseWidth = bw
            self.rectFrame.baseHeight = bh

        pen = QPen()
        pen.setColor(self.frameColor)
        if GC.__FOUR_MON__:
            pen.setWidth(2)
        elif GC.__FOUR_MON_4K__:
            pen.setWidth(3)
        else:
            pen.setWidth(1)
        painter.setPen(pen)

        rect = self.toQRect()
        #painter.drawRect(rect)

        brush = QBrush()

        if self.view == 0: # offline
            brush.setColor(QColor("#404040"))
            brush.setStyle(Qt.SolidPattern)
            painter.fillRect(rect, brush)
        if self.view == 1: # normal
            pass
        if self.view == 2: # yellow
            if self.blinker:
                brush.setColor(QColor("#FFFF00"))
            else:
                #brush.setColor(QColor("#404040"))
                brush.setColor(QColor("#000000"))
            brush.setStyle(Qt.SolidPattern)
            painter.fillRect(rect, brush)
        if self.view == 3: # red
            if self.blinker:
                brush.setColor(QColor("#FF0000"))
            else:
                #brush.setColor(QColor("#404040"))
                brush.setColor(QColor("#000000"))
            brush.setStyle(Qt.SolidPattern)
            painter.fillRect(rect, brush)

        painter.drawRect(rect)

        to = QTextOption()
        to.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        font = QFont()
        font.setFamily("Calibri")
        if GC.__FOUR_MON__:
            font.setPixelSize(64)
        elif GC.__FOUR_MON_4K__:
            font.setPixelSize(128)
        else:
            font.setPixelSize(32)
        font.setCapitalization(QFont.AllUppercase)
        font.setBold(1)

        if self.view == 0:
            pen.setColor(QColor("#202020"))
        if self.view == 1 or self.view == 3:
            pen.setColor(QColor("#FFFF00"))
        if self.view == 2:
            if self.blinker:
                pen.setColor(QColor("#000000"))
            else:
                pen.setColor(QColor("#FFFF00"))

        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(QRectF(rect), self.centralText, to)






