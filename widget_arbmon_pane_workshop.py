########################################################################################################################

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtCore import pyqtSlot


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStyle, QStyleOption


from PyQt5.QtGui import QColor, QPainter, QBrush


########################################################################################################################

from enums import *
from const import *


from udt_machine_tool_footprint import UDT_MACHINE_TOOL_FOOTPRINT
from udt_rect_text_field import UDT_RECT_TEXT_FIELD
from udt_mt_class_display import UDT_MT_CLASS_DISPLAY




########################################################################################################################
# описание класса:
# - на этом виджете придётся рисовать вручную )))
#
########################################################################################################################


class WIDGET_ARBMON_PANE_WORKSHOP(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        # UI

        self.setStyleSheet("background-color: green")

        # machine tool footprints

        self.fp_MT01 = UDT_MACHINE_TOOL_FOOTPRINT()  # footprint for MachineTool #1
        self.fp_MT02 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT03 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT04 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT05 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT06 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT07 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT08 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT09 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT10 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT11 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT12 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT13 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT14 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT15 = UDT_MACHINE_TOOL_FOOTPRINT()
        self.fp_MT16 = UDT_MACHINE_TOOL_FOOTPRINT()


        # captions

        self.header_r1 = UDT_RECT_TEXT_FIELD()
        self.header_r2 = UDT_RECT_TEXT_FIELD()
        self.header_r3 = UDT_RECT_TEXT_FIELD()
        self.tblhdr_PowderCoating = UDT_RECT_TEXT_FIELD()
        self.tblhdr_MetallWork = UDT_RECT_TEXT_FIELD()
        self.tblhdr_Punching = UDT_RECT_TEXT_FIELD()
        self.tblhdr_Bending = UDT_RECT_TEXT_FIELD()

        #

        k_CLASS_TABLE_BODY_ROW_HEIGHT_REL = 0.025

        self.tbldisp_PowderCoating = UDT_MT_CLASS_DISPLAY()
        self.tbldisp_Punching = UDT_MT_CLASS_DISPLAY()
        self.tbldisp_Bending = UDT_MT_CLASS_DISPLAY()


        self.initUI()

    ####################################################################################################################

    def initUI(self):

        k_UPPER_HEADER_ROW_HEIGHT_REL = 0.045
        k_CLASS_TABLE_HEADER_ROW_HEIGHT_REL = 0.025


        if GC.__FOUR_MON__:
            px_CLASS_TABLE_HEADER_TEXT_SIZE = 50
        elif GC.__FOUR_MON_4K__:
            px_CLASS_TABLE_HEADER_TEXT_SIZE = 100
        else:
            px_CLASS_TABLE_HEADER_TEXT_SIZE = 25



        # machine tool footprints

        self.fp_MT01.rectFrame.relX0 = 0.65
        self.fp_MT01.rectFrame.relY0 = 0.8
        #self.fp_MT01.rectFrame.relX0 = 0
        #self.fp_MT01.rectFrame.relY0 = 0
        self.fp_MT01.rectFrame.relWidth = 0.12
        self.fp_MT01.rectFrame.relHeight = 0.2
        self.fp_MT01.centralText = "n/d" #"M1"

        self.fp_MT02.rectFrame.relX0 = 0.48
        self.fp_MT02.rectFrame.relY0 = 0.45
        self.fp_MT02.rectFrame.relWidth = 0.06
        self.fp_MT02.rectFrame.relHeight = 0.25
        self.fp_MT02.centralText = "n/d" #"M2"

        self.fp_MT03.rectFrame.relX0 = 0.35
        self.fp_MT03.rectFrame.relY0 = 0.45
        self.fp_MT03.rectFrame.relWidth = 0.15
        self.fp_MT03.rectFrame.relHeight = 0.25
        self.fp_MT03.centralText = "n/d" #"M3"

        self.fp_MT04.rectFrame.relX0 = 0.7
        self.fp_MT04.rectFrame.relY0 = 0.45
        self.fp_MT04.rectFrame.relWidth = 0.06
        self.fp_MT04.rectFrame.relHeight = 0.25
        self.fp_MT04.centralText = "n/d" #"M3"

        self.fp_MT05.rectFrame.relX0 = 0.60
        self.fp_MT05.rectFrame.relY0 = 0.15
        self.fp_MT05.rectFrame.relWidth = 0.1
        self.fp_MT05.rectFrame.relHeight = 0.2
        self.fp_MT05.centralText = "n/d" #"M4"

        self.fp_MT06.rectFrame.relX0 = 0.52
        self.fp_MT06.rectFrame.relY0 = 0.8
        self.fp_MT06.rectFrame.relWidth = 0.12
        self.fp_MT06.rectFrame.relHeight = 0.2
        self.fp_MT06.centralText = "n/d" #"P1"

        self.fp_MT07.rectFrame.relX0 = 0.24
        self.fp_MT07.rectFrame.relY0 = 0.85
        self.fp_MT07.rectFrame.relWidth = 0.055
        self.fp_MT07.rectFrame.relHeight = 0.055
        self.fp_MT07.centralText = "n/d" #"P2"

        self.fp_MT08.rectFrame.relX0 = 0.4
        self.fp_MT08.rectFrame.relY0 = 0.85
        self.fp_MT08.rectFrame.relWidth = 0.055
        self.fp_MT08.rectFrame.relHeight = 0.055
        self.fp_MT08.centralText = "n/d" #"P2"

        self.fp_MT09.rectFrame.relX0 = 0.32
        self.fp_MT09.rectFrame.relY0 = 0.85
        self.fp_MT09.rectFrame.relWidth = 0.055
        self.fp_MT09.rectFrame.relHeight = 0.055
        self.fp_MT09.centralText = "n/d" #"P3"

        self.fp_MT10.rectFrame.relX0 = 0.32
        self.fp_MT10.rectFrame.relY0 = 0.75
        self.fp_MT10.rectFrame.relWidth = 0.055
        self.fp_MT10.rectFrame.relHeight = 0.055
        self.fp_MT10.centralText = "n/d" #"P4"

        self.fp_MT11.rectFrame.relX0 = 0.24
        self.fp_MT11.rectFrame.relY0 = 0.75
        self.fp_MT11.rectFrame.relWidth = 0.055
        self.fp_MT11.rectFrame.relHeight = 0.055
        self.fp_MT11.centralText = "n/d" #"P5"

        self.fp_MT12.rectFrame.relX0 = 0.4
        self.fp_MT12.rectFrame.relY0 = 0.75
        self.fp_MT12.rectFrame.relWidth = 0.055
        self.fp_MT12.rectFrame.relHeight = 0.055
        self.fp_MT12.centralText = "n/d" #"P6"

        self.fp_MT13.rectFrame.relX0 = 0.54
        self.fp_MT13.rectFrame.relY0 = 0.45
        self.fp_MT13.rectFrame.relWidth = 0.06
        self.fp_MT13.rectFrame.relHeight = 0.25
        self.fp_MT13.centralText = "n/d" #"P7"

        self.fp_MT14.rectFrame.relX0 = 0.62
        self.fp_MT14.rectFrame.relY0 = 0.45
        self.fp_MT14.rectFrame.relWidth = 0.06
        self.fp_MT14.rectFrame.relHeight = 0.25
        self.fp_MT14.centralText = "n/d" #"P8"

        self.fp_MT15.rectFrame.relX0 = 0.72
        self.fp_MT15.rectFrame.relY0 = 0.15
        self.fp_MT15.rectFrame.relWidth = 0.1
        self.fp_MT15.rectFrame.relHeight = 0.2
        self.fp_MT15.centralText = "n/d" #"SV2"

        self.fp_MT16.rectFrame.relX0 = 0.105
        self.fp_MT16.rectFrame.relY0 = 0.2
        self.fp_MT16.rectFrame.relWidth = 0.2
        self.fp_MT16.rectFrame.relHeight = 0.3
        self.fp_MT16.centralText = "n/d" #"П"

        # captions

        self.header_r1.frame.relX0 = 0.4
        self.header_r1.frame.relY0 = k_UPPER_HEADER_ROW_HEIGHT_REL/2.0
        self.header_r1.frame.relWidth = 0.3
        self.header_r1.frame.relHeight = k_UPPER_HEADER_ROW_HEIGHT_REL
        self.header_r1.frame.visible = False
        self.header_r1.text.text = "ПРОСТОИ ЗА СМЕНУ"
        self.header_r1.text.color = QColor("#FFFF00")
        if GC.__FOUR_MON__:
            self.header_r1.text.pxSize = 100
        elif GC.__FOUR_MON_4K__:
            self.header_r1.text.pxSize = 200
        else:
            self.header_r1.text.pxSize = 28

        self.header_r2.frame.relX0 = 0.4
        self.header_r2.frame.relY0 = k_UPPER_HEADER_ROW_HEIGHT_REL/2.0 + k_UPPER_HEADER_ROW_HEIGHT_REL + 0.02
        self.header_r2.frame.relWidth = 0.3
        self.header_r2.frame.relHeight = k_UPPER_HEADER_ROW_HEIGHT_REL
        self.header_r2.frame.visible = False
        self.header_r2.text.text = "Смена 1: 06:00 - 14:30"
        self.header_r2.text.color = QColor("#FFFF00")
        if GC.__FOUR_MON__:
            self.header_r2.text.pxSize = 56
        elif GC.__FOUR_MON_4K__:
            self.header_r2.text.pxSize = 112
        else:
            self.header_r2.text.pxSize = 28

        self.header_r3.frame.relX0 = 0.4
        self.header_r3.frame.relY0 = k_UPPER_HEADER_ROW_HEIGHT_REL/2.0 + k_UPPER_HEADER_ROW_HEIGHT_REL * 2.0 + 0.02
        self.header_r3.frame.relWidth = 0.3
        self.header_r3.frame.relHeight = k_UPPER_HEADER_ROW_HEIGHT_REL
        self.header_r3.frame.visible = False
        self.header_r3.text.text = "Дата:"
        self.header_r3.text.color = QColor("#FFFF00")
        if GC.__FOUR_MON__:
            self.header_r3.text.pxSize = 56
        elif GC.__FOUR_MON_4K__:
            self.header_r3.text.pxSize = 112
        else:
            self.header_r3.text.pxSize = 28

        #

        self.tblhdr_PowderCoating.frame.relX0 = 0.08
        self.tblhdr_PowderCoating.frame.relY0 = 0.6
        self.tblhdr_PowderCoating.frame.relWidth = 0.2
        self.tblhdr_PowderCoating.frame.relHeight = k_CLASS_TABLE_HEADER_ROW_HEIGHT_REL
        self.tblhdr_PowderCoating.frame.visible = False
        self.tblhdr_PowderCoating.text.text = "ПОРОШКОВАЯ ПОКРАСКА"
        self.tblhdr_PowderCoating.text.color = QColor("#FFFF00")
        self.tblhdr_PowderCoating.text.pxSize = px_CLASS_TABLE_HEADER_TEXT_SIZE



        self.tbldisp_PowderCoating.table[0][0].frame.relX0 = 0.08 - 1.0 * self.tbldisp_PowderCoating.rw
        self.tbldisp_PowderCoating.table[0][0].frame.relY0 = 0.66

        self.tbldisp_PowderCoating.table[0][0].text.text = ""
        self.tbldisp_PowderCoating.table[0][1].text.text = "О"
        self.tbldisp_PowderCoating.table[0][2].text.text = "Т"

        self.tbldisp_PowderCoating.table[1][0].text.text = "Отключен"
        self.tbldisp_PowderCoating.table[1][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[1][2].text.visible = False
        self.tbldisp_PowderCoating.table[2][0].text.text = "Поломка"
        self.tbldisp_PowderCoating.table[2][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[2][2].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[3][0].text.text = "Материал"
        self.tbldisp_PowderCoating.table[3][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[3][2].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[4][0].text.text = "Процесс"
        self.tbldisp_PowderCoating.table[4][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[4][2].text.visible = False
        self.tbldisp_PowderCoating.table[5][0].text.text = "Качество"
        self.tbldisp_PowderCoating.table[5][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[5][2].text.visible = False
        self.tbldisp_PowderCoating.table[6][0].text.text = "Итог"
        self.tbldisp_PowderCoating.table[6][1].text.text = "00:00:00"
        self.tbldisp_PowderCoating.table[6][2].text.text = "00:00:00"

        #

        self.tblhdr_MetallWork.frame.relX0 = 0.9
        self.tblhdr_MetallWork.frame.relY0 = 0.1
        self.tblhdr_MetallWork.frame.relWidth = 0.2
        self.tblhdr_MetallWork.frame.relHeight = k_CLASS_TABLE_HEADER_ROW_HEIGHT_REL
        self.tblhdr_MetallWork.frame.visible = False
        self.tblhdr_MetallWork.text.text = "МЕТАЛЛООБРАБОТКА"
        self.tblhdr_MetallWork.text.color = QColor("#FFFF00")
        self.tblhdr_MetallWork.text.pxSize = px_CLASS_TABLE_HEADER_TEXT_SIZE

        #

        self.tblhdr_Punching.frame.relX0 = 0.9
        self.tblhdr_Punching.frame.relY0 = 0.15
        self.tblhdr_Punching.frame.relWidth = 0.2
        self.tblhdr_Punching.frame.relHeight = k_CLASS_TABLE_HEADER_ROW_HEIGHT_REL
        self.tblhdr_Punching.frame.visible = False
        self.tblhdr_Punching.text.text = "ШТАМПОВКА"
        self.tblhdr_Punching.text.color = QColor("#FFFF00")
        self.tblhdr_Punching.text.pxSize = px_CLASS_TABLE_HEADER_TEXT_SIZE

        self.tbldisp_Punching.table[0][0].frame.relX0 = 0.9 - 1.0 * self.tbldisp_Punching.rw
        self.tbldisp_Punching.table[0][0].frame.relY0 = 0.21

        self.tbldisp_Punching.table[0][0].text.text = ""
        self.tbldisp_Punching.table[0][1].text.text = "О"
        self.tbldisp_Punching.table[0][2].text.text = "Т"

        self.tbldisp_Punching.table[1][0].text.text = "Отключен"
        self.tbldisp_Punching.table[1][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[1][2].text.visible = False
        self.tbldisp_Punching.table[2][0].text.text = "Поломка"
        self.tbldisp_Punching.table[2][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[2][2].text.text = "00:00:00"
        self.tbldisp_Punching.table[3][0].text.text = "Материал"
        self.tbldisp_Punching.table[3][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[3][2].text.text = "00:00:00"
        self.tbldisp_Punching.table[4][0].text.text = "Процесс"
        self.tbldisp_Punching.table[4][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[4][2].text.visible = False
        self.tbldisp_Punching.table[5][0].text.text = "Качество"
        self.tbldisp_Punching.table[5][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[5][2].text.visible = False
        self.tbldisp_Punching.table[6][0].text.text = "Итог"
        self.tbldisp_Punching.table[6][1].text.text = "00:00:00"
        self.tbldisp_Punching.table[6][2].text.text = "00:00:00"

        #

        self.tblhdr_Bending.frame.relX0 = 0.9
        self.tblhdr_Bending.frame.relY0 = 0.6
        self.tblhdr_Bending.frame.relWidth = 0.2
        self.tblhdr_Bending.frame.relHeight = k_CLASS_TABLE_HEADER_ROW_HEIGHT_REL
        self.tblhdr_Bending.frame.visible = False
        self.tblhdr_Bending.text.text = "Г И Б К А"
        self.tblhdr_Bending.text.color = QColor("#FFFF00")
        self.tblhdr_Bending.text.pxSize = px_CLASS_TABLE_HEADER_TEXT_SIZE

        self.tbldisp_Bending.table[0][0].frame.relX0 = 0.9 - 1.0 * self.tbldisp_Bending.rw
        self.tbldisp_Bending.table[0][0].frame.relY0 = 0.66

        self.tbldisp_Bending.table[0][0].text.text = ""
        self.tbldisp_Bending.table[0][1].text.text = "О"
        self.tbldisp_Bending.table[0][2].text.text = "Т"

        self.tbldisp_Bending.table[1][0].text.text = "Отключен"
        self.tbldisp_Bending.table[1][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[1][2].text.visible = False
        self.tbldisp_Bending.table[2][0].text.text = "Поломка"
        self.tbldisp_Bending.table[2][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[2][2].text.text = "00:00:00"
        self.tbldisp_Bending.table[3][0].text.text = "Материал"
        self.tbldisp_Bending.table[3][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[3][2].text.text = "00:00:00"
        self.tbldisp_Bending.table[4][0].text.text = "Процесс"
        self.tbldisp_Bending.table[4][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[4][2].text.visible = False
        self.tbldisp_Bending.table[5][0].text.text = "Качество"
        self.tbldisp_Bending.table[5][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[5][2].text.visible = False
        self.tbldisp_Bending.table[6][0].text.text = "Итог"
        self.tbldisp_Bending.table[6][1].text.text = "00:00:00"
        self.tbldisp_Bending.table[6][2].text.text = "00:00:00"


    ####################################################################################################################

    def paintEvent(self, event):

        # (!!!) почему то painter должен быть разрушен ври выходе из этой функции,
        # т.е. нельзя self.painter, только локальный painter

        cur_w = self.width()
        cur_h = self.height()



        painter = QPainter(self)

        opt = QStyleOption()
        stl = self.style()

        #stl.drawPrimitive(QStyle.PE_Widget, opt, self.painter, self)

        #brush = painter.brush()
        #brush.setColor(QColor("#FF0000"))
        #brush.setStyle(Qt.SolidPattern)
        #rect = QRect(0,0,painter.device().width(),painter.device().height())    # device() возвращает размер прямоугольника
                                                                                # заданного в __init__
                                                                                # в данном случае - это размер self



        self.fp_MT01.draw(painter, bw = cur_w, bh = cur_h)
        self.fp_MT02.draw(painter, bw = cur_w, bh = cur_h)
        self.fp_MT03.draw(painter, bw = cur_w, bh = cur_h)
        self.fp_MT04.draw(painter, bw = cur_w, bh = cur_h)
        self.fp_MT05.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT06.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT07.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT08.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT09.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT10.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT11.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT12.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT13.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT14.draw(painter, bw=cur_w, bh=cur_h)
        self.fp_MT15.draw(painter, bw = cur_w, bh = cur_h)
        self.fp_MT16.draw(painter, bw = cur_w, bh = cur_h)



        self.header_r1.draw(painter, bw = cur_w, bh = cur_h)
        self.header_r2.draw(painter, bw = cur_w, bh = cur_h)
        self.header_r3.draw(painter, bw = cur_w, bh = cur_h)
        self.tblhdr_PowderCoating.draw(painter, bw = cur_w, bh = cur_h)
        self.tblhdr_MetallWork.draw(painter, bw = cur_w, bh = cur_h)
        self.tblhdr_Punching.draw(painter, bw = cur_w, bh = cur_h)
        self.tblhdr_Bending.draw(painter, bw = cur_w, bh = cur_h)

        self.tbldisp_PowderCoating.draw(painter, bw = cur_w, bh = cur_h)
        self.tbldisp_Punching.draw(painter, bw = cur_w, bh = cur_h)
        self.tbldisp_Bending.draw(painter, bw = cur_w, bh = cur_h)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        #
        # txt = "Смена " + str( self.appData.CD.shift_number )+ ": " + str( self.appData.CD.shiftCaption )
        txt = "Смена " + str(self.appData.CD.shift_number) + ": " + str( self.appData.CD.curShiftBTime.toString("hh:mm")) + " - " + str( self.appData.CD.curShiftETime.toString("hh:mm"))
        if self.appData.CD.isNight:
            txt = txt + " (ночь)"   # -- не работает!

        self.header_r2.text.text = txt
        self.header_r3.text.text = "Дата: " + self.appData.CD.date.toString("dd.MM.yyyy")

        # mt fooprints

        if self.appData.MACHINE_TOOLS.count() > 0:
            self.fp_MT01.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY - 1].tag
            self.fp_MT02.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN - 1].tag
            self.fp_MT03.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600 - 1].tag
            self.fp_MT04.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000 - 1].tag
            self.fp_MT05.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000 - 1].tag
            self.fp_MT06.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT - 1].tag
            self.fp_MT07.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1 - 1].tag
            self.fp_MT08.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2 - 1].tag
            self.fp_MT09.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM - 1].tag
            self.fp_MT10.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL - 1].tag
            self.fp_MT11.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3 - 1].tag
            self.fp_MT12.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P6_TRUBEND - 1].tag
            self.fp_MT13.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN - 1].tag
            self.fp_MT14.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW - 1].tag
            self.fp_MT15.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT - 1].tag
            self.fp_MT16.centralText = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT - 1].tag

        if self.appData.CD.MT_INFO.count() > 0:
            self.fp_MT01.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY - 1].view
            self.fp_MT02.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN - 1].view
            self.fp_MT03.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600 - 1].view
            self.fp_MT04.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000 - 1].view
            self.fp_MT05.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000 - 1].view
            self.fp_MT06.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P1_STARMATIC_ROBOT - 1].view
            self.fp_MT07.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_1 - 1].view
            self.fp_MT08.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P2_COLGAR_BIG_2 - 1].view
            self.fp_MT09.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P3_COLGAR_MEDIUM - 1].view
            self.fp_MT10.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P4_COLGAR_SMALL - 1].view
            self.fp_MT11.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P5_COLGAR_BIG_3 - 1].view
            self.fp_MT12.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P6_TRUBEND - 1].view
            self.fp_MT13.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P7_SALVAGNINI_GREEN - 1].view
            self.fp_MT14.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.BEND_P8_SALVAGNINI_YELLOW - 1].view
            self.fp_MT15.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.WELD_SV2_ABB_ROBOT - 1].view
            self.fp_MT16.view = self.appData.CD.MT_INFO[ENM_MACHINE_TOOLS.COAT_N_POWDER_COAT - 1].view


        # update table <Металлообработка:Штамповка>

        if self.appData.CD.MT_STAT.count() > 0:

            self.tbldisp_PowderCoating.table[1][1].text.text = self.appData.CD.MT_STAT[1][26].offline.strHMS()
            #self.tbldisp_PowderCoating.table[2][2].text.text = self.appData.CD.MT_STAT[1][26].alr_failure.strHMS()
            self.tbldisp_PowderCoating.table[2][2].text.text = "---"
            #self.tbldisp_PowderCoating.table[3][2].text.text = self.appData.CD.MT_STAT[1][26].alr_material.strHMS()
            self.tbldisp_PowderCoating.table[3][2].text.text = "---"
            #self.tbldisp_PowderCoating.table[2][1].text.text = self.appData.CD.MT_STAT[1][26].stp_failure.strHMS()
            self.tbldisp_PowderCoating.table[2][1].text.text = "---"
            #self.tbldisp_PowderCoating.table[3][1].text.text = self.appData.CD.MT_STAT[1][26].stp_material.strHMS()
            self.tbldisp_PowderCoating.table[3][1].text.text = "---"
            self.tbldisp_PowderCoating.table[4][1].text.text = self.appData.CD.MT_STAT[1][26].stp_process.strHMS()
            #self.tbldisp_PowderCoating.table[5][1].text.text = self.appData.CD.MT_STAT[1][26].stp_quality.strHMS()
            self.tbldisp_PowderCoating.table[5][1].text.text = "---"

            self.tbldisp_PowderCoating.table[6][1].text.text = self.appData.CD.MT_STAT[1][26].stp_sum.strHMS()
            #self.tbldisp_PowderCoating.table[6][2].text.text = self.appData.CD.MT_STAT[1][26].alr_sum.strHMS()
            self.tbldisp_PowderCoating.table[6][2].text.text = "---"

            self.tbldisp_Bending.table[1][1].text.text = self.appData.CD.MT_STAT[1][24].offline.strHMS()
            self.tbldisp_Bending.table[2][2].text.text = self.appData.CD.MT_STAT[1][24].alr_failure.strHMS()
            self.tbldisp_Bending.table[3][2].text.text = self.appData.CD.MT_STAT[1][24].alr_material.strHMS()
            self.tbldisp_Bending.table[2][1].text.text = self.appData.CD.MT_STAT[1][24].stp_failure.strHMS()
            self.tbldisp_Bending.table[3][1].text.text = self.appData.CD.MT_STAT[1][24].stp_material.strHMS()
            self.tbldisp_Bending.table[4][1].text.text = self.appData.CD.MT_STAT[1][24].stp_process.strHMS()
            self.tbldisp_Bending.table[5][1].text.text = self.appData.CD.MT_STAT[1][24].stp_quality.strHMS()

            self.tbldisp_Bending.table[6][1].text.text = self.appData.CD.MT_STAT[1][24].stp_sum.strHMS()
            self.tbldisp_Bending.table[6][2].text.text = self.appData.CD.MT_STAT[1][24].alr_sum.strHMS()

            self.tbldisp_Punching.table[1][1].text.text = self.appData.CD.MT_STAT[1][23].offline.strHMS()
            self.tbldisp_Punching.table[2][2].text.text = self.appData.CD.MT_STAT[1][23].alr_failure.strHMS()
            self.tbldisp_Punching.table[3][2].text.text = self.appData.CD.MT_STAT[1][23].alr_material.strHMS()
            self.tbldisp_Punching.table[2][1].text.text = self.appData.CD.MT_STAT[1][23].stp_failure.strHMS()
            self.tbldisp_Punching.table[3][1].text.text = self.appData.CD.MT_STAT[1][23].stp_material.strHMS()
            self.tbldisp_Punching.table[4][1].text.text = self.appData.CD.MT_STAT[1][23].stp_process.strHMS()
            self.tbldisp_Punching.table[5][1].text.text = self.appData.CD.MT_STAT[1][23].stp_quality.strHMS()

            self.tbldisp_Punching.table[6][1].text.text = self.appData.CD.MT_STAT[1][23].stp_sum.strHMS()
            self.tbldisp_Punching.table[6][2].text.text = self.appData.CD.MT_STAT[1][23].alr_sum.strHMS()

            #self.tbldisp_Punching.table[5][1].text.text = self.appData.MT_STAT[1]

        # update table <Металлообработка:Гибка>

        # update table <Порошковая покраска>




        #

        self.fp_MT01.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT02.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT03.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT04.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT05.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT06.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT07.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT08.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT09.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT10.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT11.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT12.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT13.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT14.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT15.blinker = self.appData.FOOTPRINT_BLINKER.Q
        self.fp_MT16.blinker = self.appData.FOOTPRINT_BLINKER.Q

        #

        self.update()

    ####################################################################################################################