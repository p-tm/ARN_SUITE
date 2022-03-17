from enums import *

class GF():

    ####################################################################################################################

    @staticmethod
    def rgbToExcelColor(r,g,b):

        # Excel can use an integer calculated by the formula Red + (Green * 256) + (Blue * 256 * 256)
        ec = r + (g * 256) + (b * 65536)

        return ec

    ####################################################################################################################

    @staticmethod
    def ilim(x, UL, LL):

        if x > UL:
            y = UL
        elif x < LL:
            y = LL
        else:
            y = x

        return y

    ####################################################################################################################

    @staticmethod
    def weekdayIdToString(dow):

        if dow == ENM_WEEKDAYS.MONDAY:
            str = "понедельник"
        else:
            if dow == ENM_WEEKDAYS.TUESDAY:
                str = "вторник"
            else:
                if dow == ENM_WEEKDAYS.WEDNESDAY:
                    str = "среда"
                else:
                    if dow == ENM_WEEKDAYS.THIRSDAY:
                        str = "четверг"
                    else:
                        if dow == ENM_WEEKDAYS.FRIDAY:
                            str = "пятница"
                        else:
                            if dow == ENM_WEEKDAYS.SATURDAY:
                                str = "суббота"
                            else:
                                if dow == ENM_WEEKDAYS.SUNDAY:
                                    str = "воскресенье"
                                else:
                                    str = "ошибка преобразования"

        return str

    ####################################################################################################################
    """
    def isWeekend(self, dow):

        if dow == ENM_WEEKDAYS.SATURDAY or dow == ENM_WEEKDAYS.SUNDAY:
            return True
        else:
            return False
    """
    ####################################################################################################################

    @staticmethod
    def isWeekendToString(b):

        if not b:
            str = "рабочий"
        else:
            str = "выходной"

        return str

    ####################################################################################################################

    @staticmethod
    def yes_no_ToString(b):

        if not b:
            str = "нет"
        else:
            str = "да"

        return str

    ####################################################################################################################

    @staticmethod
    def bool_to_OK_NOK(b):

        if b:
            return "OK"
        else:
            return "NOK"

    ####################################################################################################################

    @staticmethod
    def bool_to_Y_N(b):

        if b:
            return "Y"
        else:
            return "N"

    ####################################################################################################################


