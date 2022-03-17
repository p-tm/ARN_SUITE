########################################################################################################################

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

import socket



########################################################################################################################
# описание класса:
# -
########################################################################################################################

class UDT_NETWORK_CHECKER(QObject):

    #signal_StationFound = pyqtSignal(int)
    #signal_StationLost = pyqtSignal(int)

    def __init__(self, app_data):

        super().__init__()

        self.appData = app_data

        self.checkAllowed = True


# а как вот правильно опрашивать узлы? в несколько потоков?
# или просто в несколько параллельных сокетов?



    ####################################################################################################################

    @pyqtSlot()
    def msgprc_OnDoCheck(self):

        self.checkAllowed = False

        #print("попытка соединения @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))
        self.appData.window_MainWindow.signal_IsCheckingNetwork.emit()
        # я чего то не понял - тут попытка соединиться даже если есть открытое соединение?
        # вот тут чего то неправильно

        #for mt in self.appData.stations:
        #
        #    if mt.PAR.persists and not mt.DAT.alive:
        #        try:
        #            mt.DAT.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #            mt.DAT.sock.settimeout(0.2)
        #       except socket.error:
        #            print("Failed to create socket on mt.id=" + mt.PAR.id)

        #for mt in self.appData.stations:
        #    if mt.PAR.persists and mt.DAT.alive and not mt.DAT.ouc_connected:
        #        if mt.DAT.alive:
        #            try:
        #                mt.DAT.sock.close()
        #            except:
        #                do_nothing = 1
        #            mt.DAT.alive = False

        for mt in self.appData.stations:

            if mt.PAR.persists and not mt.DAT.alive:

                sock_err = False

                #print("запрос данных FIO @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))

                if not mt.DAT.alive:

                    self.appData.window_MainWindow.signal_IsCheckingSocket.emit(mt.PAR.id)

                    try:
                        mt.DAT.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AA
                        mt.DAT.sock.settimeout(0.2) # AA
                        mt.DAT.sock.connect((mt.PAR.string_IP, mt.PAR.port))
                    #except socket.timeout:
                    except TimeoutError:
                        sock_err = True
                        print("timeout on mt.id=" + str(mt.PAR.id))
                    except InterruptedError:
                        sock_err = True
                    except:
                        sock_err = True    # AA
                    finally:

                        if not sock_err:
                            mt.DAT.socket_error = False
                            mt.DAT.alive = True
                            #if not mt.DAT.alive:
                            self.appData.window_MainWindow.signal_StationFound.emit(mt.PAR.id) # worker_FieldAccess::msgprc_OnStationFound()

        #for mt in self.appData.stations:
        #
        #    if mt.PAR.persists and mt.DAT.alive and not mt.DAT.ouc_connected:
        #
        #            self.appData.window_MainWindow.signal_StationFound.emit(mt.PAR.id)  # worker_FieldAccess::msgprc_OnStationFound()

        self.checkAllowed = True

        #        else:
        #            mt.DAT.socket_error = True
        #            #mt.DAT.alive = False
        #            if mt.DAT.alive:
        #                self.signal_StationLost.emit(mt.PAR.id)
        #               pass # пока уберём, но надо протестировать
        #                     # вероятно тут всё равно надо вставлять закрывание сокета

                #print("запрос данных -конец- @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))



        #try:
        #    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    #s.setblocking(False)
        #    s1.settimeout(0.2)
        #    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    #s.setblocking(False)
        #    s2.settimeout(0.2)
        #except socket.error:
        #    print("Failed to create socket")

        #try:
        #    s1.connect((host, port))
        #    #info = s.recv(4096)
        #    #print(info)
        #except socket.timeout:
        #    socket1_error = 1
        #    print("timeout 1")
        #except socket.error:
        #    socket1_error = 1
        #    print("Failed to connect to IP")
        #
        #try:
        #    s2.connect(("192.168.1.5", port))
        #    #info = s.recv(4096)
        #    #print(info)
        #except socket.timeout:
        #    socket2_error = 1
        #    print("timeout 2")
        #except socket.error:
        #    socket2_error = 1
        #    print("Failed to connect to IP")
        #
        #if not socket1_error:
        #    print("успешно 1")
        #if not socket2_error:
        #    print("успешно 2")

        #print("завершено @ " + QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss.zzz"))




    ####################################################################################################################
