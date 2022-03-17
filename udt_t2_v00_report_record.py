from PyQt5.QtCore import QDate, QTime

class UDT_T2_V00_REPORT_RECORD():

    def __init__(self):

        self.rec_id = 0
        self.day_id = 0
        self.month_id = 0
        self.month_w_year = 0
        self.year_id = 0
        self.the_date = QDate()
        self.is_dayout = False
        self.rec_type = 0

        self.day_cl1_mt1_stp_time = None
        self.day_cl1_mt2_stp_time = None
        self.day_cl1_mt3_stp_time = None
        self.day_cl1_mt4_stp_time = None
        self.day_cl1_mt5_stp_time = None
        self.day_cl1_stp_sum = None
        self.day_cl1_stp_sum_prc = None
        self.day_cl1_reference_time = None

        self.day_cl2_mt6_stp_time = None
        self.day_cl2_mt7_stp_time = None
        self.day_cl2_mt8_stp_time = None
        self.day_cl2_mt9_stp_time = None
        self.day_cl2_mt10_stp_time = None
        self.day_cl2_mt11_stp_time = None
        self.day_cl2_mt12_stp_time = None
        self.day_cl2_mt13_stp_time = None
        self.day_cl2_mt14_stp_time = None
        self.day_cl2_stp_sum = None
        self.day_cl2_stp_sum_prc = None
        self.day_cl2_reference_time = None

        self.day_cl3_mt15_stp_time = None
        self.day_cl3_stp_sum = None
        self.day_cl3_stp_sum_prc = 0.0
        self.day_cl3_reference_time = None

        self.day_cl4_mt16_stp_time = None
        self.day_cl4_stp_sum = None
        self.day_cl4_stp_sum_prc = 0.0
        self.day_cl4_reference_time = None

        self.day_mt1_stp_failure = None
        self.day_mt1_stp_material = None
        self.day_mt1_stp_process = None
        self.day_mt1_stp_quality = None
        self.day_mt1_stp_offline = None
        self.day_mt1_alr_failure = None
        self.day_mt1_alr_material = None
        self.day_mt1_stp_sum = None
        self.day_mt1_alr_sum = None



        self.is_valid = False
