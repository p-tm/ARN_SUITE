########################################################################################################################
import sys

from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtCore import QTime
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtGui import QPixmap

from datetime import timedelta

########################################################################################################################

from const import *
from enums import *

from udt_rect_frame import UDT_RECT_FRAME
from udt_rect_text_field import UDT_RECT_TEXT_FIELD

########################################################################################################################
# описание класса:
# - на этом виджете придётся рисовать вручную )))
#
########################################################################################################################

class WIDGET_ARBMON_PANE_ALARM(QWidget):

    ####################################################################################################################

    def __init__(self, app_data, id, view_type):

        super().__init__()

        self.appData = app_data

        #

        self.mtID = id
        self.mtNickname = "n/d"
        self.mtCaption = "n/d"
        self.buttonTime = QTime(0, 0, 0)
        self.onCondition = False
        self.viewType = view_type   # 0 = unknown
                            # 1 = тревога/поломка
                            # 2 = тревога/материал
                            # 3 = отключение/поломка
                            # 4 = отключение/материал
                            # 5 = отключение/процесс
                            # 6 = отключение/качество

        if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
            self.baseColor = QColor("#FFFFFF")
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL:
            self.baseColor = QColor("#FFFF00")
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL or self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS or self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY:
            self.baseColor = QColor("#FF0000")

        #

        self.tabCaption = ""

        self.frame_1 = UDT_RECT_FRAME()
        self.label_stanok = UDT_RECT_TEXT_FIELD()
        self.mt_nickname = UDT_RECT_TEXT_FIELD()

        self.frame_2 = UDT_RECT_FRAME()
        self.mt_caption = UDT_RECT_TEXT_FIELD()
        self.event_type_1 = UDT_RECT_TEXT_FIELD()
        self.event_type_2 = UDT_RECT_TEXT_FIELD()

        self.frame_3 = UDT_RECT_FRAME()
        self.litera_1 = UDT_RECT_TEXT_FIELD()

        self.frame_4 = UDT_RECT_FRAME()
        self.litera_2 = UDT_RECT_TEXT_FIELD()

        self.frame_5 = UDT_RECT_FRAME()
        self.label_button_time = UDT_RECT_TEXT_FIELD()
        self.button_time = UDT_RECT_TEXT_FIELD()

        self.clock_string = UDT_RECT_TEXT_FIELD()
        self.logo_label = QPixmap(self.appData.str_ResDir + "/logo_arneg_russia.png")

        self.initUI()

    ####################################################################################################################

    def initUI(self):

        k_1ST_FRAME_WIDTH = 0.15
        k_2ND_FRAME_WIDTH = 0.35
        k_3RD_FRAME_WIDTH = 0.05
        k_4TH_FRAME_WIDTH = 0.05
        k_5TH_FRAME_WIDTH = 0.4 + 0.01

        k_1ST_FRAME_X = k_1ST_FRAME_WIDTH/2.0 - 0.001
        k_2ND_FRAME_X = k_1ST_FRAME_WIDTH + k_2ND_FRAME_WIDTH/2.0 - 0.001
        k_3RD_FRAME_X = k_1ST_FRAME_WIDTH + k_2ND_FRAME_WIDTH + k_3RD_FRAME_WIDTH/2.0 - 0.001
        k_4TH_FRAME_X = k_1ST_FRAME_WIDTH + k_2ND_FRAME_WIDTH + k_3RD_FRAME_WIDTH + k_4TH_FRAME_WIDTH/2.0 - 0.001
        k_5TH_FRAME_X = k_1ST_FRAME_WIDTH + k_2ND_FRAME_WIDTH + k_3RD_FRAME_WIDTH + k_4TH_FRAME_WIDTH + k_5TH_FRAME_WIDTH/2.0 - 0.001

        k_FRAME_Y = 0.505
        k_FRAME_HEIGHT = 1.0

        if GC.__FOUR_MON__:
            px_FRAME_THICKNESS = 2
        elif GC.__FOUR_MON_4K__:
            px_FRAME_THICKNESS = 4
        else:
            px_FRAME_THICKNESS = 2



        self.frame_1.relX0 = k_1ST_FRAME_X
        self.frame_1.relY0 = k_FRAME_Y
        self.frame_1.relWidth = k_1ST_FRAME_WIDTH
        self.frame_1.relHeight = k_FRAME_HEIGHT
        self.frame_1.visible = True
        self.frame_1.pxThickness = px_FRAME_THICKNESS
        self.frame_1.color = self.baseColor

        self.label_stanok.frame.relX0 = k_1ST_FRAME_X
        if GC.__FOUR_MON__:
            self.label_stanok.frame.relY0 = 0.20
        elif GC.__FOUR_MON_4K__:
            self.label_stanok.frame.relY0 = 0.20
        else:
            self.label_stanok.frame.relY0 = 0.15
        self.label_stanok.frame.relWidth = k_1ST_FRAME_WIDTH
        self.label_stanok.frame.relHeight = 0.30
        self.label_stanok.frame.visible = False
        self.label_stanok.frame.pxThickness = 1
        self.label_stanok.frame.color = self.baseColor
        self.label_stanok.text.text = "Станок"
        self.label_stanok.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.label_stanok.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.label_stanok.text.pxSize = 120
        else:
            self.label_stanok.text.pxSize = 20
        self.label_stanok.text.bold = False

        self.mt_nickname.frame.relX0 = k_1ST_FRAME_X
        if GC.__FOUR_MON__:
            self.mt_nickname.frame.relY0 = 0.55
        elif GC.__FOUR_MON_4K__:
            self.mt_nickname.frame.relY0 = 0.55
        else:
            self.mt_nickname.frame.relY0 = 0.15 + (1.0 - 0.15 * 2.0) / 2.0
        self.mt_nickname.frame.relWidth = k_1ST_FRAME_WIDTH
        self.mt_nickname.frame.relHeight = 1.0 - 0.30
        self.mt_nickname.frame.visible = False
        self.mt_nickname.frame.pxThickness = 1
        self.mt_nickname.frame.color = self.baseColor
        self.mt_nickname.text.text = self.mtNickname
        self.mt_nickname.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.mt_nickname.text.pxSize = 100
        elif GC.__FOUR_MON_4K__:
            self.mt_nickname.text.pxSize = 200
        else:
            self.mt_nickname.text.pxSize = 50
        self.mt_nickname.text.bold = True

        self.frame_2.relX0 = k_2ND_FRAME_X
        self.frame_2.relY0 = k_FRAME_Y
        self.frame_2.relWidth = k_2ND_FRAME_WIDTH
        self.frame_2.relHeight = k_FRAME_HEIGHT
        self.frame_2.visible = True
        self.frame_2.pxThickness = px_FRAME_THICKNESS
        self.frame_2.color = self.baseColor

        self.mt_caption.frame.relX0 = k_2ND_FRAME_X
        if GC.__FOUR_MON__:
            self.mt_caption.frame.relY0 = 0.20
        elif GC.__FOUR_MON_4K__:
            self.mt_caption.frame.relY0 = 0.20
        else:
            self.mt_caption.frame.relY0 = 0.15
        self.mt_caption.frame.relWidth = k_2ND_FRAME_WIDTH
        self.mt_caption.frame.relHeight = 0.30
        self.mt_caption.frame.visible = False
        self.mt_caption.frame.pxThickness = 1
        self.mt_caption.frame.color = self.baseColor
        self.mt_caption.text.text = self.mtCaption
        self.mt_caption.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.mt_caption.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.mt_caption.text.pxSize = 120
        else:
            self.mt_caption.text.pxSize = 20
        self.mt_caption.text.bold = False

        self.event_type_1.frame.relX0 = k_2ND_FRAME_X
        if GC.__FOUR_MON__:
            self.event_type_1.frame.relY0 = 0.50
        elif GC.__FOUR_MON_4K__:
            self.event_type_1.frame.relY0 = 0.50
        else:
            self.event_type_1.frame.relY0 = 0.45
        self.event_type_1.frame.relWidth = k_2ND_FRAME_WIDTH
        self.event_type_1.frame.relHeight = 0.30
        self.event_type_1.frame.visible = False
        self.event_type_1.frame.pxThickness = 1
        self.event_type_1.frame.color = self.baseColor
        if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
            self.event_type_1.text.text = "--"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL:
            self.event_type_1.text.text = "Тревога"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL or self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS or self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY:
            self.event_type_1.text.text = "Остановка"
        self.event_type_1.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.event_type_1.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.event_type_1.text.pxSize = 120
        else:
            self.event_type_1.text.pxSize = 20
        self.event_type_1.text.bold = False

        self.event_type_2.frame.relX0 = k_2ND_FRAME_X
        if GC.__FOUR_MON__:
            self.event_type_2.frame.relY0 = 0.80
        elif GC.__FOUR_MON_4K__:
            self.event_type_2.frame.relY0 = 0.80
        else:
            self.event_type_2.frame.relY0 = 0.75
        self.event_type_2.frame.relWidth = k_2ND_FRAME_WIDTH
        self.event_type_2.frame.relHeight = 0.30
        self.event_type_2.frame.visible = False
        self.event_type_2.frame.pxThickness = 1
        self.event_type_2.frame.color = self.baseColor
        if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
            self.event_type_2.text.text = "--"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE:
            self.event_type_2.text.text = "Поломка"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL or self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL:
            self.event_type_2.text.text = "Материал"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS:
            self.event_type_2.text.text = "Процесс"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY:
            self.event_type_2.text.text = "Качество"
        self.event_type_2.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.event_type_2.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.event_type_2.text.pxSize = 120
        else:
            self.event_type_2.text.pxSize = 20
        self.event_type_2.text.bold = False

        self.frame_3.relX0 = k_3RD_FRAME_X
        self.frame_3.relY0 = k_FRAME_Y
        self.frame_3.relWidth = k_3RD_FRAME_WIDTH
        self.frame_3.relHeight = k_FRAME_HEIGHT
        self.frame_3.visible = True
        self.frame_3.pxThickness = px_FRAME_THICKNESS
        self.frame_3.color = self.baseColor

        self.litera_1.frame.relX0 = k_3RD_FRAME_X
        self.litera_1.frame.relY0 = 0.5
        self.litera_1.frame.relWidth = k_3RD_FRAME_WIDTH
        self.litera_1.frame.relHeight = 0.990
        self.litera_1.frame.visible = False
        self.litera_1.frame.pxThickness = 1
        self.litera_1.frame.color = self.baseColor
        if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
            self.litera_1.text.text = "--"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL:
            self.litera_1.text.text = "Т"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL or self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY or self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS:
            self.litera_1.text.text = "О"
        self.litera_1.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.litera_1.text.pxSize = 128
        elif GC.__FOUR_MON_4K__:
            self.litera_1.text.pxSize = 256
        else:
            self.litera_1.text.pxSize = 64
        self.litera_1.text.bold = True

        self.frame_4.relX0 = k_4TH_FRAME_X
        self.frame_4.relY0 = k_FRAME_Y
        self.frame_4.relWidth = k_4TH_FRAME_WIDTH
        self.frame_4.relHeight = k_FRAME_HEIGHT
        self.frame_4.visible = True
        self.frame_4.pxThickness = px_FRAME_THICKNESS
        self.frame_4.color = self.baseColor

        self.litera_2.frame.relX0 = k_4TH_FRAME_X
        self.litera_2.frame.relY0 = 0.5
        self.litera_2.frame.relWidth = k_4TH_FRAME_WIDTH
        self.litera_2.frame.relHeight = 0.990
        self.litera_2.frame.visible = False
        self.litera_2.frame.pxThickness = 1
        self.litera_2.frame.color = self.baseColor
        if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
            self.litera_2.text.text = "--"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE or self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE:
            self.litera_2.text.text = "П"
        if self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL or self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL:
            self.litera_2.text.text = "М"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS:
            self.litera_2.text.text = "П"
        if self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY:
            self.litera_2.text.text = "К"
        self.litera_2.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.litera_2.text.pxSize = 128
        elif GC.__FOUR_MON_4K__:
            self.litera_2.text.pxSize = 256
        else:
            self.litera_2.text.pxSize = 64
        self.litera_2.text.bold = True

        self.frame_5.relX0 = k_5TH_FRAME_X
        self.frame_5.relY0 = k_FRAME_Y
        self.frame_5.relWidth = k_5TH_FRAME_WIDTH
        self.frame_5.relHeight = k_FRAME_HEIGHT
        self.frame_5.visible = True
        self.frame_5.pxThickness = px_FRAME_THICKNESS
        self.frame_5.color = self.baseColor

        self.label_button_time.frame.relX0 = k_5TH_FRAME_X
        if GC.__FOUR_MON__:
            self.label_button_time.frame.relY0 = 0.20
        elif GC.__FOUR_MON_4K__:
            self.label_button_time.frame.relY0 = 0.20
        else:
            self.label_button_time.frame.relY0 = 0.15
        self.label_button_time.frame.relWidth = k_5TH_FRAME_WIDTH
        self.label_button_time.frame.relHeight = 0.30
        self.label_button_time.frame.visible = False
        self.label_button_time.frame.pxThickness = 1
        self.label_button_time.frame.color = self.baseColor
        self.label_button_time.text.text = "Время с начала нажатия кнопки"
        self.label_button_time.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.label_button_time.text.pxSize = 60
        elif GC.__FOUR_MON_4K__:
            self.label_button_time.text.pxSize = 120
        else:
            self.label_button_time.text.pxSize = 20
        self.label_button_time.text.bold = False

        self.button_time.frame.relX0 = k_5TH_FRAME_X
        if GC.__FOUR_MON__:
            self.button_time.frame.relY0 = 0.55
        elif GC.__FOUR_MON_4K__:
            self.button_time.frame.relY0 = 0.55
        else:
            self.button_time.frame.relY0 = 0.15 + ( 1.0 - 0.15 * 2.0 )/2.0
        self.button_time.frame.relWidth = k_5TH_FRAME_WIDTH
        self.button_time.frame.relHeight = 1.0 - 0.30
        self.button_time.frame.visible = False
        self.button_time.frame.pxThickness = 1
        self.button_time.frame.color = self.baseColor
        self.button_time.text.text = "00:00:00"
        self.button_time.text.color = self.baseColor
        if GC.__FOUR_MON__:
            self.button_time.text.pxSize = 100
        elif GC.__FOUR_MON_4K__:
            self.button_time.text.pxSize = 200
        else:
            self.button_time.text.pxSize = 50
        self.button_time.text.bold = True


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

        self.frame_1.draw(painter, bw=cur_w, bh=cur_h)
        self.label_stanok.draw(painter, bw=cur_w, bh=cur_h)
        self.mt_nickname.draw(painter, bw=cur_w, bh=cur_h)

        self.frame_2.draw(painter, bw=cur_w, bh=cur_h)
        self.mt_caption.draw(painter, bw=cur_w, bh=cur_h)
        self.event_type_1.draw(painter, bw=cur_w, bh=cur_h)
        self.event_type_2.draw(painter, bw=cur_w, bh=cur_h)

        self.frame_3.draw(painter, bw=cur_w, bh=cur_h)
        self.litera_1.draw(painter, bw=cur_w, bh=cur_h)

        self.frame_4.draw(painter, bw=cur_w, bh=cur_h)
        self.litera_2.draw(painter, bw=cur_w, bh=cur_h)

        self.frame_5.draw(painter, bw=cur_w, bh=cur_h)
        self.label_button_time.draw(painter, bw=cur_w, bh=cur_h)
        self.button_time.draw(painter, bw=cur_w, bh=cur_h)

        self.clock_string.draw(painter, bw=cur_w, bh=cur_h)

        source = QRectF(0, 0, 1000, 1000)
        if GC.__FOUR_MON__:
            target = QRectF(2, cur_h - 50, 1000, 1000)
        elif GC.__FOUR_MON_4K__:
            target = QRectF(2, cur_h - 125, 2000, 2000)
        else:
            target = QRectF(2, cur_h - 20, 400, 400)
        painter.drawPixmap(target, self.logo_label, source)


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):


        if self.appData.MACHINE_TOOLS.count() > 0:

            self.mtNickname = self.appData.MACHINE_TOOLS[self.mtID - 1].tag
            self.mtCaption = self.appData.MACHINE_TOOLS[self.mtID - 1].caption

        #

        self.mt_nickname.text.text = self.mtNickname
        self.mt_caption.text.text = self.mtCaption

        #

        xTime = QTime(23, 59, 59)   # это максимальное значение, которое принимает QTime
        zTime = QTime(18, 18, 18)


        if self.appData.CD.MT_STAT.count() > 0:

            if self.viewType == ENM_ALARM_PANE_TYPE.UNKNOWN:
                zTime = zTime
            if self.viewType == ENM_ALARM_PANE_TYPE.ALR_FAILURE:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].alr_failure
            if self.viewType == ENM_ALARM_PANE_TYPE.ALR_MATERIAL:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].alr_material
            if self.viewType == ENM_ALARM_PANE_TYPE.STP_FAILURE:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].stp_failure
            if self.viewType == ENM_ALARM_PANE_TYPE.STP_MATERIAL:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].stp_material
            if self.viewType == ENM_ALARM_PANE_TYPE.STP_PROCESS:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].stp_process
            if self.viewType == ENM_ALARM_PANE_TYPE.STP_QUALITY:
                zTime = self.appData.CD.MT_STAT[0][self.mtID - 1].stp_quality

        self.button_time.text.text = zTime.strHMS()

        #

        txt = self.appData.CD.time.toString("hh:mm:ss")

        self.clock_string.text.text = txt

        self.update()

    ####################################################################################################################