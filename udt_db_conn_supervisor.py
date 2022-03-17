from PyQt5.QtCore import QTime

class UDT_DB_CONN_SUPERVISOR():

    def __init__(self):

        self.DB_READ_STATUS = False     # 0 = problem, 1 = OK # output
        self.DB_DATA_STATUS = False     # 0 = problem, 1 = OK # output

        self.db_read_fail_TO_counter = 0
        self.db_data_fail_TO_counter = 0

        self.db_read_fail_TO = 10
        self.db_data_fail_TO = 20

        self.dbReadConnOK = False        # input
        self.read_time      = QTime()    # input

        self.read_time_Z0   = QTime()
        self.read_time_Z1   = QTime()

    def update(self):

        if self.dbReadConnOK:
            self.DB_READ_STATUS = True
            self.db_read_fail_TO_counter = 0
        else:
            self.db_read_fail_TO_counter += 1
            if self.db_read_fail_TO_counter >= self.db_read_fail_TO:
                self.DB_READ_STATUS = False

        self.read_time_Z0 = self.read_time

        if not(self.read_time is None):
            if self.read_time_Z0 == self.read_time_Z1:
                self.db_data_fail_TO_counter += 1
                if self.db_data_fail_TO_counter >= self.db_data_fail_TO:
                    self.DB_DATA_STATUS = False
            else:
                self.DB_DATA_STATUS = True
                self.db_data_fail_TO_counter = 0

        self.read_time_Z1 = self.read_time_Z0














