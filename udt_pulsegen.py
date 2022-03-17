########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class UDT_PULSEGEN():

    ####################################################################################################################

    def __init__(self):

        self.nCounter = 0
        self.Q = False

        self.ms_RTx_CALL = 200.0
        self.ms_TIME_ON = 1000.0
        self.ms_TIME_OFF = 1000.0

    ####################################################################################################################

    def update(self):

        self.n_COUNT_ON = self.ms_TIME_ON / self.ms_RTx_CALL
        self.n_COUNT_OFF = self.ms_TIME_OFF / self.ms_RTx_CALL

        self.nCounter += 1

        if self.Q and self.nCounter > self.n_COUNT_ON:
            self.Q = False
            self.nCounter = 0
        if not self.Q and self.nCounter > self.n_COUNT_OFF:
            self.Q = True
            self.nCounter = 0

    ####################################################################################################################
