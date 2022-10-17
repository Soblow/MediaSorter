"""
changeActionWidget

Module providing ChangeAction dialog
"""
import copy

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, \
    QWidget

from utils import fileUtils as fsUtils
from utils import BindingsGlobals


class ChangeAction(QDialog):
    """
    Dialog window allowing to edit what a biding is doing
    """

    def __init__(self, parent: QWidget, actId: int, act: BindingsGlobals.SorterAction):
        super().__init__(parent)
        self.actId = actId
        self.act = act
        self.newact = copy.deepcopy(act)

        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.validateButton = QPushButton("Validate")
        self.pathLayout = QHBoxLayout()
        self.pathLabel = QLabel("Path")
        self.pathLineEdit = QLineEdit()
        self.pathButton = QPushButton("...")
        self.actLayout = QHBoxLayout()
        self.actLabel = QLabel("Action")
        self.actChoose = QComboBox()

        self.initUI()
        self.show()

    def initUI(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.actLayout)
        self.mainLayout.addLayout(self.pathLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addWidget(self.validateButton)
        self.actLayout.addWidget(self.actLabel)
        self.actLayout.addWidget(self.actChoose)
        self.pathLayout.addWidget(self.pathLabel)
        self.pathLayout.addWidget(self.pathLineEdit)
        self.pathLayout.addWidget(self.pathButton)

        for e in sorted(BindingsGlobals.AVAILABLESORTERACTIONS.keys()):
            self.actChoose.addItem(e)

        self.pathLineEdit.setText(self.act.path)
        self.pathLineEdit.setEnabled(False)

        self.actChoose.setCurrentText(self.act.name)

        self.validateButton.clicked.connect(self.validate)
        self.cancelButton.clicked.connect(self.close)
        self.pathButton.clicked.connect(self.choosePath)
        self.actChoose.currentTextChanged.connect(self.chooseAct)

    def validate(self):
        self.parentWidget().editAction(self.actId, self.newact)
        self.close()

    @pyqtSlot(str)
    def chooseAct(self, newAct: str):
        tmpAct = BindingsGlobals.AVAILABLESORTERACTIONS[newAct]()
        tmpAct.path = self.newact.path
        tmpAct.keystr = self.newact.keystr
        self.newact = tmpAct
        if newAct == BindingsGlobals.SorterAction.name:
            self.newact.path = ""
        self.pathLineEdit.setText(self.newact.path)

    @pyqtSlot()
    def choosePath(self):
        rez = fsUtils.chooseDirectory(self)
        if rez[0]:
            self.newact.path = rez[1]
            self.pathLineEdit.setText(self.newact.path)
        else:
            self.newact.path = ""
            self.pathLineEdit.setText("")
