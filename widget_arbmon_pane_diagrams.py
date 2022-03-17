########################################################################################################################

# pip install matplotlib


import sys


from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot


from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem

from PyQt5.QtGui import QColor

from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from udt_matplotlib_figure import UDT_MATPLOTLIB_FIGURE



########################################################################################################################

from const import *
from enums import *
from udt_empty_piechart import UDT_EMPTY_PIECHART

########################################################################################################################



########################################################################################################################
STYLESHEET_LABEL = """
    QLabel {
        color: #FFFF00;
    }
"""

########################################################################################################################

if GC.__FOUR_MON__:

    STYLESHEET_DATE_TIME_STRING = """
        QLabel {
            border: 0px solid #00FFFF;
            padding-left: 10px;
            padding-top: 0px;
            padding-right: 10px;
            padding-bottom: 0px;
            color: #00FF00;
            font-family: Calibri;
            font-size: 60px;
    
        }
    """

elif GC.__FOUR_MON_4K__:

    STYLESHEET_DATE_TIME_STRING = """
        QLabel {
            border: 0px solid #00FFFF;
            padding-left: 10px;
            padding-top: 0px;
            padding-right: 10px;
            padding-bottom: 0px;
            color: #00FF00;
            font-family: Calibri;
            font-size: 120px;

        }
    """

else:

    STYLESHEET_DATE_TIME_STRING = """
        QLabel {
            border: 0px solid #00FFFF;
            padding-left: 5px;
            padding-top: 0px;
            padding-right: 5px;
            padding-bottom: 0px;
            color: #00FF00;
            font-family: Calibri;
            font-size: 20px;

        }
    """

# font: bold;

########################################################################################################################

if GC.__FOUR_MON__:

    STYESHEET_DIAGRAM_HEADER = """
        QLabel {
            font-family: Calibri;
            font-size: 100px;
            color: #FFFF00;
        }
    """

elif GC.__FOUR_MON_4K__:

    STYESHEET_DIAGRAM_HEADER = """
        QLabel {
            font-family: Calibri;
            font-size: 200px;
            color: #FFFF00;
        }
    """

else:

    STYESHEET_DIAGRAM_HEADER = """
        QLabel {
            font-family: Calibri;
            font-size: 24px;
            color: #FFFF00;
        }
    """

########################################################################################################################

class WIDGET_ARBMON_PANE_DIAGRAMS(QWidget):

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.layout_CoreLayout = QGridLayout()
        self.setLayout(self.layout_CoreLayout)

        self.setMinimumWidth(GC.monitor_px_width)   # AB 05.02.22
        self.setMinimumWidth(GC.monitor_px_width)   # AB 05.02.22

        self.widget_Header = QWidget()
        self.widget_LeftDiagram = QWidget()
        self.widget_RightDiagram = QWidget()

        self.widget_Header.setLayout(QHBoxLayout())
        self.widget_LeftDiagram.setLayout(QVBoxLayout())
        self.widget_RightDiagram.setLayout(QVBoxLayout())

        #self.layout_LeftDiagram = self.widget_LeftDiagram.layout()
        #self.layout_RightDiagram = self.widget_RightDiagram.layout()



        self.widget_Header.layout().setAlignment(Qt.AlignCenter)
        self.widget_LeftDiagram.layout().setAlignment(Qt.AlignCenter)
        self.widget_RightDiagram.layout().setAlignment(Qt.AlignCenter)

        self.widget_LeftDiagramTW = QTabWidget()
        self.widget_RightDiagramTW = QTabWidget()

        self.label_LEFT_DIAGRAM_HEADER = QLabel()
        self.label_RIGHT_DIAGRAM_HEADER = QLabel()

        self.widget_LD = UDT_MATPLOTLIB_FIGURE(self, width=200, height=200)      # widget_LEFT_DIAGRAM
        self.widget_RD = UDT_MATPLOTLIB_FIGURE(self, width=200, height=200)      # widget_RIGHT_DIAGRAM

        self.widget_EmptyPieChart1 = UDT_EMPTY_PIECHART()
        self.widget_EmptyPieChart2 = UDT_EMPTY_PIECHART()

        self.widget_DataNotReady1 = UDT_EMPTY_PIECHART()
        self.widget_DataNotReady2 = UDT_EMPTY_PIECHART()

        #-------------------------------------------------------------------------

        self.date_string = QLabel()
        self.clock_string = QLabel()

        self.initUI()

    ####################################################################################################################

    def initUI(self):

        self.layout_CoreLayout.addWidget(self.widget_Header,0,0,1,2)
        self.layout_CoreLayout.addWidget(self.widget_LeftDiagram,1,0,1,1)
        self.layout_CoreLayout.addWidget(self.widget_RightDiagram, 1, 1, 1, 1)

        self.layout_CoreLayout.setContentsMargins(0, 0, 0, 0)
        self.layout_CoreLayout.setSpacing(0)

        self.label_LEFT_DIAGRAM_HEADER.setStyleSheet(STYESHEET_DIAGRAM_HEADER)
        self.label_LEFT_DIAGRAM_HEADER.setText("ОСТАНОВКА ШТАМПОВКА")
        #self.label_LEFT_DIAGRAM_HEADER.setMaximumHeight(30)
        self.label_LEFT_DIAGRAM_HEADER.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.label_LEFT_DIAGRAM_HEADER.setMinimumHeight(400)
        self.label_LEFT_DIAGRAM_HEADER.setMaximumHeight(400)

        self.label_RIGHT_DIAGRAM_HEADER.setStyleSheet(STYESHEET_DIAGRAM_HEADER)
        self.label_RIGHT_DIAGRAM_HEADER.setText("ОСТАНОВКА ГИБКА")
        self.label_RIGHT_DIAGRAM_HEADER.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.label_RIGHT_DIAGRAM_HEADER.setMinimumHeight(400)
        self.label_RIGHT_DIAGRAM_HEADER.setMaximumHeight(400)


        self.widget_Header.setMaximumHeight(160)    # тут header это только часы вроде...
        self.widget_Header.setMinimumHeight(160)
        self.widget_Header.layout().setContentsMargins(0, 0, 0, 0)

        #self.label_LEFT_DIAGRAM_HEADER.setMinimumHeight(100)


        #self.sc1.axes = self.sc1.fig.add_subplot(111)
        #self.widget_LD.fig.set_edgecolor("#FF0000")
        self.widget_LD.fig.set_facecolor("#000000")
        #self.widget_LD.fig.set_frameon(False)
        #self.widget_LD.fig.set_linewidth(1)

        #self.widget_LD.axes.legend(labels=("1","2"), loc="lower right")
        #self.widget_LD.axes.set_title("график")
        #self.widget_LD.axes.pie([self.p1,self.p2], labels=["20","80"], autopct="%1.1f%%")

        #self.piechart_A = self.sc1.fig.add_subplot(111)
        #self.piechart_A.pie()

        self.widget_LeftDiagram.layout().addWidget(self.label_LEFT_DIAGRAM_HEADER)
        self.widget_LeftDiagram.layout().addWidget(self.widget_LeftDiagramTW)

        self.widget_LeftDiagramTW.addTab(self.widget_LD,"1")
        self.widget_LeftDiagramTW.addTab(self.widget_EmptyPieChart1, "2")
        self.widget_LeftDiagramTW.addTab(self.widget_DataNotReady1, "3")
        self.widget_LeftDiagramTW.tabBar().hide()

        self.widget_RD.fig.set_facecolor("#000000")

        self.widget_RightDiagram.layout().addWidget(self.label_RIGHT_DIAGRAM_HEADER)
        self.widget_RightDiagram.layout().addWidget(self.widget_RightDiagramTW)

        self.widget_RightDiagramTW.addTab(self.widget_RD,"1")
        self.widget_RightDiagramTW.addTab(self.widget_EmptyPieChart2, "2")
        self.widget_RightDiagramTW.addTab(self.widget_DataNotReady2, "3")
        self.widget_RightDiagramTW.tabBar().hide()

        # -------------------------------------------------------------------------

        self.widget_DataNotReady1.fill_color = QColor("#808080")
        self.widget_DataNotReady1.caption = "данные\nне готовы"
        self.widget_DataNotReady1.caption_color = QColor("#000000")

        self.widget_DataNotReady2.fill_color = QColor("#808080")
        self.widget_DataNotReady2.caption = "данные\nне готовы"
        self.widget_DataNotReady2.caption_color = QColor("#000000")

        # -------------------------------------------------------------------------

        self.widget_Header.layout().addStretch(1)
        self.widget_Header.layout().addWidget(self.date_string)
        self.widget_Header.layout().addWidget(self.clock_string)

        self.date_string.setStyleSheet(STYLESHEET_DATE_TIME_STRING)
        self.clock_string.setStyleSheet(STYLESHEET_DATE_TIME_STRING)


    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnUpdateWindow(self):

        #makepct = lambda z: str(z)

        #def make_autopct(val):
        #    def my_autopct(pct):
        #        return str(pct)
        #    return my_autopct
        #def make_pct(pct):
        #    return "{:.1f}%".format(pct*100.0)

        if GC.__FOUR_MON__:
            fsz = 13.0
        elif GC.__FOUR_MON_4K__:
            fsz = 26.0
        else:
            fsz = 6.5

        self.widget_LD.axes.clear()
        self.widget_RD.axes.clear()

        if self.appData.PIECHART_1_DATA.ready:

            if not self.appData.PIECHART_1_DATA.zero_total:

                #explode = (0.1, 0.1, 0.1, 0.1, 0.1)


                wedges, texts, autotexts = self.widget_LD.axes.pie(
                    x           = self.appData.PIECHART_1_DATA.values,
                    labels      = self.appData.PIECHART_1_DATA.chart_labels,
                    #textprops   = {"fontsize": 12},
                    #explode     = explode,
                    shadow      = False,
                    #autopct     = make_autopct(self.appData.PIECHART_1_DATA.values)
                    #autopct     = lambda val: make_pct(val)
                    autopct     = "%.1f%%",
                    radius      = 0.75,
                    wedgeprops  = {"linewidth": 0.5, "edgecolor":"#FFFFFF"}
                )

                #for wdg in wedges:
                #    wdg.edgecolor = "#FFFF00"
                #    #wdg.set_width(2)
                for txt in texts:
                    if GC.__FOUR_MON__:
                        txt.set_fontsize(12)
                    elif GC.__FOUR_MON_4K__:
                        txt.set_fontsize(24)
                    else:
                        txt.set_fontsize(6)
                    txt.set_color("#FFFF00")
                    txt.set_fontweight("bold")
                for atxt in autotexts:
                    if GC.__FOUR_MON__:
                        atxt.set_fontsize(18)
                    elif GC.__FOUR_MON_4K__:
                        atxt.set_fontsize(36)
                    else:
                        atxt.set_fontsize(9)
                    atxt.set_color("#FFFF00")


                #pyplot.setp(texts, fontweight=1)

                columns_no = len(wedges)

                self.widget_LD.axes.legend(
                    handles         = wedges,
                    labels          = self.appData.PIECHART_1_DATA.legend_labels,
                    labelcolor      = "#FFFF00",
                    loc             = "center",
                    bbox_to_anchor  = (0.5, 0.025),
                    fontsize        = fsz,
                    ncol            = 5,
                    frameon         = False,
                    fancybox        = False,
                    framealpha      = 1.0,
                    handlelength    = 0.9,
                    facecolor       = "#FF0000",
                    edgecolor       = "#FF0000")

                self.widget_LD.draw()
                self.widget_LeftDiagramTW.setCurrentIndex(0)

            #else:
            #    self.widget_LeftDiagramTW.setCurrentIndex(1)
        else:
            self.widget_LeftDiagramTW.setCurrentIndex(1)


        if self.appData.PIECHART_2_DATA.ready:

            if not self.appData.PIECHART_2_DATA.zero_total:

                #explode = (0.1, 0.1, 0.1, 0.1, 0.1)


                wedges, texts, autotexts = self.widget_RD.axes.pie(
                    x           = self.appData.PIECHART_2_DATA.values,
                    labels      = self.appData.PIECHART_2_DATA.chart_labels,
                    #textprops   = {"fontsize": 12},
                    #explode     = explode,
                    shadow      = False,
                    #autopct     = make_autopct(self.appData.PIECHART_1_DATA.values)
                    #autopct     = lambda val: make_pct(val)
                    autopct     = "%.1f%%",
                    radius      = 0.75,
                    wedgeprops  = {"linewidth": 0.5, "edgecolor":"#FFFFFF"}
                )

                for txt in texts:
                    if GC.__FOUR_MON__:
                        txt.set_fontsize(12)
                    elif GC.__FOUR_MON_4K__:
                        txt.set_fontsize(24)
                    else:
                        txt.set_fontsize(6)
                    txt.set_color("#FFFF00")
                    txt.set_fontweight("bold")
                for atxt in autotexts:
                    if GC.__FOUR_MON__:
                        atxt.set_fontsize(18)
                    elif GC.__FOUR_MON_4K__:
                        atxt.set_fontsize(36)
                    else:
                        atxt.set_fontsize(9)
                    atxt.set_color("#FFFF00")

                #pyplot.setp(texts, fontweight=1)
                #for k, patch in enumerate(wedges):
                #    texts[k].set_color("#FFFF00")

                columns_no = len(wedges)

                self.widget_RD.axes.legend(
                    handles         = wedges,
                    labels          = self.appData.PIECHART_2_DATA.legend_labels,
                    labelcolor      = "#FFFF00",
                    loc             = "center",
                    bbox_to_anchor  = (0.5, 0.025),
                    fontsize        = fsz,
                    ncol            = 5,
                    frameon         = False,
                    fancybox        = False,
                    framealpha      = 1.0,
                    handlelength    = 0.9,
                    facecolor       = "#FF0000",
                    edgecolor       = "#FF0000")

                self.widget_RD.draw()
                self.widget_RightDiagramTW.setCurrentIndex(0)

            #else:
            #    self.widget_RightDiagramTW.setCurrentIndex(1)
        else:
            self.widget_RightDiagramTW.setCurrentIndex(1)

        # -------------------------------------------------------------------------
        """
        #self.widget_LeftDiagramTW.setMinimumWidth(self.width() / 2)
        self.widget_LeftDiagramTW.setMaximumWidth(self.width() / 2)

        self.widget_RightDiagramTW.setMinimumWidth(self.width() / 2)
        #self.widget_RightDiagramTW.setMaximumWidth(self.width() / 2)
        """

        self.widget_LeftDiagramTW.setMinimumWidth(GC.monitor_px_width / 2)
        self.widget_LeftDiagramTW.setMaximumWidth(GC.monitor_px_width / 2)

        self.widget_RightDiagramTW.setMinimumWidth(GC.monitor_px_width / 2)
        self.widget_RightDiagramTW.setMaximumWidth(GC.monitor_px_width / 2)

        # -------------------------------------------------------------------------
        #self.date_string.setText("Дата: " + self.appData.CD.date.toString("dd.MM.yyyy"))
        #self.clock_string.setText("Время: " + self.appData.CD.time.toString("hh:mm:ss"))
        self.date_string.setText(self.appData.CD.date.toString("dd.MM.yyyy"))
        self.clock_string.setText(self.appData.CD.time.toString("hh:mm:ss"))

    ####################################################################################################################


