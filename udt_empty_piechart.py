from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor, QTextOption
from PyQt5.QtGui import QFont

########################################################################################################################

from const import *

########################################################################################################################

class UDT_EMPTY_PIECHART(QWidget):

    ####################################################################################################################

    def __init__(self):

        super().__init__()

        self.width_ = 400
        self.height_ = 400

        self.rel_diameter = 0.60

        self.edge_color = QColor("#FFFFFF")
        self.fill_color = QColor("#008000")
        self.caption_color = QColor("#FFFF00")

        self.caption = "простоев\nнет"
        self.showCaption  = True

    ####################################################################################################################

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)

        cur_w = self.width()
        cur_h = self.height()

        diameter = cur_w * self.rel_diameter

        rect = QRect(cur_w/2 - diameter/2, cur_h/2 - diameter/2, diameter, diameter)
        #rect = QRect(100,100, self.width_, self.height_)

        pen = painter.pen()
        brush = painter.brush()


        pen.setColor(self.edge_color)
        brush.setColor(self.fill_color)


        pen.setWidth(1)
        painter.setPen(pen)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        painter.drawEllipse(rect)

        to = QTextOption()
        to.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        font = painter.font()
        font.setFamily("Calibri")
        if GC.__FOUR_MON__:
            font.setPixelSize(70)
        elif GC.__FOUR_MON_4K__:
            font.setPixelSize(140)
        else:
            font.setPixelSize(24)
        #font.setCapitalization(QFont.AllUppercase)
        #font.setBold(1)


        pen.setColor(self.caption_color)
        painter.setPen(pen)

        painter.setFont(font)
        painter.drawText(QRectF(rect), self.caption, to)

        painter.end()

    ####################################################################################################################

    def sizeHint(self):

        return QSize(self.width_+2,self.height_+2)

    ####################################################################################################################

    def minimumSizeHint(self):

        return QSize(10,10)

    ####################################################################################################################

