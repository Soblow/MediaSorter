"""
createBindingDialog

Module providing the createBindingDialog window
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class CreateBindingDialog(QDialog):
    """
    Dialog to create new binding, by asking the key
    """
    myKey = 0
    validate = pyqtSignal(int)
    recording = False

    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags(), forbiddenKeys=None):
        super().__init__(parent, flags)
        if forbiddenKeys is None:
            forbiddenKeys = []
        self.forbiddenKeys = forbiddenKeys
        self.validateButton = QPushButton("Validate")
        self.recordButton = QPushButton("Record")
        self.cancelButton = QPushButton("Cancel")
        self.helpLabel = QLabel("Press the Record button to record your next key pressing.\n"
                                "Click on validate to create a new binding")
        self.currentKeyLabel = QLabel("Current Key : None")
        self.buttonLayout = QHBoxLayout()
        self.mainLayout = QVBoxLayout()

        self.initUI()

        self.validate.connect(parent.addBindingCallback)
        self.show()

    def setRecording(self):
        self.recording = True

    def keyPressEvent(self, a0: QKeyEvent):
        if self.recording:
            if a0.key() in self.forbiddenKeys:
                self.currentKeyLabel.setText("This key is reserved or already in use. Please choose an other one")
            else:
                self.recording = False
                self.myKey = a0.key()
                self.currentKeyLabel.setText(f"Current Key : {self.myKey} ({a0.text()})")

    def initUI(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.helpLabel)
        self.mainLayout.addWidget(self.currentKeyLabel)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.validateButton)
        self.buttonLayout.addWidget(self.recordButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.cancelButton.clicked.connect(self.close)
        self.recordButton.clicked.connect(self.setRecording)
        self.validateButton.clicked.connect(self.validating)

    def validating(self):
        self.validate.emit(self.myKey)
        self.close()
