from PyQt5.QtCore import QTime, QDate

class UDT_ARGATE_APP_SETTINGS():

    def __init__(self):

        self.writeRtDataToDB                = 0
        self.writeStatesHistoryToDB         = 0

        self.reportStartDate                = QDate().currentDate()
        self.dailyReportTime                = QTime(23, 59, 59)
        self.monthReportTime                = QTime(23, 59, 59)
        self.yearReportTime                 = QTime(23, 59, 59)

        self.keepCopyOfReportFileOnServer   = 0
        self.dirForReportFiles              = ""
        self.destEmail                      = ""
        self.show12hShiftsInReportT1        = 0