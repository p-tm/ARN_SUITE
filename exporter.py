########################################################################################################################
# pip install pywin32
import win32com.client
import win32gui
import win32con
import pythoncom
import os

from PyQt5.QtCore import QDate, QTime, QDateTime
#from PyQt5.QtCore import QString

########################################################################################################################

from global_functions import *
from const import *
from enums import *
from udt_arr import UDT_ARR
from udt_interval import UDT_INTERVAL

########################################################################################################################
# описание класса:
# - экспортёр в MS Excel
########################################################################################################################

class EXPORTER():

    ####################################################################################################################

    class xlLineStyle():
        xlContinuous = 1
        xlDash = -4115

    ####################################################################################################################

    class xlHorizontalAlignment():
        xlLeft = -4131
        xlCenter = -4108
        xlRight = -4152

    ####################################################################################################################

    class xlVerticalAlignment():
        xlVAlignBottom = -4107
        xlVAlignCenter = -4108
        xlVAlignTop = -4160

    ####################################################################################################################

    class xlOrientation():
        xlUpward = -4171

    ####################################################################################################################

    def __init__(self):
        pass

    ####################################################################################################################

    #@staticmethod
    def monthCaption(self, m):
        if m == 1: return "январь"
        else:
            if m == 2: return "февраль"
            else:
                if m == 3: return "март"
                else:
                    if m == 4: return "апрель"
                    else:
                        if m == 5: return "май"
                        else:
                            if m == 6: return "июнь"
                            else:
                                if m == 7: return "июль"
                                else:
                                    if m == 8: return "август"
                                    else:
                                        if m == 9: return "сентябрь"
                                        else:
                                            if m == 10: return "октябрь"
                                            else:
                                                if m == 11: return "ноябрь"
                                                else:
                                                    if m == 12: return "декабрь"

    ####################################################################################################################

    #@staticmethod
    def exportToExcel_ReportType1(self, app_data):

        ################################################################################################################

        def extract_time(s):
            start_pos_days = s.find("days")
            start_pos_day = s.find("day")
            first_semicolon = s.find(":")
            if start_pos_days == -1 and start_pos_day == -1: # если нету слова "day" или "days"
                return s[0:first_semicolon+6]
            else:
                if start_pos_days != -1:
                    return s[start_pos_days+4:first_semicolon+6]
                if start_pos_day != -1:
                    return s[start_pos_day+3:first_semicolon+6]

        ################################################################################################################

        def extract_time_hh_mm(s):
            start_pos_days = s.find("days")
            start_pos_day = s.find("day")
            first_semicolon = s.find(":")
            if start_pos_days == -1 and start_pos_day == -1: # если нету слова "day" или "days"
                return s[0:first_semicolon+3]
            else:
                if start_pos_days != -1:
                    return s[start_pos_days+4:first_semicolon+3]
                if start_pos_day != -1:
                    return s[start_pos_day+3:first_semicolon+3]

        ################################################################################################################

        def extract_hours(s):   # !!! нужна защита от пустой строки
            if s == "":
                return 0
            else:
                first_semicolon = s.find(":")
                return int(s[0:first_semicolon])

        ################################################################################################################

        def print_cell( current_row, record, _data, _exists):

            #current_row += 1
            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss, "hh:mm:ss")
                null_time = (ss == "00:00:00")
                null_time_a = (tm == QTime(0,0,0))
            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(255, 255, 192) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if not _exists:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_SHIFT_NO_DATA_R, GC.COLOR_SHIFT_NO_DATA_G, GC.COLOR_SHIFT_NO_DATA_B)
                        sheet.Range(rng).value = "--"
                    else:
                        if null_time:
                            pass
                            # output nothing
                        else:
                            sheet.Range(rng).value = ss
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        def print_cell_shift_stp_sum( current_row, record, _data, _exists, _class):

            # _class - machine_tools_class

            #current_row += 1
            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            # тут поставил грубую заплатку
            # сравнилка времени черех QTime не понимается время больше 24 часов
            # но тут вроде таких времён и нет
            # поэтому можно просто наложить условие hours >= 24
            # если бы надо было сравнивать с 25 часами то так не получилось бы
            # в идеале сделать потом по-нормальному

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss, "hh:mm:ss")
                null_time = (ss == "00:00:00")
                null_time_a = (tm == QTime(0,0,0))
                hours = extract_hours(ss)
                if _class == 1:
                    attention_color = (hours >= 24)or(tm >= QTime(2, 30, 0))
                    critical_color = (hours >= 24)or(tm >= QTime(5, 0, 0))
                if _class == 2:
                    attention_color = (hours >= 24)or(tm >= QTime(4, 30, 0))
                    critical_color = (hours >= 24)or(tm >= QTime(9, 0, 0))
                if _class == 3 or _class == 4:
                    attention_color = (hours >= 24)or(tm >= QTime(1, 30, 0))
                    critical_color = (hours >= 24)or(tm >= QTime(2, 30, 0))
            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(255, 255, 192) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if not _exists:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_SHIFT_NO_DATA_R, GC.COLOR_SHIFT_NO_DATA_G, GC.COLOR_SHIFT_NO_DATA_B)
                        sheet.Range(rng).value = "--"
                    else:
                        if null_time:
                            pass
                            # output nothing
                        else:
                            sheet.Range(rng).value = ss
                            if critical_color:
                                sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_CRITICAL_R, GC.COLOR_STP_CRITICAL_G, GC.COLOR_STP_CRITICAL_B)
                            elif attention_color:
                                sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_ALARM_R, GC.COLOR_STP_ALARM_G, GC.COLOR_STP_ALARM_B)
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        show_12H_shifts = app_data.settings.show12hShiftsInReportT1
        time_data = QTime()
        today = QDate.currentDate()

        pythoncom.CoInitialize()    # !!!!!!!!!!!!!!!!

        excelapp = None
        im_the_only_ExcelApp_object = False

        #excelapp = win32com.client.gencache.EnsureDispatch("Excel.Application")

        #hwnd = win32gui.FindWindow(None,"Microsoft Excel")
        #win32gui.ShowWindow(excelapp.Hwnd, win32con.SW_HIDE)

        try:
            excelapp1 = win32com.client.GetActiveObject("Excel.Application")
        except:
            im_the_only_ExcelApp_object = True
        finally:
            pass

        excelapp = win32com.client.DispatchEx("Excel.Application")

        if im_the_only_ExcelApp_object:
            excelapp.Visible = False
            excelapp.ScreenUpdating = False
            excelapp.DisplayAlerts = False
            excelapp.EnableEvents = False


        workbook = excelapp.Workbooks.Add(1)
        sheet = workbook.Sheets(1)

        # сколько всего дней вообще в запросе - это в любом случае пока так:
        # а также - сколько всего месяцев в запросе

        months_list = UDT_ARR()
        years_list = UDT_ARR()

        rec_date = app_data.T1_REPORT_ARR[0].the_date
        last_record_id = app_data.T1_REPORT_ARR[app_data.T1_REPORT_ARR.count() - 1].rec_id
        m_days = 0
        y_months = 1

        for record in app_data.T1_REPORT_ARR:
            if record.day_id != -1:
                if record.the_date.month() == rec_date.month(): # тут смотрим, что месяц след.записи равен месяцу предыдущ.записи
                    m_days += 1
                else:
                    month_tuple = tuple((rec_date.month(), m_days, rec_date.year()))
                    months_list.append(month_tuple)
                    m_days = 1

                if record.the_date.year() == rec_date.year():
                    if record.the_date.month() != rec_date.month(): # тут смотрим, что год след.записи равен году предыдущ.записи
                        y_months += 1
                else:
                    year_tuple = tuple((rec_date.year(), y_months))
                    years_list.append(year_tuple)
                    y_months = 1


                rec_date = record.the_date

            if record.rec_id == last_record_id:
                month_tuple = tuple((rec_date.month(), m_days, rec_date.year()))
                months_list.append(month_tuple)
                year_tuple = tuple((rec_date.year(), y_months))
                years_list.append(year_tuple)

        months_number = months_list.count()
        years_number = years_list.count()

        # set font for the whole sheet

        start_row = 1
        start_col = 1
        frame_left_upr_corner = sheet.Cells(start_row, start_col).Address

        end_row = app_data.MACHINE_TOOL_CLASSES.count() * app_data.SHIFT_TYPES.count() * 7 * 2
        end_col = app_data.T1_REPORT_ARR.count() * 2
        frame_right_lwr_corner = sheet.Cells(end_row, end_col).Address

        frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)

        rng = frame_full_range

        sheet.Range(rng).Font.Size = 10
        #sheet.Range(rng).Font.FontStyle = "Courier" #??

        sheet.Range("A1").ColumnWidth = 5
        sheet.Range("B1").ColumnWidth = 14
        sheet.Range("C1").ColumnWidth = 20

        # левая шапка(столбец) - по классам станков и по сменам

        current_row = 3
        current_column = 3


        #start_row = 3
        #start_col = 1
        #frame_left_upr_corner = sheet.Cells(start_row, start_col).Address
        #
        #end_row = start_row + 7
        #end_col = start_col
        #frame_right_lwr_corner = sheet.Cells(end_row, end_col).Address
        #
        #frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)
        #rng = frame_full_range
        #
        #sheet.Range(rng).Merge()
        #sheet.Range(rng).Value = "Штамповка"
        ##sheet.Range(rng).Style.Orientation = EXPORTER.xlOrientation.xlUpward
        #sheet.Range(rng).Orientation = EXPORTER.xlOrientation.xlUpward
        ##sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
        #sheet.Range(rng).VerticalAlignment = EXPORTER.xlVerticalAlignment.xlVAlignCenter




        shift_end_row = current_row - 1 # :-)
        class_end_row = current_row - 1 # :-)
        shift_start_col = 2

        for mtc in app_data.MACHINE_TOOL_CLASSES:

            class_start_row = class_end_row + 1
            class_start_col = 1
            if show_12H_shifts:
                class_end_row = class_start_row + 9 * ( app_data.SHIFT_TYPES.count() - 0 ) - 1  # две смены - это ночь, хотя
                                                                                                # я не уверен, правильно ли так делать
            else:
                class_end_row = class_start_row + 9 * (app_data.SHIFT_TYPES.count() - 2) - 1

            class_end_col = class_start_col

            frame_left_upr_corner = sheet.Cells(class_start_row, class_start_col).Address
            frame_right_lwr_corner = sheet.Cells(class_end_row, class_end_col).Address
            frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)
            rng = frame_full_range

            sheet.Range(rng).Merge()
            sheet.Range(rng).Value = mtc.caption.capitalize()
            #sheet.Range(rng).Value = mtc.caption.left(5).toUpper()
            #sheet.Range(rng).Value = mtc.caption.left(1).toUpper() + mtc.caption.mid(1).toLower()
            # sheet.Range(rng).Style.Orientation = EXPORTER.xlOrientation.xlUpward
            sheet.Range(rng).Orientation = EXPORTER.xlOrientation.xlUpward
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
            sheet.Range(rng).VerticalAlignment = EXPORTER.xlVerticalAlignment.xlVAlignCenter
            sheet.Range(rng).Font.Size = 11
            sheet.Range(rng).Font.Bold = True

            for shift in app_data.SHIFT_TYPES:

                #if shift.id == 4 or shift.id == 7:
                #    continue

                if not show_12H_shifts:
                    if shift.id == 4 or shift.id == 5:
                        continue

                #

                shift_start_row = shift_end_row + 1
                shift_start_col = 2
                shift_end_row = shift_start_row + 8
                shift_end_col = shift_start_col

                frame_left_upr_corner = sheet.Cells(shift_start_row, shift_start_col).Address
                frame_right_lwr_corner = sheet.Cells(shift_end_row, shift_end_col).Address
                frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)
                rng = frame_full_range

                sheet.Range(rng).Merge()
                if shift.id == 1:
                    no_w_day = 1
                    shift_b_time = app_data.T1_REPORT_ARR[0].s1_b_time
                    shift_e_time = app_data.T1_REPORT_ARR[0].s2_b_time
                elif shift.id == 2:
                    no_w_day = 2
                    shift_b_time = app_data.T1_REPORT_ARR[0].s2_b_time
                    shift_e_time = app_data.T1_REPORT_ARR[0].s3_b_time
                elif shift.id == 3:
                    no_w_day = 3
                    shift_b_time = app_data.T1_REPORT_ARR[0].s3_b_time
                    shift_e_time = app_data.T1_REPORT_ARR[0].s1_b_time
                elif shift.id == 4:
                    no_w_day = 1
                    shift_b_time = app_data.T1_REPORT_ARR[0].s4_b_time
                    shift_e_time = app_data.T1_REPORT_ARR[0].s5_b_time
                elif shift.id == 5:
                    no_w_day = 2
                    shift_b_time = app_data.T1_REPORT_ARR[0].s5_b_time
                    shift_e_time = app_data.T1_REPORT_ARR[0].s4_b_time
                else:
                    no_w_day = 1234
                    shift_b_time = "???"
                    shift_e_time = "???"



                str_shift_descr =  "Смена " + str(no_w_day)  + "\n" + shift.caption   + "\n" + \
                                   extract_time_hh_mm( shift_b_time ) + " - " + extract_time_hh_mm( shift_e_time )

                sheet.Range(rng).Value = str_shift_descr
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                sheet.Range(rng).VerticalAlignment = EXPORTER.xlVerticalAlignment.xlVAlignCenter



                #

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Итог Остановки"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Поломка"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Материал"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Процесс"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Качество"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Выключен"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Итог Тревоги"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Поломка"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Value = "Материал"
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight

                current_row += 1

        # левый столбец готов
        # вываливаем дельше
        # горизонтальная шапка

        current_row = 1
        current_column = 4

        i = 0
        month = months_list[i]

        for year in years_list:

            while month[2] == year[0] and i < months_number:

                #month_name = EXPORTER.monthCaption(month[0])
                month_name = self.monthCaption(month[0])
                days_in_month = month[1]

                merge_start_column = current_column
                merge_end_column = merge_start_column + days_in_month # +1 is for "Аккум"

                rng1 = sheet.Cells(current_row, merge_start_column).Address
                rng2 = sheet.Cells(current_row, merge_end_column).Address
                rng = rng1 + ":" + rng2
                sheet.Range(rng).Merge()
                sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)

                #sheet.Range(rng).value = month_name.left(1).toUpper() + month_name.mid(1).toLower() + " " + report_year
                sheet.Range(rng).value = month_name.capitalize() + " " + str(month[2])
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                #sheet.Range(rng).Font.Size = 14
                #sheet.Range(rng).Font.Bold = True

                current_column += days_in_month + 1 + 1 # more +1 is for spacer

                i += 1
                if i < months_number:
                    month = months_list[i]


        # горизонтальная шапка готова
        # вываливаем дальше
        # data - day by day

        current_row = 2
        current_column = 4

        full_number_of_records = app_data.T1_REPORT_ARR.count()

        for record in app_data.T1_REPORT_ARR:

            current_row = 2

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"

            #frame_left_upr_corner = rng

            if record.day_id != -1:
                date = record.the_date
                #tmp_str = date.toString("dd.MM")
                sheet.Range(rng).NumberFormat = "@"
                sheet.Range(rng).value = date.toString("dd.MM")
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                sheet.Range(rng).ColumnWidth = 10
            else:
                if record.rec_type == 2:
                    sheet.Range(rng).value = "Накопленный"
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                    sheet.Range(rng).ColumnWidth = 15

            if record.is_dayout:
                sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

            #sheet.Range(rng).ColumnWidth = 10
            #sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            # CLASS 1

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl1_s1_stp_sum, record.s1_data_exists, 1)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl1_s1_stp_sum, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s1_stp_failure, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s1_stp_material, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_stp_process, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_stp_quality, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_stp_offline, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_alr_sum, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_alr_failure, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s1_alr_material, record.s1_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl1_s2_stp_sum, record.s2_data_exists, 1)
            if record.rec_type == 2:
                print_cell(current_row, record, record.cl1_s2_stp_sum, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s2_stp_failure, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s2_stp_material, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_stp_process, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_stp_quality, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_stp_offline, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_alr_sum, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_alr_failure, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s2_alr_material, record.s2_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl1_s3_stp_sum, record.s3_data_exists, 1)
            if record.rec_type == 2:
                print_cell(current_row, record, record.cl1_s3_stp_sum, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s3_stp_failure, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl1_s3_stp_material, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_stp_process, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_stp_quality, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_stp_offline, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_alr_sum, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_alr_failure, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl1_s3_alr_material, record.s3_data_exists)

            if show_12H_shifts:

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl1_s4_stp_sum, record.s4_data_exists, 1)
                if record.rec_type == 2:
                    print_cell(current_row, record, record.cl1_s4_stp_sum, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl1_s4_stp_failure, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl1_s4_stp_material, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_stp_process, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_stp_quality, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_stp_offline, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_alr_sum, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_alr_failure, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s4_alr_material, record.s4_data_exists)

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl1_s5_stp_sum, record.s5_data_exists, 1)
                if record.rec_type == 2:
                    print_cell(current_row, record, record.cl1_s5_stp_sum, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl1_s5_stp_failure, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl1_s5_stp_material, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_stp_process, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_stp_quality, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_stp_offline, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_alr_sum, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_alr_failure, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl1_s5_alr_material, record.s5_data_exists)

            # CLASS 2

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl2_s1_stp_sum, record.s1_data_exists, 2)
            if record.rec_type == 2:
                print_cell(current_row, record, record.cl2_s1_stp_sum, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl2_s1_stp_failure, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl2_s1_stp_material, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_stp_process, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_stp_quality, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_stp_offline, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_alr_sum, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_alr_failure, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s1_alr_material, record.s1_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum(current_row, record, record.cl2_s2_stp_sum, record.s2_data_exists, 2)
            if record.rec_type == 2:
                print_cell(current_row, record, record.cl2_s2_stp_sum, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_stp_failure, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_stp_material, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_stp_process, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_stp_quality, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_stp_offline, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_alr_sum, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_alr_failure, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s2_alr_material, record.s2_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum(current_row, record, record.cl2_s3_stp_sum, record.s3_data_exists, 2)
            if record.rec_type == 2:
                print_cell(current_row, record, record.cl2_s3_stp_sum, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_stp_failure, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_stp_material, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_stp_process, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_stp_quality, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_stp_offline, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_alr_sum, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_alr_failure, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl2_s3_alr_material, record.s3_data_exists)

            if show_12H_shifts:

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum(current_row, record, record.cl2_s4_stp_sum, record.s4_data_exists, 2)
                if record.rec_type == 2:
                    print_cell(current_row, record, record.cl2_s4_stp_sum, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_stp_failure, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_stp_material, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_stp_process, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_stp_quality, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_stp_offline, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_alr_sum, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_alr_failure, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s4_alr_material, record.s4_data_exists)

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum(current_row, record, record.cl2_s5_stp_sum, record.s5_data_exists, 2)
                if record.rec_type == 2:
                    print_cell(current_row, record, record.cl2_s5_stp_sum, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_stp_failure, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_stp_material, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_stp_process, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_stp_quality, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_stp_offline, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_alr_sum, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_alr_failure, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl2_s5_alr_material, record.s5_data_exists)

            # CLASS 3

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl3_s1_stp_sum, record.s1_data_exists, 3)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl3_s1_stp_sum, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s1_stp_failure, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s1_stp_material, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_stp_process, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_stp_quality, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_stp_offline, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_alr_sum, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_alr_failure, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s1_alr_material, record.s1_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl3_s2_stp_sum, record.s2_data_exists, 3)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl3_s2_stp_sum, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s2_stp_failure, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s2_stp_material, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_stp_process, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_stp_quality, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_stp_offline, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_alr_sum, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_alr_failure, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s2_alr_material, record.s2_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl3_s3_stp_sum, record.s3_data_exists, 3)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl3_s3_stp_sum, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s3_stp_failure, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl3_s3_stp_material, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_stp_process, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_stp_quality, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_stp_offline, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_alr_sum, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_alr_failure, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl3_s3_alr_material, record.s3_data_exists)

            if show_12H_shifts:

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl3_s4_stp_sum, record.s4_data_exists, 3)
                if record.rec_type == 2:
                    print_cell( current_row, record, record.cl3_s4_stp_sum, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl3_s4_stp_failure, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl3_s4_stp_material, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_stp_process, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_stp_quality, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_stp_offline, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_alr_sum, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_alr_failure, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s4_alr_material, record.s4_data_exists)

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl3_s5_stp_sum, record.s5_data_exists, 3)
                if record.rec_type == 2:
                    print_cell( current_row, record, record.cl3_s5_stp_sum, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl3_s5_stp_failure, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl3_s5_stp_material, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_stp_process, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_stp_quality, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_stp_offline, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_alr_sum, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_alr_failure, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl3_s5_alr_material, record.s5_data_exists)

            # CLASS 4

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl4_s1_stp_sum, record.s1_data_exists, 4)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl4_s1_stp_sum, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s1_stp_failure, record.s1_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s1_stp_material, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_stp_process, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_stp_quality, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_stp_offline, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_alr_sum, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_alr_failure, record.s1_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s1_alr_material, record.s1_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl4_s2_stp_sum, record.s2_data_exists, 4)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl4_s2_stp_sum, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s2_stp_failure, record.s2_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s2_stp_material, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_stp_process, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_stp_quality, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_stp_offline, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_alr_sum, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_alr_failure, record.s2_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s2_alr_material, record.s2_data_exists)

            current_row += 1
            if record.rec_type == -1 or record.rec_type == 1:
                print_cell_shift_stp_sum( current_row, record, record.cl4_s3_stp_sum, record.s3_data_exists, 4)
            if record.rec_type == 2:
                print_cell( current_row, record, record.cl4_s3_stp_sum, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s3_stp_failure, record.s3_data_exists)
            current_row += 1
            print_cell( current_row, record, record.cl4_s3_stp_material, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_stp_process, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_stp_quality, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_stp_offline, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_alr_sum, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_alr_failure, record.s3_data_exists)
            current_row += 1
            print_cell(current_row, record, record.cl4_s3_alr_material, record.s3_data_exists)

            if show_12H_shifts:

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl4_s4_stp_sum, record.s4_data_exists, 4)
                if record.rec_type == 2:
                    print_cell( current_row, record, record.cl4_s4_stp_sum, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl4_s4_stp_failure, record.s4_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl4_s4_stp_material, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_stp_process, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_stp_quality, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_stp_offline, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_alr_sum, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_alr_failure, record.s4_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s4_alr_material, record.s4_data_exists)

                current_row += 1
                if record.rec_type == -1 or record.rec_type == 1:
                    print_cell_shift_stp_sum( current_row, record, record.cl4_s5_stp_sum, record.s5_data_exists, 4)
                if record.rec_type == 2:
                    print_cell( current_row, record, record.cl4_s5_stp_sum, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl4_s5_stp_failure, record.s5_data_exists)
                current_row += 1
                print_cell( current_row, record, record.cl4_s5_stp_material, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_stp_process, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_stp_quality, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_stp_offline, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_alr_sum, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_alr_failure, record.s5_data_exists)
                current_row += 1
                print_cell(current_row, record, record.cl4_s5_alr_material, record.s5_data_exists)


            #  next date

            if record.day_id != -1: # normal daily data
                current_row = 2
                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                #sheet.Range(rng).ColumnWidth = 5
            else:
                if record.rec_type == 2: # summary column (not day)
                    current_column += 1 # for spacer column
                    rng = sheet.Cells(current_row, current_column).Address
                    sheet.Range(rng).ColumnWidth = 2 # spacer column width
                    current_column += 1
                    rng = sheet.Cells(current_row, current_column).Address
                    frame_left_upr_corner = rng

        # freeze panes
        rng = "D3"
        sheet.Range(rng).Select()
        workbook.Windows(1).FreezePanes = True

        #excelapp.Visible = True
        #excelapp.ScreenUpdating = True
        #excelapp.DisplayAlerts = True
        #excelapp.EnableEvents = True

        today = QDate.currentDate()
        #filename = "auto_report_t1_" + today.toString("dd.MM.yyyy") + "_" + QDateTime.currentDateTime().time().toString("hh.mm.ss") + ".xlsx"
        filename = today.toString("yyyy.MM.dd") + "_" + QDateTime.currentDateTime().time().toString("hh.mm.ss") + "_" + "auto_report_t1" + ".xlsx"
        filepath = app_data.settings.dirForReportFiles
        fullname = filepath + "/" + filename
        workbook.SaveCopyAs(fullname)
        workbook.Close(False)


        #if im_the_only_ExcelApp_object:
        #    excelapp.Quit()
        #if excelapp.Workbooks.Count == 0:
        #    excelapp.Qiut()

        dummy = 0

        #if send_email:
        #    app_data.window_MainWindow.signal_SendEmail.emit(filepath, filename)

        #app_data.window_MainWindow.signal_ExcelFileT1_Done.emit(True, filepath, filename)

        q_res = True

        return q_res, filepath, filename



    ####################################################################################################################

    #@staticmethod
    def exportToExcel_ReportType2(self, app_data):

        ################################################################################################################

        def extract_time(s):
            start_pos_days = s.find("days")
            start_pos_day = s.find("day")
            first_semicolon = s.find(":")
            if start_pos_days == -1 and start_pos_day == -1: # если нету слова "day" или "days"
                return s[0:first_semicolon+6]
            else:
                if start_pos_days != -1:
                    return s[start_pos_days+4:first_semicolon+6]
                if start_pos_day != -1:
                    return s[start_pos_day+3:first_semicolon+6]

        ################################################################################################################

        def extract_hours(s):   # !!! нужна защита от пустой строки
            if s == "":
                return 0
            else:
                first_semicolon = s.find(":")
                return int(s[0:first_semicolon])

        ################################################################################################################

        def print_cell_0(current_row, record, _data):   # ячейки без подсветки

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss,"hh:mm:ss")
                null_time = (ss == "00:00:00")
            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_DATA_DURING_DAYOUT_R, GC.COLOR_DATA_DURING_DAYOUT_G, GC.COLOR_DATA_DURING_DAYOUT_B) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if null_time:
                        pass
                        # output nothing
                    else:
                        sheet.Range(rng).value = ss

            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        def print_cell_1(current_row, record, _data, _class):   # подсветка на один станок (за две смены)

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss,"hh:mm:ss")
                null_time = (ss == "00:00:00")
                hours = extract_hours(ss)

                if record.rec_type == ENM_R02_RECTYPE_ID.DAILY_DATA:
                    if _class == 1:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                    if _class == 2:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                    if _class == 3 or _class == 4:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                else:
                    attention_color = False
                    critical_color = False

            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_DATA_DURING_DAYOUT_R, GC.COLOR_DATA_DURING_DAYOUT_G, GC.COLOR_DATA_DURING_DAYOUT_B) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if null_time:
                        pass
                        # output nothing
                    else:
                        sheet.Range(rng).value = ss
                        if critical_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_CRITICAL_R,GC.COLOR_STP_CRITICAL_G,GC.COLOR_STP_CRITICAL_B)
                        elif attention_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_ALARM_R,GC.COLOR_STP_ALARM_G,GC.COLOR_STP_ALARM_B)
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        def print_cell_2(current_row, record, _data, _class):   # подсветка на сумму по классу (за две смены)

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss,"hh:mm:ss")
                null_time = (ss == "00:00:00")
                hours = extract_hours(ss)

                if record.rec_type == ENM_R02_RECTYPE_ID.DAILY_DATA:
                    if _class == 1:
                        attention_color = (hours>=24)or(tm >= QTime(5, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(10, 0, 0))
                    if _class == 2:
                        attention_color = (hours>=24)or(tm >= QTime(9, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(18, 0, 0))
                    if _class == 3 or _class == 4:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                else:
                    attention_color = False
                    critical_color = False

            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_DATA_DURING_DAYOUT_R, GC.COLOR_DATA_DURING_DAYOUT_G, GC.COLOR_DATA_DURING_DAYOUT_B) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if null_time:
                        pass
                        # output nothing
                    else:
                        sheet.Range(rng).value = ss
                        if critical_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_CRITICAL_R,GC.COLOR_STP_CRITICAL_G,GC.COLOR_STP_CRITICAL_B)
                        elif attention_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_ALARM_R,GC.COLOR_STP_ALARM_G,GC.COLOR_STP_ALARM_B)
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        def print_cell_3(current_row, record, _data, _class):   # подсветка на сумму по станку (за две смены)

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss,"hh:mm:ss")
                null_time = (ss == "00:00:00")
                hours = extract_hours(ss)

                if record.rec_type == ENM_R02_RECTYPE_ID.DAILY_DATA:
                    if _class == 1:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                    if _class == 2:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                    if _class == 3 or _class == 4:
                        attention_color = (hours>=24)or(tm >= QTime(1, 0, 0))
                        critical_color = (hours>=24)or(tm >= QTime(2, 0, 0))
                else:
                    attention_color = False
                    critical_color = False

            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    if null_time:
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        # output nothing
                    else:
                        #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_DATA_DURING_DAYOUT_R, GC.COLOR_DATA_DURING_DAYOUT_G, GC.COLOR_DATA_DURING_DAYOUT_B) # выделение цветом отменили
                        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                        sheet.Range(rng).value = ss
                else:
                    if null_time:
                        pass
                        # output nothing
                    else:
                        sheet.Range(rng).value = ss
                        if critical_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_CRITICAL_R,GC.COLOR_STP_CRITICAL_G,GC.COLOR_STP_CRITICAL_B)
                        elif attention_color:
                            sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_STP_ALARM_R,GC.COLOR_STP_ALARM_G,GC.COLOR_STP_ALARM_B)
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)



        ################################################################################################################

        def print_cell_A(current_row, record, _data): # для [%]

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                else:
                    sheet.Range(rng).value = str(_data) + "%"
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        def print_cell_B(current_row, record, _data): # для reference_time

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #sheet.Range(rng).NumberFormat = "чч:мм:сс"
            sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter

            if record.is_valid:
                ss = extract_time(_data)
                tm = QTime.fromString(ss,"hh:mm:ss")
                null_time = (ss == "00:00:00")
            else:
                null_time = False

            if record.is_valid:
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
                else:
                    sheet.Range(rng).value = ss # no color
            else:
                #sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
                sheet.Range(rng).value = "n/d"
                if record.is_dayout:
                    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

        ################################################################################################################

        class UDT_FRAME_CELL(): # это область которую надо обвести ВЛУ(r1,c1) НПУ(r2,c2)

            def __init__(self,r1,c1,r2,c2):
                self.r1 = r1
                self.c1 = c1
                self.r2 = r2
                self.c2 = c2

        class UDT_FRAME_COLUMN_ARRAY(UDT_ARR): # массив областей которые надо обвести
                                                # в начале знаем номера строк, но не знаем номера столбцов
                                                # поэтому заполняем (инициализируем) сначала так

            def __init__(self):
                super().__init__()

                fr = UDT_FRAME_CELL(3,0,3,0)
                self.append(fr)
                fr = UDT_FRAME_CELL(4,0,12,0)
                self.append(fr)
                fr = UDT_FRAME_CELL(14,0,25,0)
                self.append(fr)
                fr = UDT_FRAME_CELL(27,0,30,0)
                self.append(fr)
                fr = UDT_FRAME_CELL(32, 0, 35, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(38, 0, 46, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(48, 0, 56, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(58, 0, 66, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(68, 0, 76, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(78, 0, 86, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(88, 0, 96, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(98, 0, 106, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(108, 0, 116, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(118, 0, 126, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(128, 0, 136, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(138, 0, 146, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(148, 0, 156, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(158, 0, 166, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(168, 0, 176, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(178, 0, 186, 0)
                self.append(fr)
                fr = UDT_FRAME_CELL(188, 0, 196, 0)
                self.append(fr)

            def setLeftColumn(self,col):

                for fr in self:
                    fr.c1 = col

            def setRightColumn(self,col):

                for fr in self:
                    fr.c2 = col

        ################################################################################################################

        time_data = QTime()

        pythoncom.CoInitialize()    # !!!!!!!!!!!!!!!!

        excelapp = None
        im_the_only_ExcelApp_object = False

        try:
            excelapp1 = win32com.client.GetActiveObject("Excel.Application")
            #excelapp.Quit()
        except:
            im_the_only_ExcelApp_object = True
        finally:
            pass

        excelapp = win32com.client.DispatchEx("Excel.Application")

        if im_the_only_ExcelApp_object:
            excelapp.Visible = False
            excelapp.ScreenUpdating = False
            excelapp.DisplayAlerts = False
            excelapp.EnableEvents = False

        workbook = excelapp.Workbooks.Add(1)
        sheet = workbook.Sheets(1)

        excelapp.ActiveWindow.Zoom = 70
        excelapp.ActiveWindow.DisplayGridlines = False

        #sheet.Range("A10").Interior.Color = GF.rgbToExcelColor(255, 0, 0)
        #sheet.Range("B10").Interior.Color = GF.rgbToExcelColor(0, 255, 0)
        #sheet.Range("C10").Interior.Color = GF.rgbToExcelColor(0, 0, 255)

        # массив рамок - можно рассчитать заранее

        FRAMES = UDT_ARR()  # list of <UDT_FRAME_COLUMN_ARRAY>



        #

        frame_column = UDT_FRAME_COLUMN_ARRAY()
        frame_column.setLeftColumn(2)
        FRAMES.append(frame_column)

        rng = "B3"
        sheet.Range(rng).value = "Автоотчёт по простоям станков_Ежедневный"
        rng = "B3:G3"
        #sheet.Range(rng).value = "Автоотчёт по простоям станков_Ежедневный"
        sheet.Range(rng).Font.Size = 14
        sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
        sheet.Range(rng).Merge()
        ###sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)


        rng = "B4:G4"
        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_HEADER_R, GC.COLOR_HEADER_G, GC.COLOR_HEADER_B)

        sheet.Range("B4").Value = "№"
        sheet.Range("C4").Value = "Номер"
        sheet.Range("D4").Value = "Название"
        sheet.Range("E4").Value = "Класс"
        sheet.Range("F4").Value = "Авария"
        sheet.Range("G4").Value = "Причина"

        sheet.Range("A4").ColumnWidth = 4
        sheet.Range("B4").ColumnWidth = 4
        sheet.Range("C4").ColumnWidth = 4
        sheet.Range("D4").ColumnWidth = 20
        sheet.Range("E4").ColumnWidth = 12
        sheet.Range("F4").ColumnWidth = 16
        sheet.Range("G4").ColumnWidth = 9

        current_row = 5
        current_column = 7

        #rng = sheet.Cells(1,1).GetAddress(RowAbsolute = False, ColumnAbsolute = False)
        rng = sheet.Cells(current_row, current_column).Address
        sheet.Range(rng).Value = "Итог"

        current_row += 1
        rng = sheet.Cells(current_row, current_column).Address
        sheet.Range(rng).Value = "Итог"

        # сколько всего станков, а также классов станков вообще существует на данный момент в системе

        full_mt_classes_number = app_data.MACHINE_TOOL_CLASSES.count()
        full_machine_tools_number = app_data.MACHINE_TOOLS.count()

        # массив: в каком классе сколько станков

        mt_classes_list = list([])

        mt = app_data.MACHINE_TOOLS[0]

        # temp_list - list of al mt_classes with its captions and number machine tools within the class

        # number of machine tools per class
        for mt_class in app_data.MACHINE_TOOL_CLASSES:
            mt_in_class_counter = 0
            for mt in app_data.MACHINE_TOOLS:
                if mt.mt_class == mt_class.caption:
                    mt_in_class_counter += 1
            mt_class_tuple = tuple((mt_class.caption, mt_in_class_counter))
            mt_classes_list.append(mt_class_tuple)

        # сколько всего дней вообще в запросе - это в любом случае пока так:
        # а также - сколько всего месяцев в запросе


        months_list = list([])
        years_list = list([])

        rec_date = app_data.T2_REPORT_ARR[0].the_date
        #last_day_id = app_data.tables.STAT_MT_REPORT[len(app_data.tables.STAT_MT_REPORT)-1].day_id
        last_record_id = app_data.T2_REPORT_ARR[len(app_data.T2_REPORT_ARR)-1].rec_id
        m_days = 0
        y_months = 1

        for record in app_data.T2_REPORT_ARR:
            if record.day_id != -1:
                if record.the_date.month() == rec_date.month(): # тут смотрим, что месяц след.записи равен месяцу предыдущ.записи
                    m_days += 1
                else:
                    month_tuple = tuple((rec_date.month(), m_days, rec_date.year()))
                    months_list.append(month_tuple)
                    m_days = 1

                if record.the_date.year() == rec_date.year():
                    if record.the_date.month() != rec_date.month(): # тут смотрим, что год след.записи равен году предыдущ.записи
                        y_months += 1
                else:
                    year_tuple = tuple((rec_date.year(), y_months))
                    years_list.append(year_tuple)
                    y_months = 1


                rec_date = record.the_date

            if record.rec_id == last_record_id:
                month_tuple = tuple((rec_date.month(), m_days, rec_date.year()))
                months_list.append(month_tuple)
                year_tuple = tuple((rec_date.year(), y_months))
                years_list.append(year_tuple)

        months_number = len(months_list)
        years_number = len(years_list)

        #frames_list = list([])

        #report_year = app_data.tables.STAT_MT_REPORT[0].the_date.year()

        today = QDate.currentDate()

        full_days_number = today.dayOfYear()
        full_month_number = today.month()

        # левая шапка(столбец) - сначала по группам станков

        #sheet.Columns(1).ColumnWidth = 4
        #sheet.Columns(2).ColumnWidth = 4
        #sheet.Columns(4).ColumnWidth = 20
        #sheet.Columns(5).ColumnWidth = 12
        #sheet.Columns(6).ColumnWidth = 16
        #sheet.Columns(7).ColumnWidth = 16

        num_groups = len(mt_classes_list)

        current_row = 5

        k = 0

        for i in range(num_groups):

            current_column = 2

            frame_left_upr_corner = sheet.Cells(current_row, current_column).Address

            group_name = mt_classes_list[i][0]

            for j in range(mt_classes_list[i][1]):

                current_column = 2

                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).value = j + 1

                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).Font.Size = 14
                sheet.Range(rng).Font.Bold = True
                sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].tag

                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].caption

                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].mt_class

                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).value = "Остановка"

                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                sheet.Range(rng).value = "Итог"

                current_row += 1
                k += 1

            k -= 1 # for sake of getting correct class
            current_column = 5

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].mt_class
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Итог"

            current_row += 1
            current_column = 5

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].mt_class
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Итог, %"

            current_row += 1
            current_column = 5

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[k].mt_class
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Рабочее время"
            current_column += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Итог"

            frame_right_lwr_corner = sheet.Cells(current_row, current_column).Address
            frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)

            ###sheet.Range(frame_full_range).BorderAround(LineStyle = EXPORTER.xlLineStyle.xlContinuous)

            # empty string

            current_row += 1
            current_row += 1

            k += 1 # because earlier made k -= 1

        # левая шапка - по индивидуальным станкам

        current_row += 1
        #current_row += 1

        k = 0



        for i in range(full_machine_tools_number):

            current_column = 2

            frame_left_upr_corner = sheet.Cells(current_row, current_column).Address

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = i + 1

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).Font.Size = 14
            sheet.Range(rng).Font.Bold = True
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[i].tag

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[i].caption

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = app_data.MACHINE_TOOLS[i].mt_class

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Поломка"

            current_row += 1
            current_column -= 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Материал"

            current_row += 1
            current_column -= 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Процесс"

            current_row += 1
            current_column -= 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Качество"

            current_row += 1
            current_column -= 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Остановка"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Отключен"

            current_row += 1
            current_column -= 5
            rng1 = sheet.Cells(current_row, current_column).Address
            current_column += 5
            rng2 = sheet.Cells(current_row, current_column).Address
            rng = rng1 + ":" + rng2
            sheet.Range(rng).Merge()

            current_column -= 5

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Cells(current_row, current_column).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
            sheet.Range(rng).value = "Итог остановка"

            current_column = 6
            current_row += 1

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Тревога"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Поломка"

            current_row += 1
            current_column -= 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Тревога"

            current_column += 1
            rng = sheet.Cells(current_row, current_column).Address
            sheet.Range(rng).value = "Материал"

            current_row += 1
            current_column -= 5
            rng1 = sheet.Cells(current_row, current_column).Address
            current_column += 5
            rng2 = sheet.Cells(current_row, current_column).Address
            rng = rng1 + ":" + rng2
            sheet.Range(rng).Merge()

            current_column -= 5

            rng = sheet.Cells(current_row, current_column).Address
            sheet.Cells(current_row, current_column).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
            sheet.Range(rng).value = "Итог тревога"

            current_column = 7

            frame_right_lwr_corner = sheet.Cells(current_row, current_column).Address
            frame_full_range = str(frame_left_upr_corner) + ":" + str(frame_right_lwr_corner)

            ###sheet.Range(frame_full_range).BorderAround(LineStyle = EXPORTER.xlLineStyle.xlContinuous)


            current_row += 1

            #empty row

            current_row += 1

        # левый столбец готов
        # вываливаем дельше
        # горизонтальная шапка

        current_row = 3
        current_column = 8

        i = 0
        month = months_list[i]
        j = 0
        month_2 = months_list[j]    # счётчик для вываливания сводной таблицы по году

        for year in years_list:

            while month[2] == year[0] and i < months_number:

                #month_name = EXPORTER.monthCaption(month[0])
                month_name = self.monthCaption(month[0])
                days_in_month = month[1]

                merge_start_column = current_column
                merge_end_column = merge_start_column + days_in_month # +1 is for "Аккум"

                rng1 = sheet.Cells(current_row, merge_start_column).Address
                rng2 = sheet.Cells(current_row, merge_end_column).Address
                rng = rng1 + ":" + rng2
                sheet.Range(rng).Merge()
                ###sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)

                nnn = FRAMES.count()-1
                FRAMES[nnn].setRightColumn(merge_end_column)

                #sheet.Range(rng).value = month_name.left(1).toUpper() + month_name.mid(1).toLower() + " " + report_year
                sheet.Range(rng).value = month_name.capitalize() + " " + str(month[2])
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                sheet.Range(rng).Font.Size = 14
                sheet.Range(rng).Font.Bold = True

                current_column += days_in_month + 1 + 1 # more +1 is for spacer

                frame_column = UDT_FRAME_COLUMN_ARRAY()
                frame_column.setLeftColumn(current_column)
                FRAMES.append(frame_column)

                i += 1
                if i < months_number:
                    month = months_list[i]

            if month_2[2] == year[0]:

                months_in_year = year[1]

                merge_start_column = current_column
                merge_end_column = merge_start_column + months_in_year

                rng1 = sheet.Cells(current_row, merge_start_column).Address
                rng2 = sheet.Cells(current_row, merge_end_column).Address
                rng = rng1 + ":" + rng2
                sheet.Range(rng).Merge()
                ###sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)

                nnn = FRAMES.count()-1
                FRAMES[nnn].setRightColumn(merge_end_column)

                sheet.Range(rng).value = str(year[0])
                sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlCenter
                sheet.Range(rng).Font.Size = 14
                sheet.Range(rng).Font.Bold = True

                current_column += months_in_year + 1 + 1  # more +1 is for spacer

                frame_column = UDT_FRAME_COLUMN_ARRAY()
                frame_column.setLeftColumn(current_column)
                FRAMES.append(frame_column)

                j += year[1]
                if j < months_number:
                    month_2 = months_list[j]

        merge_start_column = current_column
        merge_end_column = merge_start_column + years_number

        rng1 = sheet.Cells(current_row, merge_start_column).Address
        rng2 = sheet.Cells(current_row, merge_end_column - 1).Address
        rng = rng1 + ":" + rng2
        sheet.Range(rng).Merge()
        ###sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)

        nnn = FRAMES.count() - 1
        FRAMES[nnn].setRightColumn(merge_end_column-1)

        # горизонтальная шапка готова
        # вываливаем дальше



        # data - day by day

        current_row = 4
        current_column = 8
        rng = sheet.Cells(current_row, current_column).Address
        frame_left_upr_corner = rng

        str_start_pos = 0

        for record in app_data.T2_REPORT_ARR:

            current_row = 4

            rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"

            #frame_left_upr_corner = rng

            if record.day_id != -1:

                date = record.the_date

                tmp_str = date.toString("dd.MM")
                # tmp_str.replace(",", ".")
                #sheet.Range(rng).NumberFormat = "dd.mm"
                sheet.Range(rng).NumberFormat = "@"
                sheet.Range(rng).value = tmp_str

            else:
                if record.rec_type == ENM_R02_RECTYPE_ID.SUM_BY_MONTH:
                    sheet.Range(rng).value = "Аккум."
                if record.rec_type == ENM_R02_RECTYPE_ID.MONTHLY_DATA:
                    #sheet.Range(rng).value = EXPORTER.monthCaption(record.month_w_year)
                    sheet.Range(rng).value = self.monthCaption(record.month_w_year)
                if record.rec_type == ENM_R02_RECTYPE_ID.SUM_BY_YEAR:
                    #sheet.Range(rng).value = record.year_id
                    sheet.Range(rng).value = "Итог"
                if record.rec_type == ENM_R02_RECTYPE_ID.YEARLY_DATA:
                    sheet.Range(rng).value = record.year_id

            if record.is_dayout:
                sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)

            sheet.Range(rng).ColumnWidth = 10
            #

            current_row += 1
            print_cell_1(current_row, record, record.day_cl1_mt1_stp_time, 1)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl1_mt2_stp_time, 1)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl1_mt3_stp_time, 1)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl1_mt4_stp_time, 1)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl1_mt5_stp_time, 1)
            current_row += 1
            print_cell_2(current_row, record, record.day_cl1_stp_sum, 1)
            current_row += 1
            print_cell_A(current_row, record, record.day_cl1_stp_sum_prc)
            current_row += 1
            print_cell_B(current_row, record, record.day_cl1_reference_time)

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl1_mt3_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl1_mt4_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"
            #
            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"

            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl1_mt5_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl1_stp_sum)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            ##sheet.Range(rng).Style = "Percent"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = str(record.day_cl1_stp_sum_prc) + "%"
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl1_reference_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            # add border around - НАПОТОМ!
            """
            if record.day_id == -1 and record.rec_type == ENM_R01_RECTYPE_ID.SUM_BY_MONTH:
                frame_right_lwr_corner = rng
                frame_full_range = frame_left_upr_corner + ":" + frame_right_lwr_corner
                #frames_list.append(frame_full_range)
                sheet.Range(frame_full_range).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)
            """

            # next group

            current_row += 1    # spacer row

            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt6_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt7_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt8_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt9_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt10_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt11_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt12_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt13_stp_time, 2)
            current_row += 1
            print_cell_1(current_row, record, record.day_cl2_mt14_stp_time, 2)
            current_row += 1
            print_cell_2(current_row, record, record.day_cl2_stp_sum, 2)
            current_row += 1
            print_cell_A(current_row, record, record.day_cl2_stp_sum_prc)
            current_row += 1
            print_cell_B(current_row, record, record.day_cl2_reference_time)

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt6_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"
            #
            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"

            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt7_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt8_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt9_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt10_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt11_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt12_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt13_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_mt14_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_stp_sum)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            ##sheet.Range(rng).Style = "Percent"
            #
            ##if record.rec_type != -1:
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = str(record.day_cl2_stp_sum_prc) + "%"
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl2_reference_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"


            # next group

            current_row += 1    # spacer row

            current_row += 1
            print_cell_1(current_row, record, record.day_cl3_mt15_stp_time, 3)
            current_row += 1
            print_cell_2(current_row, record, record.day_cl3_stp_sum, 3)
            current_row += 1
            print_cell_A(current_row, record, record.day_cl3_stp_sum_prc)
            current_row += 1
            print_cell_B(current_row, record, record.day_cl3_reference_time)

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl3_mt15_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl3_stp_sum)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            ##sheet.Range(rng).Style = "Percent"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = str(record.day_cl3_stp_sum_prc) + "%"
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl3_reference_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            # next group

            current_row += 1    # spacer row

            current_row += 1
            print_cell_1(current_row, record, record.day_cl4_mt16_stp_time, 4)
            current_row += 1
            print_cell_2(current_row, record, record.day_cl4_stp_sum, 4)
            current_row += 1
            print_cell_A(current_row, record, record.day_cl4_stp_sum_prc)
            current_row += 1
            print_cell_B(current_row, record, record.day_cl4_reference_time)

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl4_mt16_stp_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl4_stp_sum)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            ## sheet.Range(rng).Style = "Percent"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = str(record.day_cl3_stp_sum_prc) + "%"
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_cl3_reference_time)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            # add border around - НАПОТОМ!

            # next machine tool

            current_row += 1    # spacer row
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt1_stp_sum, 1)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt1_alr_sum)

            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt2_stp_sum, 1)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt2_alr_sum)

            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt3_stp_sum, 1)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt3_alr_sum)

            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt4_stp_sum, 1)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt4_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt5_stp_sum, 1)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt5_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt6_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt6_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt7_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt7_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt8_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt8_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt9_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt9_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt10_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt10_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt11_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt11_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt12_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt12_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt13_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt13_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt14_stp_sum, 2)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt14_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt15_stp_sum, 3)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt15_alr_sum)
            
            current_row += 1    # spacer row

            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_stp_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_stp_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_stp_process)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_stp_quality)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_stp_offline)
            current_row += 1
            print_cell_3(current_row, record, record.day_mt16_stp_sum, 4)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_alr_failure)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_alr_material)
            current_row += 1
            print_cell_0(current_row, record, record.day_mt16_alr_sum)

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_failure)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_material)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_process)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_quality)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_offline)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"

            #current_row += 1
            #rng = sheet.Cells(current_row, current_column).Address
            #sheet.Range(rng).NumberFormat = "@"
            #
            #if record.is_valid:
            #    if record.is_dayout == 1:
            #        sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_WEEKEND_R, GC.COLOR_WEEKEND_G, GC.COLOR_WEEKEND_B)
            #    else:
            #        sheet.Range(rng).value = extract_time(record.day_mt1_stp_sum)
            #else:
            #    sheet.Range(rng).Interior.Color = GF.rgbToExcelColor(GC.COLOR_NODATA_R, GC.COLOR_NODATA_G, GC.COLOR_NODATA_B)
            #    sheet.Range(rng).value = "n/d"
























            #  next date

            if record.day_id != -1: # normal daily data
                current_row = 5
                current_column += 1
                rng = sheet.Cells(current_row, current_column).Address
                #sheet.Range(rng).ColumnWidth = 5
            else:
                if record.rec_type == ENM_R02_RECTYPE_ID.SUM_BY_MONTH: # summary column (not day)
                    current_column += 1 # for spacer column
                    rng = sheet.Cells(current_row, current_column).Address
                    sheet.Range(rng).ColumnWidth = 2 # spacer column width
                    current_column += 1
                    rng = sheet.Cells(current_row, current_column).Address
                    frame_left_upr_corner = rng
                if record.rec_type == ENM_R02_RECTYPE_ID.MONTHLY_DATA:
                    current_column += 1
                    rng = sheet.Cells(current_row, current_column).Address
                if record.rec_type == ENM_R02_RECTYPE_ID.SUM_BY_YEAR:
                    current_column += 1 # for spacer column
                    rng = sheet.Cells(current_row, current_column).Address
                    sheet.Range(rng).ColumnWidth = 2  # spacer column width
                    current_column += 1
                if record.rec_type == ENM_R02_RECTYPE_ID.YEARLY_DATA:
                    current_column += 1
                    rng = sheet.Cells(current_row, current_column).Address




        # sheet.Columns.AutoFit()

        #

        for fr_col in FRAMES:
            for fr in fr_col:
                frame_left_upr_corner = sheet.Cells(fr.r1,fr.c1).Address
                frame_right_lwr_corner = sheet.Cells(fr.r2, fr.c2).Address
                rng = frame_left_upr_corner + ":" + frame_right_lwr_corner
                sheet.Range(rng).BorderAround(LineStyle=EXPORTER.xlLineStyle.xlContinuous)


        #

        #excelapp.ActiveWindow.SplitColumn = 7
        #excelapp.ActiveWindow.SplitRow = 4
        #excelapp.ActiveWindow.FreezePanes = True

        # freeze panes
        rng = "H5"
        sheet.Range(rng).Select()
        workbook.Windows(1).FreezePanes = True

        #excelapp.Visible = True
        #excelapp.ScreenUpdating = True
        #excelapp.DisplayAlerts = True
        #excelapp.EnableEvents = True

        today = QDate.currentDate()
        #filename = "auto_report_t2_" + today.toString("dd.MM.yyyy") + "_" + QDateTime.currentDateTime().time().toString("hh.mm.ss") + ".xlsx"
        filename = today.toString("yyyy.MM.dd") + "_" + QDateTime.currentDateTime().time().toString("hh.mm.ss") + "_" + "auto_report_t2" + ".xlsx"
        filepath = app_data.settings.dirForReportFiles
        fullname = filepath + "/" + filename
        workbook.SaveCopyAs(fullname)
        workbook.Close(False)

        #if excelapp.Workbooks.Count == 0:
        #    excelapp.Quit()
        #if im_the_only_ExcelApp_object:
        #    excelapp.Quit()

        dummy = 0

        #if send_email:
        #    app_data.window_MainWindow.signal_SendEmail.emit(filepath, filename)

        #app_data.window_MainWindow.signal_ExcelFileT2_Done.emit(True, filepath, filename)

        q_res = True

        return q_res, filepath, filename

    ####################################################################################################################

    def exportToExcel_DetailedRep(self, app_data):

        ################################################################################################################

        def extract_time(s):
            start_pos_days = s.find("days")
            start_pos_day = s.find("day")
            first_semicolon = s.find(":")
            if start_pos_days == -1 and start_pos_day == -1: # если нету слова "day" или "days"
                return s[0:first_semicolon+6]
            else:
                if start_pos_days != -1:
                    return s[start_pos_days+4:first_semicolon+6]
                if start_pos_day != -1:
                    return s[start_pos_day+3:first_semicolon+6]

        ################################################################################################################

        def extract_hh_mm_ss(s):   # !!! нужна защита от пустой строки
            if s == "":
                return 0
            else:
                dot_position = s.find(".")
                if dot_position != -1:
                    s = s[0:dot_position]
                q_list = s.split(":")
                return int(q_list[0]), int(q_list[1]), int(q_list[2])

        ################################################################################################################

        def HMS_2_H(h,m,s):

            return ( h + m/60.0 + s/3600.0 )

        ################################################################################################################


        def print_row(current_row, record, rec_num):

            #current_column = 1

            for current_column in range(1,14):

                rng = sheet.Cells(current_row, current_column).Address
                #sheet.Range(rng).NumberFormat = "@"



                if current_column == 1:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    #sheet.Range(rng).NumberFormat = "@"
                    sheet.Range(rng).value = rec_num #record.rec_id
                elif current_column == 2:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    sheet.Range(rng).value = record.mt_class_caption
                elif current_column == 3:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    #sheet.Range(rng).NumberFormat = "@"
                    sheet.Range(rng).value = record.mt_tag
                elif current_column == 4:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    #sheet.Range(rng).NumberFormat = "@"
                    sheet.Range(rng).value = record.mt_caption
                elif current_column == 5:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    #sheet.Range(rng).NumberFormat = "@"
                    sheet.Range(rng).value = record.state_cap1
                elif current_column == 6:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlLeft
                    sheet.Range(rng).value = record.state_cap2
                elif current_column == 7:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    s_d = record.b_dt.toString("dd.MM.yyyy")
                    sheet.Range(rng).value = s_d
                elif current_column == 8:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    s_dt = record.b_dt.toString("dd.MM.yyyy hh:mm:ss")
                    sheet.Range(rng).value = s_dt
                elif current_column == 9:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    s_dt = record.e_dt.toString("dd.MM.yyyy hh:mm:ss")
                    sheet.Range(rng).value = s_dt
                elif current_column == 10:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    #sheet.Range(rng).NumberFormat = "чч:мм:сс"
                    s_int = extract_time(record.full_time)
                    sheet.Range(rng).value = s_int
                elif current_column == 11:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    #sheet.Range(rng).NumberFormat = "чч:мм:сс"
                    s_int = extract_time(record.act_time)
                    sheet.Range(rng).value = s_int
                elif current_column == 12:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    sheet.Range(rng).NumberFormat = "0,00"
                    sheet.Range(rng).value = record.full_time_hrs
                elif current_column == 13:
                    sheet.Range(rng).HorizontalAlignment = EXPORTER.xlHorizontalAlignment.xlRight
                    sheet.Range(rng).NumberFormat = "0,00"
                    sheet.Range(rng).value = record.act_time_hrs




        ################################################################################################################

        # попробуем пока обработать дополнительно массив здесь
        # это всё равно вызывается в выделенном потоке
        # и в принципе можно не создавать ещё промежуточный поток для дополнительной обработки

        for record in app_data.DETAILED_REP_ARR:

            # тут время простоя передаётся в виде str, что конечно не совсем удобно
            # однако, эта строка при вываливании в Excel автоматичсеки превращается во время, что хорошо
            # однако, если время большое (типа 300 часов) то Excel его уже почему-то не понимает как время ((

            f_hh, f_mm, f_ss = extract_hh_mm_ss(record.full_time)
            a_hh, a_mm, a_ss = extract_hh_mm_ss(record.act_time)

            record.full_time_hrs = HMS_2_H(f_hh, f_mm, f_ss)
            record.act_time_hrs = HMS_2_H(a_hh, a_mm, a_ss)

        ################################################################################################################

        pythoncom.CoInitialize()    # !!!!!!!!!!!!!!!!

        excelapp = None
        im_the_only_ExcelApp_object = False

        try:
            excelapp1 = win32com.client.GetActiveObject("Excel.Application")
            #excelapp.Quit()
        except:
            im_the_only_ExcelApp_object = True
        finally:
            pass

        excelapp = win32com.client.DispatchEx("Excel.Application")

        if im_the_only_ExcelApp_object:
            excelapp.Visible = False
            excelapp.ScreenUpdating = False
            excelapp.DisplayAlerts = False
            excelapp.EnableEvents = False

        workbook = excelapp.Workbooks.Add(1)
        sheet = workbook.Sheets(1)

        excelapp.ActiveWindow.Zoom = 100
        excelapp.ActiveWindow.DisplayGridlines = False

        sheet.Range("A1").value = "№п/п"
        sheet.Range("B1").value = "Класс"
        sheet.Range("C1").value = "Обозначение"
        sheet.Range("D1").value = "Наименование"
        sheet.Range("E1").value = "Причина"
        sheet.Range("F1").value = "Причина"
        sheet.Range("G1").value = "Дата (начало)"
        sheet.Range("H1").value = "Остановка начало"
        sheet.Range("I1").value = "Остановка конец"
        sheet.Range("J1").value = "Полное время"
        sheet.Range("K1").value = "Время простоя"
        sheet.Range("L1").value = "Полн.вр. [час]"
        sheet.Range("M1").value = "Вр.простоя [час]"

        sheet.Range("A1:M1").Font.Bold = True
        sheet.Range("A1:M1").Interior.Color = GF.rgbToExcelColor(180,200,230)

        sheet.Range("A1").ColumnWidth = 6
        sheet.Range("B1").ColumnWidth = 20
        sheet.Range("C1").ColumnWidth = 20
        sheet.Range("D1").ColumnWidth = 30
        sheet.Range("E1").ColumnWidth = 15
        sheet.Range("F1").ColumnWidth = 15
        sheet.Range("G1").ColumnWidth = 15
        sheet.Range("H1").ColumnWidth = 20
        sheet.Range("I1").ColumnWidth = 20
        sheet.Range("J1").ColumnWidth = 15
        sheet.Range("K1").ColumnWidth = 15
        sheet.Range("L1").ColumnWidth = 15
        sheet.Range("M1").ColumnWidth = 15

        current_row = 1
        #current_column = 1
        rec_num = 1

        for record in app_data.DETAILED_REP_ARR:

            current_row += 1
            print_row(current_row, record, rec_num)
            rec_num += 1













        today = QDate.currentDate()
        filename = today.toString("yyyy.MM.dd") + "_" + QDateTime.currentDateTime().time().toString("hh.mm.ss") + "_" + "detailed_report" + ".xlsx"
        filepath = app_data.settings.path_ReportFolder
        fullname = filepath + "/" + filename
        workbook.SaveCopyAs(fullname)
        workbook.Close(False)


        q_res = True

        return q_res, filepath, filename

    ####################################################################################################################



