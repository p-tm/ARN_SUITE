from PyQt5.QtCore import QDate, QTime, QDateTime

class UDT_ARTERM_APP_SETTINGS():

    def __init__(self):

        self.ms_CHANGE_ALARM_WIDGET = 0
        self.ms_RUNNING_CAPTION_TICK = 0
        self.ms_SHOW_WORKSHOP = 0
        self.ms_SHOW_DIAGRAMS = 0

        self.path_ReportFolder = ""
        self.date_ReportBeginDate = QDate() # как сделать например "вчера", я вроде делал в argate
        self.date_ReportEndDate = QDate().currentDate()
        self.time_ReportBeginTime = QTime()
        self.time_ReportEndTime = QTime()
        self.enum_ReportSortBy = 0

