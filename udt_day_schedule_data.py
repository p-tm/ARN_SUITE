from udt_arr import UDT_ARR

class UDT_DAY_SCHEDULE_DATA():

    ####################################################################################################################

    def __init__(self):

        self.day_id = None
        self.day_big_id = None
        self.date = None
        self.is_weekend = None
        self.is_holiday = None
        self.plan_id = None

        self.plan_tag = None
        self.plan_caption = None
        self.holiday_caption = None

        self.SHIFTS = UDT_ARR() # <UDT_SCHEDULED_BREAK>

    ####################################################################################################################

