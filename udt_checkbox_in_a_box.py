from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QCheckBox




class UDT_CHECKBOX_IN_A_BOX(QWidget):

    def __init__(self):

        super().__init__()
        self.checkbox = QCheckBox()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch()
        self.layout.addWidget(self.checkbox)
        self.layout.addStretch()

        self.setLayout(self.layout)

