########################################################################################################################
import sys


from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect, QRectF


from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QTextOption
from PyQt5.QtGui import QFont

########################################################################################################################

from const import *

from udt_rect_frame import UDT_RECT_FRAME
from udt_text import UDT_TEXT



########################################################################################################################
# описание класса:
#
########################################################################################################################

class UDT_RECT_TEXT_FIELD():

    ####################################################################################################################

    def __init__(self):

        self.frame = UDT_RECT_FRAME()
        self.text = UDT_TEXT()

        if GC.__FOUR_MON__:
            self.frame.pxThickness = 1
        elif GC.__FOUR_MON_4K__:
            self.frame.pxThickness = 1
        else:
            self.frame.pxThickness = 1

        self.frame.color = QColor("#FFFFFF")
        self.frame.visible = True

        self.text.text = "Text"
        self.text.color = QColor("#FFFFFF")
        if GC.__FOUR_MON__:
            self.text.pxSize = 30
        elif GC.__FOUR_MON_4K__:
            self.text.pxSize = 60
        else:
            self.text.pxSize = 15
        self.text.visible = True
        self.text.bold = False



    ####################################################################################################################

    #def update(self):
    #
    #   self.frame.update()

    ####################################################################################################################

    def toQRect(self):

        self.frame.update()

        r = QRect()

        r.setLeft(self.frame.absX0 - self.frame.absWidth / 2.0 )
        r.setTop(self.frame.absY0 - self.frame.absHeight / 2.0 )
        r.setWidth(self.frame.absWidth)
        r.setHeight(self.frame.absHeight)

        return r

    ####################################################################################################################

    def draw(self, painter, bw = None, bh = None, hj = 2):

        if bw is None and bh is None:
            pass
        else:
            self.frame.baseWidth = bw
            self.frame.baseHeight = bh

        pen = QPen()
        #pen.setColor(self.frameColor)
        #pen.setWidth(self.pxFrameThickness)
        #painter.setPen(pen)

        rect = self.toQRect()

        #if self.frameVisible : painter.drawRect(rect)
        self.frame.draw(painter, self.frame.baseWidth, self.frame.baseHeight)

        to = QTextOption()
        if hj == 1:
            to.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if hj == 2:
            to.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if hj == 3:
            to.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        font = QFont()
        font.setFamily("Calibri")
        font.setPixelSize(self.text.pxSize)
        font.setCapitalization(QFont.MixedCase)
        font.setBold(self.text.bold)

        pen.setColor(self.text.color)
        painter.setPen(pen)

        painter.setFont(font)
        painter.setPen(pen)

        if self.text.visible:
            painter.drawText(QRectF(rect), self.text.text, to)

    ####################################################################################################################
