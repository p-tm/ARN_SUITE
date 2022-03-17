from PyQt5.QtCore import QTime

class UDT_INTERVAL():

    def __init__(self):

        self.value = 0      # main storage - total [ms]
        self.dd = 0
        self.dd_hh = 0      # hours from 00 to 24
        self.hh = 0
        self.mm = 0
        self.ss = 0
        self.ms = 0

    def regen(self):

        self.dd, rem = divmod(self.value, 86400000)
        self.hh, rem = divmod(rem, 3600000)
        self.mm, rem = divmod(rem, 60000)
        self.ms, rem = divmod(rem, 1000)
        #self.dd_hh = self.value - self.dd * 86400000

    def fromHMS(self,h=0,m=0,s=0,ms=0):

        self.value = h*3600000 + m*60000 + s*1000 + ms
        self.dd = 0
        self.dd_hh = h
        self.hh = h
        self.mm = m
        self.ss = s
        self.ms = ms

    @staticmethod
    def s_fromHMS(h=0,m=0,s=0,ms=0):

        x = UDT_INTERVAL()

        x.value = h*3600000 + m*60000 + s*1000 + ms
        x.dd = 0
        x.dd_hh = h
        x.hh = h
        x.mm = m
        x.ss = s
        x.ms = ms

        return x


    def fromQTime(self, tm):

        h = tm.hour()
        m = tm.minute()
        s = tm.second()
        _ms = tm.msec()

        self.value = h * 3600000 + m * 60000 + s * 1000 + _ms
        self.dd = 0
        self.dd_hh = h
        self.hh = h
        self.mm = m
        self.ss = s
        self.ms = _ms

    def toQTime(self):

        tm = QTime()

        return QTime(self.dd_hh,self.mm,self.ss,self.ms)

    def strHMS(self):

        return str(self.hh).zfill(2) + ":" + str(self.mm).zfill(2) + ":" + str(self.ss).zfill(2)





