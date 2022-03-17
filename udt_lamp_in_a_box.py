from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout


from udt_lamp import *


class UDT_LAMP_IN_A_BOX(QWidget):

    def __init__(self,cl=ENM_LAMP_COLOR.GREY,sh=ENM_LAMP_SHAPE.ROUND,pl=0):

        super().__init__()
        self.lamp = UDT_LAMP(cl=cl,sh=sh,pl=pl)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,3,0,0)
        self.layout.addStretch()
        self.layout.addWidget(self.lamp)
        self.layout.addStretch()

        self.setLayout(self.layout)

