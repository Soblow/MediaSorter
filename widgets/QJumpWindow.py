"""
QJumpWindow

Module providing a dialog window to select the mediaList position to which user want to go
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal


class QJumpWindow(QDialog):
    """
    Dialog window to select the mediaList position to which user want to go
    """
    validate = pyqtSignal(int)

    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags(), maxNumber: int = 1, curPos: int = 0):
        super().__init__(parent, flags)
        self.maxNumber = maxNumber

        self.validateButton = QPushButton("Validate")
        self.cancelButton = QPushButton("Cancel")

        self.helpLabel = QLabel(
            f"Choose the item to jump to, then press Validate (max: {self.maxNumber})")
        self.toComboBox = QSpinBox()
        self.buttonLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.initUI(curPos)

        self.validate.connect(parent.jumpToCallback)
        self.show()

    def initUI(self, curPos: int = 0):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.helpLabel)
        self.mainLayout.addWidget(self.toComboBox)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.validateButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.cancelButton.clicked.connect(self.close)
        self.validateButton.clicked.connect(self.validating)

        self.toComboBox.setMaximum(self.maxNumber)
        self.toComboBox.setValue(curPos)

    def validating(self):
        self.validate.emit(int(self.toComboBox.value()))
        self.close()
