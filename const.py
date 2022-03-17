#################################################################




#################################################################
# описание класса:                                              #
# Класс для объявления глобальных констант                      #
#################################################################

class GC():

    YES                 = True
    NO                  = False

    NO_ERROR            = 0

    COLOR_NODATA_R                 = 92
    COLOR_NODATA_G                 = 92
    COLOR_NODATA_B                 = 160

    COLOR_HEADER_R                 = 220
    COLOR_HEADER_G                 = 220
    COLOR_HEADER_B                 = 220

    COLOR_WEEKEND_R                 = 255
    COLOR_WEEKEND_G                 = 220
    COLOR_WEEKEND_B                 = 220

    COLOR_SHIFT_NO_DATA_R           = 127
    COLOR_SHIFT_NO_DATA_G           = 255
    COLOR_SHIFT_NO_DATA_B           = 255

    COLOR_DATA_DURING_DAYOUT_R      = 255
    COLOR_DATA_DURING_DAYOUT_G      = 255
    COLOR_DATA_DURING_DAYOUT_B      = 0

    COLOR_STP_ALARM_R               = 255
    COLOR_STP_ALARM_G               = 255
    COLOR_STP_ALARM_B               = 0

    COLOR_STP_CRITICAL_R            = 255
    COLOR_STP_CRITICAL_G            = 0
    COLOR_STP_CRITICAL_B            = 0

    __FOUR_MON__                    = False  # for 4x FullHD scale 100% - for BIGMON
    __FOUR_MON_4K__                 = True  # for 4x 3840*2160 scale 225% - for BIGMON

    monitor_px_width = 0
    monitor_px_height = 0

    @staticmethod
    def initialize():

        # for BIGMON only

        if GC.__FOUR_MON__:
            GC.monitor_px_width = 1920 * 2
            GC.monitor_px_height = 1080 * 2
        elif GC.__FOUR_MON_4K__:
            GC.monitor_px_width = 3840 * 2
            GC.monitor_px_height = 2160 * 2
        else:
            GC.monitor_px_width = 1920
            GC.monitor_px_height = 1080

