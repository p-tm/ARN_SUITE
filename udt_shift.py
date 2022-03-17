from PyQt5.QtCore import QTime

from udt_arr import UDT_ARR

########################################################################################################################
# описание класса:
# - описание смены
########################################################################################################################

#class UDT_SHIFT():
#
#    def __init__(self):
#
#        self.shift_id = None # unique id
#        self.shift_big_id = None
#        self.shift_type_id = None
#        self.shift_number_w_day = None
#        self.b_time = None
#        self.e_time = None
#        #self.active = None
#        self.isNight = None
#        self.isWorkingShift = None
#
#        self.shiftCaption = None

class UDT_SHIFT():

    def __init__(self):

        self.shift_id = None # unique id
        self.shift_big_id = None
        self.shift_type_id = None
        self.shift_number_w_day = None
        self.b_time = None
        self.e_time = None
        #self.active = None
        self.isNight = None
        #self.isWorkingShift = None

        self.shiftCaption = None

        self.SCHEDULED_BREAKS = UDT_ARR() # <UDT_SCHEDULED_BREAKS>