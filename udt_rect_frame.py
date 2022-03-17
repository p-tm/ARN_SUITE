########################################################################################################################
import sys

from PyQt5.QtCore import QRect, QRectF

from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QTextOption

########################################################################################################################

from const import *


########################################################################################################################

########################################################################################################################

class UDT_RECT_FRAME():

    ####################################################################################################################

    def __init__(self):

        self.baseWidth = 800;
        self.baseHeight = 600;

        self.relWidth = 0.01
        self.relHeight = 0.01
        self.relX0 = 0.5 - self.relWidth * 0.5
        self.relY0 = 0.5 - self.relHeight * 0.5

        # self.absX0 = self.baseWidth / 2.0 - self.absWidth / 2.0
        # self.absY0 = self.baseHeight / 2.0 - self.absHeight / 2.0
        self.absX0 = self.relX0 * self.baseWidth
        self.absY0 = self.relY0 * self.baseHeight
        self.absWidth = self.relWidth * self.baseWidth
        self.absHeight = self.relHeight * self.baseHeight

        self.maxTextSize = self.absHeight

        self.color = QColor("#FFFFFF")
        if GC.__FOUR_MON__:
            self.pxThickness = 1
        elif GC.__FOUR_MON_4K__:
            self.pxThickness = 1
        else:
            self.pxThickness = 1

        self.visible = True

    ####################################################################################################################

    def update(self):

        self.absX0 = round(self.relX0 * self.baseWidth)
        self.absY0 = round(self.relY0 * self.baseHeight)
        self.absWidth = round(self.relWidth * self.baseWidth)
        self.absHeight = round(self.relHeight * self.baseHeight)

        self.maxTextSize = self.absHeight

    ####################################################################################################################

    def draw(self, painter, bw = None, bh = None):

        if bw is None and bh is None:
            pass
        else:
            self.baseWidth = bw
            self.baseHeight = bh

        pen = QPen()
        pen.setColor(self.color)
        pen.setWidth(self.pxThickness)
        painter.setPen(pen)

        rect = self.toQRect()

        if self.visible : painter.drawRect(rect)

    ####################################################################################################################

    def toQRect(self):

        self.update()

        r = QRect()

        r.setLeft(self.absX0 - self.absWidth / 2.0 )
        r.setTop(self.absY0 - self.absHeight / 2.0 )
        r.setWidth(self.absWidth)
        r.setHeight(self.absHeight)

        return r

    ####################################################################################################################