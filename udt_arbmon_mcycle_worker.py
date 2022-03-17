########################################################################################################################

from datetime import *

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDate, QTime, QDateTime


########################################################################################################################

from enums import *
from udt_interval import UDT_INTERVAL

########################################################################################################################

__DEBUG_FIXED_PIECHARTS__   = False

########################################################################################################################
# описание класса:
# -
#
########################################################################################################################

class UDT_ARBMON_MCYCLE_WORKER(QObject):

    signal_ScreenChanged = pyqtSignal(int)

    ####################################################################################################################

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnMainCycle(self):

        print("--начало arbmon_mcycle--" + QTime.currentTime().toString("hh:mm:ss.zzz"))

        # я полагаю, что это можно вызывать асинхронно
        # т.к. влияет только на отображение на экране

        self.appData.CD.shift_number = self.appData.CD.shift % 10 # где это используется??? - на экране Workshop

        #

        for mti in self.appData.CD.MT_INFO:
            mti.update()

        #

        self.appData.FOOTPRINT_BLINKER.update()

        # data for PIE CHARTS

        piechart = self.appData.PIECHART_1_DATA

        piechart.includeZeroWedges = False

        if not __DEBUG_FIXED_PIECHARTS__:
            piechart.WEDGES[0].time_TIME = self.appData.CD.MT_STAT[1][0].stp_sum
            piechart.WEDGES[1].time_TIME = self.appData.CD.MT_STAT[1][1].stp_sum
            #piechart.WEDGES[1].time_TIME = UDT_INTERVAL.s_fromHMS(200, 30, 0)
            piechart.WEDGES[2].time_TIME = self.appData.CD.MT_STAT[1][2].stp_sum
            piechart.WEDGES[3].time_TIME = self.appData.CD.MT_STAT[1][3].stp_sum
            piechart.WEDGES[4].time_TIME = self.appData.CD.MT_STAT[1][4].stp_sum
        else:
            piechart.WEDGES[0].time_TIME = UDT_INTERVAL.s_fromHMS(1,0,0)
            piechart.WEDGES[1].time_TIME = UDT_INTERVAL.s_fromHMS(0,30,0)
            piechart.WEDGES[2].time_TIME = UDT_INTERVAL.s_fromHMS(0,0,0)
            piechart.WEDGES[3].time_TIME = UDT_INTERVAL.s_fromHMS(0,0,0)
            piechart.WEDGES[4].time_TIME = UDT_INTERVAL.s_fromHMS(0,0,0)


        piechart.update()

        piechart = self.appData.PIECHART_2_DATA

        piechart.includeZeroWedges = False

        piechart.WEDGES[0].time_TIME = self.appData.CD.MT_STAT[1][5].stp_sum
        piechart.WEDGES[1].time_TIME = self.appData.CD.MT_STAT[1][6].stp_sum
        piechart.WEDGES[2].time_TIME = self.appData.CD.MT_STAT[1][7].stp_sum
        piechart.WEDGES[3].time_TIME = self.appData.CD.MT_STAT[1][8].stp_sum
        piechart.WEDGES[4].time_TIME = self.appData.CD.MT_STAT[1][9].stp_sum
        piechart.WEDGES[5].time_TIME = self.appData.CD.MT_STAT[1][10].stp_sum
        piechart.WEDGES[6].time_TIME = self.appData.CD.MT_STAT[1][11].stp_sum
        piechart.WEDGES[7].time_TIME = self.appData.CD.MT_STAT[1][12].stp_sum
        piechart.WEDGES[8].time_TIME = self.appData.CD.MT_STAT[1][13].stp_sum

        piechart.update()



        #self.appData.pane_Diagrams.widget_LD.axes.clear()
        #self.appData.pane_Diagrams.widget_RD.axes.clear()

        #
        self.appData.DB_CONN_SUPERVISOR.read_time = self.appData.CD.time

        self.appData.DB_CONN_SUPERVISOR.update()

        field_ok = self.appData.DB_CONN_SUPERVISOR.DB_DATA_STATUS

        #

        self.appData.window_MainWindow.signal_UpdateUI.emit() # WINDOW_ARBMON_MAIN_WINDOW::msgprc_OnUpdateWindow
                                                                # WIDGET_ARBMON_PANE_WORKSHOP::msgprc_OnUpdateWindow

        #print("--конец arbmon_mcycle--" + QTime.currentTime().toString("hh:mm:ss.zzz"))

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnChangeAlarmWidget(self):

        win = self.appData.window_MainWindow
        cd = self.appData.CD

        max_num = len(self.appData.window_MainWindow.list_AlarmPaneWidgets)

        k = 0
        m = 0

        #while k < max_num-6:
        #
        #    win.list_AlarmPaneWidgets[k + 1].onCondition = cd.MT_INFO[m].alr_failure
        #    win.list_AlarmPaneWidgets[k + 2].onCondition = cd.MT_INFO[m].alr_material
        #    win.list_AlarmPaneWidgets[k + 3].onCondition = cd.MT_INFO[m].stp_failure
        #    win.list_AlarmPaneWidgets[k + 4].onCondition = cd.MT_INFO[m].stp_material
        #    win.list_AlarmPaneWidgets[k + 5].onCondition = cd.MT_INFO[m].stp_process
        #    win.list_AlarmPaneWidgets[k + 6].onCondition = cd.MT_INFO[m].stp_quality
        #
        #    k += 6
        #    m += 1


        #

        k = 1 ; m = 0

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1 
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_failure ; k += 1 
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].alr_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_failure ; k += 1 
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_material ; k += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1 
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_quality ; k += 1 ; m += 1

        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1 ; m += 1
        win.list_AlarmPaneWidgets[k].onCondition = cd.MT_INFO[m].stp_process ; k += 1 ; m += 1

        #for wdg in self.appData.window_MainWindow.list_AlarmPaneWidgets:

        k = self.appData.window_MainWindow.n_ALARM_PANE_ACTIVE_WIDGET
        # 0 - это widget "бегущая строка"
        # которую мы не показываем, если есть к-л alarm

        found = False
        k += 1
        if k >= max_num: k = 0
        m = 0

        while not found and m < max_num:

            wdg = win.list_AlarmPaneWidgets[k]
            if k > 0 and wdg.onCondition:   # widget [0] has no "onCondition"
                found = True
                break

            k += 1
            if k >= max_num: k = 0

            m += 1

        if found:
            win.n_ALARM_PANE_ACTIVE_WIDGET = k
        else:
            win.n_ALARM_PANE_ACTIVE_WIDGET = 0



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnRunningCaptionUpdate(self):

        wdg = self.appData.window_MainWindow.list_AlarmPaneWidgets[0]

        str1 = wdg.actualString[:1]
        str2 = wdg.actualString[1:]

        wdg.actualString = str2 + str1

        #wdg.update()

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnChangeScreen(self):

        if self.appData.currentScreen == 1:
            self.appData.currentScreen = 2
        elif self.appData.currentScreen == 2:
            self.appData.currentScreen = 1

        self.signal_ScreenChanged.emit(self.appData.currentScreen)

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionSuccess(self):

        self.appData.dbConnected = True
        print("связь с БД установлена")
        self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True

    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDBConnectionFailure(self):

        self.appData.dbConnected = False
        print("невозможно установить связь с БД")
        self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False

    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnInitialDataReadDone(self,success):

        if success:

            self.appData.window_MainWindow.signal_RestartTimers.emit()

            piechart = self.appData.PIECHART_1_DATA
            piechart.WEDGES[0].mt_pointer = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M1_SALVAGNINI_GREY - 1]
            piechart.WEDGES[1].mt_pointer = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M2_SALVAGNINI_GREEN - 1]
            piechart.WEDGES[2].mt_pointer = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_600 - 1]
            piechart.WEDGES[3].mt_pointer = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M3_TRUMPF_3000 - 1]
            piechart.WEDGES[4].mt_pointer = self.appData.MACHINE_TOOLS[ENM_MACHINE_TOOLS.STAMP_M4_TRUMPF_6000 - 1]

            piechart = self.appData.PIECHART_2_DATA
            piechart.WEDGES[0].mt_pointer = self.appData.MACHINE_TOOLS[5]
            piechart.WEDGES[1].mt_pointer = self.appData.MACHINE_TOOLS[6]
            piechart.WEDGES[2].mt_pointer = self.appData.MACHINE_TOOLS[7]
            piechart.WEDGES[3].mt_pointer = self.appData.MACHINE_TOOLS[8]
            piechart.WEDGES[4].mt_pointer = self.appData.MACHINE_TOOLS[9]
            piechart.WEDGES[5].mt_pointer = self.appData.MACHINE_TOOLS[10]
            piechart.WEDGES[6].mt_pointer = self.appData.MACHINE_TOOLS[11]
            piechart.WEDGES[7].mt_pointer = self.appData.MACHINE_TOOLS[12]
            piechart.WEDGES[8].mt_pointer = self.appData.MACHINE_TOOLS[13]

            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True

        else:

            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False



    ####################################################################################################################

    @pyqtSlot(bool)
    def msgprc_OnRTDataReadDone(self,success):

        if success:
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = True
        else:
            self.appData.DB_CONN_SUPERVISOR.dbReadConnOK = False

    ####################################################################################################################


