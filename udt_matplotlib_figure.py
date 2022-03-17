from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

########################################################################################################################
# описание класса:
# - для круговых диаграмм
#
########################################################################################################################

class UDT_MATPLOTLIB_FIGURE(FigureCanvasQTAgg): # получается что это pyqt5 wrapper (widget) для matplotlib.figure

    def __init__(self, parent=None, width=100, height=200):

        ww = width/100.0
        hh = height/100.0

        self.fig = Figure(figsize=(ww,hh),dpi=150)
        #self.axes = fig.add_subplot(111)
        super().__init__(self.fig)
        self.axes = self.fig.add_axes([0, 0, 1, 1])