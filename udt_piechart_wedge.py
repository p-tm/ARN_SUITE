from udt_interval import UDT_INTERVAL

class UDT_PIECHART_WEDGE():

    def __init__(self, pt=None):

        self.time_TIME = UDT_INTERVAL()
        self.mt_pointer = pt

        self.value_original = None
        self.value_fractional = None
        self.chart_label = "name\nvalue"
        self.legend_label = "name\nvalue"

    def update(self):

        self.value_original = self.time_TIME.value
        if self.mt_pointer is not None:
            self.chart_label = self.mt_pointer.short_cap + "\n" +\
                self.time_TIME.strHMS()
            self.legend_label = self.mt_pointer.short_cap