########################################################################################################################
import sys

from PyQt5.QtGui import QColor

########################################################################################################################

from const import GC
from udt_rect_text_field import UDT_RECT_TEXT_FIELD



########################################################################################################################
# описание класса:
#
########################################################################################################################

class UDT_MT_CLASS_DISPLAY():

    class T_ROW(list):

        def __init__(self):
            super().__init__()

    class T_BODY(list):

        def __init__(self):
            super().__init__()

    def __init__(self):

        self.table = self.T_BODY()

        self.x0 = 0.0 ; self.y0 = 0.0 ; self.rw = 0.06 ; self.rh = 0.040

        for i in range(7):

            row = self.T_ROW()

            for j in range(3):

                cell = UDT_RECT_TEXT_FIELD()

                cell.frame.relX0 = self.x0 + j * self.rw
                cell.frame.relY0 = self.y0 + i * self.rh
                cell.frame.relWidth = self.rw
                cell.frame.relHeight = self.rh
                cell.frame.visible = False
                cell.frame.color = QColor("#FFFF00")

                cell.text.color = QColor("#FFFF00")
                if GC.__FOUR_MON__:
                    if i == 0:
                        cell.text.pxSize = 50
                    else:
                        cell.text.pxSize = 40
                elif GC.__FOUR_MON_4K__:
                    if i == 0:
                        cell.text.pxSize = 100
                    else:
                        cell.text.pxSize = 80
                else:
                    cell.text.pxSize = 20

                row.append(cell)

            self.table.append(row)

        fake = 0

    def update(self):

        x0 = self.table[0][0].frame.relX0
        y0 = self.table[0][0].frame.relY0
        rw = self.table[0][0].frame.relWidth
        rh = self.table[0][0].frame.relHeight

        for i in range(7):
            for j in range(3):

                cell = self.table[i][j]

                cell.frame.relX0 = x0 + j * rw
                cell.frame.relY0 = y0 + i * rh
                cell.frame.relWidth = rw
                cell.frame.relHeight = rh

                #cell.update()


    def draw(self, painter, bw = None, bh = None):

        self.update()

        for i in range(7):
            for j in range(3):
                if j == 0:
                    self.table[i][j].draw(painter, bw, bh, hj = 3)
                else:
                    self.table[i][j].draw(painter, bw, bh, hj = 2)







