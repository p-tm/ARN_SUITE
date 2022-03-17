from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor

########################################################################################################################

from enums import *

########################################################################################################################

class UDT_LAMP(QWidget):

    ####################################################################################################################

    def __init__(self, sh = ENM_LAMP_SHAPE.ROUND, cl = ENM_LAMP_COLOR.GREY, pl = 0):

        super().__init__()

        self.shape = sh
        self.color = cl
        self.pulsing = pl

        self.blinker = 0
        self.on = False

        self.width_ = 10
        self.height_ = 10




    ####################################################################################################################

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)

        cur_w = self.width()
        cur_h = self.height()

        #rect = QRect(0,0,10,10)
        rect = QRect(0, 0, self.width_, self.height_)

        #pen = QPen()
        #brush = QBrush()
        pen = painter.pen()
        brush = painter.brush()

        grey_color = QColor("#808080")
        green_color = QColor("#00FF00")
        yellow_color = QColor("#FFFF00")
        red_color = QColor("#FF0000")
        black_color = QColor("#000000")

        if self.color == ENM_LAMP_COLOR.GREY:

            pen.setColor(grey_color)
            brush.setColor(grey_color)

        elif self.color == ENM_LAMP_COLOR.GREEN:

            if not self.on:
                pen.setColor(grey_color)
                brush.setColor(grey_color)
            else:
                if self.pulsing:
                    if self.blinker:
                        pen.setColor(green_color)
                        brush.setColor(green_color)
                    else:
                        pen.setColor(grey_color)
                        brush.setColor(grey_color)
                else:
                    pen.setColor(green_color)
                    brush.setColor(green_color)

        elif self.color == ENM_LAMP_COLOR.YELLOW:

            if not self.on:
                pen.setColor(grey_color)
                brush.setColor(grey_color)
            else:
                if self.pulsing:
                    if self.blinker:
                        pen.setColor(yellow_color)
                        brush.setColor(yellow_color)
                    else:
                        pen.setColor(grey_color)
                        brush.setColor(grey_color)
                else:
                    pen.setColor(yellow_color)
                    brush.setColor(yellow_color)

        elif self.color == ENM_LAMP_COLOR.RED:

            if not self.on:
                pen.setColor(grey_color)
                brush.setColor(grey_color)
            else:
                if self.pulsing:
                    if self.blinker:
                        pen.setColor(red_color)
                        brush.setColor(red_color)
                    else:
                        pen.setColor(grey_color)
                        brush.setColor(grey_color)
                else:
                    pen.setColor(red_color)
                    brush.setColor(red_color)

        pen.setWidth(1)
        painter.setPen(pen)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)



        #brush.setColor(QColor("#404040"))



        if self.shape == ENM_LAMP_SHAPE.ROUND:
            painter.drawEllipse(rect)
        elif self.shape == ENM_LAMP_SHAPE.SQUARED:
            #painter.fillRect(rect, brush)
            painter.drawRect(rect)

        painter.end()

    ####################################################################################################################

    def sizeHint(self):

        return QSize(self.width_+2,self.height_+2)

    ####################################################################################################################

    def minimumSizeHint(self):

        return QSize(0,0)

    ####################################################################################################################
