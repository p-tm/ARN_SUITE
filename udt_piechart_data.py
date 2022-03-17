from udt_arr import UDT_ARR
from udt_interval import UDT_INTERVAL


class UDT_PIECHART_DATA():

    def __init__(self):

        self.value_total = None
        self.zero_total = True
        self.includeZeroWedges = True
        self.ready = False

        self.WEDGES = UDT_ARR()     # list<UDT_PIECHART_WEDGE>

        self.values = list([])
        self.chart_labels = list([])
        self.legend_labels = list([])

    def update(self):

        tot = 0

        for wdg in self.WEDGES:
            tot = tot + wdg.time_TIME.value

        self.value_total = tot
        self.zero_total = (self.value_total == 0)

        self.values.clear()
        self.chart_labels.clear()
        self.legend_labels.clear()

        if not self.zero_total:

            for wdg in self.WEDGES:

                wdg.update()
                wdg.value_relative = wdg.value_original / self.value_total

                #if self.includeZeroWedges or( not self.includeZeroWedges and wdg.value_original != 0):
                if self.includeZeroWedges or (not self.includeZeroWedges and wdg.value_relative >= 0.01):

                    self.values.append(wdg.value_relative)
                    self.chart_labels.append(wdg.chart_label)
                    self.legend_labels.append(wdg.legend_label)

        self.ready =( not self.zero_total and len(self.values) > 0 )






