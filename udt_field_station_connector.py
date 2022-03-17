########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QDateTime

from PyQt5.QtCore import QTimer

from opcua import Client
from opcua.ua.uaerrors import UaStatusCodeError

import socket

########################################################################################################################

from enums import *
from global_functions import *


########################################################################################################################
# описание класса:
# - производит опрос станций сбора данных
# - ПРОБЛЕМА: если какая-то станция отвалилась в процессе опроса,
# - то весь опрос подвисает
# - что с этим делать? спасёт ли, если на опрос каждой станции запустить
# - отдельный поток? я будмаю что нет, потому что например если застревает
# - на уровне сетевой карты, а сетевая карта - она одна, то что сделаешь?
#
########################################################################################################################

class UDT_FIELD_STATION_CONNECTOR(QObject):

    signal_connectResult = pyqtSignal(int, int, QDateTime)
    #signal_readDataResult = pyqtSignal(int, int, QDateTime)    # (node_id, result_id)
    signal_disconnectResult = pyqtSignal(int, QDateTime)

    signal_FieldDataReady = pyqtSignal(int)
    signal_TrackFieldAccess = pyqtSignal(str)

    ioStation01Connected = False

    ####################################################################################################################

    def __init__(self, app_data):

        self.appData = app_data

        super().__init__()

        #self.moveToThread(appData.thread_FieldAccess)

        #self.timer_RequestData = QTimer()
        #self.timer_RequestData.setInterval(2000)
        #self.timer_RequestData.start()
        #self.timer_RequestData.timeout.connect(self.ttt)
        #self.timer_ConnectAttempt = QTimer()



        #self.Client01 = Client("opc.tcp://192.168.1.4:4840")

        for mt in self.appData.stations:

            opc_ua_socket = "opc.tcp://" + mt.PAR.string_Socket
            mt.DAT.opc_ua_client = Client(opc_ua_socket)

    ####################################################################################################################

    def connectSignals(self):

        self.signal_TrackFieldAccess.connect(self.appData.widget_TabPaneFieldAccessTracker.msgprc_OnTrackFieldAccess)
        self.signal_FieldDataReady.connect(self.appData.worker_MCycle.msgprc_OnFieldDataReady)

    ####################################################################################################################

    def TRACK(self,track_msg):

        self.appData.model_FieldAccessTrackerBack.append(track_msg)
        if not self.appData.widget_TabPaneFieldAccessTracker.paused:
            self.appData.model_FieldAccessTrackerView.append(track_msg)
        self.appData.window_MainWindow.signal_UpdateFieldAccessTracker.emit()  # --> window_MainWindow.msgprc_OnUpdateFieldAccessTracker

    ####################################################################################################################

    """
    # @pyqtSlot(str)
    def PrintA(self, str_arg): # удалить

        print("A - " + str_arg)

    # @pyqtSlot(str)
    def PrintB(self, str_arg): # удалить

        print("B - " + str_arg)

    # @pyqtSlot(str)
    def ioStation01Connect(self): # удалить

        print("попытка соединения")

        host = "192.168.1.4"
        port = 4840

        socket_error = 0

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Failed to create socket")

        try:
            s.connect((host,port))
            #info = s.recv(4096)
            #print(info)
        except socket.error:
            socket_error = 1
            print("Failed to connect to IP")


        if not socket_error:
            try:
                self.Client01.connect()
            except:
                print("какая-то ошибка")

        if not socket_error:

            self.ioStation01Connected = True

            self.timer_ConnectAttempt.stop()

            self.timer_RequestData = QTimer()
            self.timer_RequestData.setInterval(1000)
            self.timer_RequestData.timeout.connect(self.ioStation01GetData)
            self.timer_RequestData.start()
            print("циклический опрос запущен")
            

        else:   # schedule another connection attempt

            self.timer_ConnectAttempt = QTimer()
            self.timer_ConnectAttempt.setInterval(2000)
            self.timer_ConnectAttempt.timeout.connect(self.ioStation01Connect)
            self.timer_ConnectAttempt.start()
            print("циклическая попытка соединения")

        if not socket_error:
            connect_result = 1
        else:
            connect_result = 2

        self.signal_connectResult.emit(1, connect_result, QDateTime.currentDateTime())

    # @pyqtSlot(str)
    def ioStation01GetData(self): # удалить

        self.d1_node = None
        self.d1_data = None

        if self.ioStation01Connected:

            try:
                self.d1_node = self.Client01.get_node("ns=3;s=\"SIGNALS_2_SCADA\".\"ARR\"")
            except:
                self.ioStation01Connected = False

            #try:
                #self.d1_node = self.Client01.get_node("ns=0;s=\"SERVER\".\"ServerStatus\"")
                #self.d1_node = self.Client01.get_node("ns=0;i=2256")
            #finally:
                #print("an exception 1")
            try:
                self.d1_data = self.d1_node.get_value()   # это вроде целый огромный массив читаем
            except UaStatusCodeError:
                print("UaStatusCodeError")
                self.ioStation01Connected = False
            except:
                self.ioStation01Connected = False

        if not self.ioStation01Connected:

            self.timer_RequestData.stop()

            self.timer_ConnectAttempt = QTimer()
            self.timer_ConnectAttempt.setInterval(2000)
            self.timer_ConnectAttempt.timeout.connect(self.ioStation01Connect)
            self.timer_ConnectAttempt.start()
            print("циклическая попытка соединения")



        self.signal_readDataResult.emit(1, 1, QDateTime.currentDateTime())

        self.appData.stations[ENM_MACHINE_TOOLS.MACHINETOOL_STAMP_M1_SALVAGNINI_GREY - 1].rawSourceArray = self.d1_data
        self.signal_DataReady.emit()

        print("get data")


    # @pyqtSlot(str)
    def ioStation01Disconnect(self): # удалить

        self.Client01.disconnect()
        self.timer_RequestData.stop()

        self.signal_disconnectResult.emit(1, QDateTime.currentDateTime())

    def ttt(self): # удалить

        print("таймер тест")
    """
    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnGetFieldData(self):

        d1_data = None

        for mt in self.appData.stations:

            if mt.PAR.persists:
                #if mt.DAT.alive and( mt.DAT.ouc_node is not None ):
                if mt.DAT.alive and mt.DAT.ouc_connected and( mt.DAT.ouc_node is not None ):

                    #print("get data from mt.id=" + str(mt.PAR.id) + " @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))

                    problem = False

                    #if not mt.DAT.ouc_connected:
                    #    mt.DAT.opc_ua_client.connect()
                    #    mt.DAT.ouc_connected = True
                    #try:
                    #    self.d1_node = mt.DAT.opc_ua_client.get_node("ns=3;s=\"SIGNALS_2_SCADA\".\"ARR\"")
                    #except:
                    #    do_nothing = 1
                    try:
                        #print("-- get value --")
                        d1_data = mt.DAT.ouc_node.get_value()
                        fake = 0
                    except:
                        problem = True
                        self.msgprc_OnStationLost(mt.PAR.id)   # ?? надо ли это - проверить ещё раз
                    #mt.DAT.opc_ua_client.disconnect()
                    if not problem:
                        mt.DAT.rawSourceArray = d1_data
                        self.signal_FieldDataReady.emit(mt.PAR.id) # worker_MCycle.msgprc_OnFieldDataReady

                    #print("completed @ " + QDateTime.currentDateTime().toString(
                    #    "dd.MM.yyyy hh:mm:ss.zzz"))

                    #tr_msg = "станция " + str(mt.PAR.id) + " данные получены @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
                    #self.signal_TrackFieldAccess.emit(tr_msg)
                    aux_str =  " " + GF.bool_to_Y_N(mt.DAT.alive) + " " + GF.bool_to_Y_N(mt.DAT.ouc_connected)
                    self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - станция " + str(mt.PAR.id) + ": данные получены (+)" + aux_str)

                else:

                    #tr_msg = "станция " + str(mt.PAR.id) + " недоступна @" + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz")
                    #self.signal_TrackFieldAccess.emit(tr_msg)
                    aux_str = " " + GF.bool_to_Y_N(mt.DAT.alive) + " " + GF.bool_to_Y_N(mt.DAT.ouc_connected)
                    self.TRACK(QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz") + " - станция " + str(mt.PAR.id) + ": недоступна (-)" + aux_str)

    ####################################################################################################################

    @pyqtSlot(int)
    def msgprc_OnStationFound(self, mt_id):

        mt = self.appData.stations[mt_id - 1]
        result = 1
        #mt.DAT.alive = True
        #mt.DAT.ouc_connected = False
        #mt.DAT.ouc_node = None

        if not mt.DAT.ouc_connected:

            self.appData.window_MainWindow.signal_IsCheckingNode.emit(mt_id)

            try:
                mt.DAT.opc_ua_client.connect() # тут бы надо таймаут
            except:
                result = 2

            if result == 1:
                mt.DAT.ouc_connected = True
            else:
                mt.DAT.ouc_connected = False

        if mt.DAT.ouc_connected:

            try:
               #mt.DAT.ouc_node = mt.DAT.opc_ua_client.get_node("ns=3;s=\"SIGNALS_2_SCADA\".\"ARR\"")
               #mt.DAT.ouc_node = mt.DAT.opc_ua_client.get_node("ns=4;s=\"SIGNALS_2_SCADA\".\"ARR\"")

               mt.DAT.ouc_node = mt.DAT.opc_ua_client.get_node("ns=4;i=2") # тут бы надо таймаут
            except:
               result = 2

        if result == 2 or mt.DAT.ouc_node is None:

            if mt.DAT.ouc_connected:
                try:
                    mt.DAT.opc_ua_client.disconnect()
                except:
                    do_nothing = 1

            if mt.DAT.alive:
                try:
                    mt.DAT.sock.close()
                except:
                    do_nothing = 1

         #   mt.DAT.opc_ua_client.disconnect()
            mt.DAT.ouc_connected = False
            mt.DAT.ouc_node = None
         #   mt.DAT.sock.close()
            mt.DAT.alive = False


        self.signal_connectResult.emit(mt_id, result, QDateTime.currentDateTime())

    ####################################################################################################################

    @pyqtSlot(int)
    def msgprc_OnStationLost(self, mt_id):

        #print("disconnect 1, mt_id=" + str(mt_id))

        mt = self.appData.stations[mt_id - 1]

        #mt.DAT.alive = False

        if mt.DAT.ouc_connected:

            try:
                mt.DAT.opc_ua_client.disconnect()
                #mt.DAT.sock.close()   # AA
            except:
                do_nothing = 1
                #print("opc ua disconnect failed")

        #mt.DAT.opc_ua_client.disconnect()
        #mt.DAT.sock.close()

        if mt.DAT.alive:

            try:
                mt.DAT.sock.close()
            except:
                do_nothing = 1

        mt.DAT.ouc_connected = False
        mt.DAT.ouc_node = None
        mt.DAT.alive = False    # AA

        #print("disconnect 2, mt_id=" + str(mt_id))
        self.signal_disconnectResult.emit(mt_id, QDateTime.currentDateTime())


    ####################################################################################################################

    @pyqtSlot(int)
    def msgprc_OnStationLost1(self, mt_id):    # функция для теста
                                                # и с этой функцией работает хуже
        pass

    ####################################################################################################################

