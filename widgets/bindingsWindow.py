"""
bindingsWindow

Module provinding the bindings editing window
"""

import logging

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget

from utils import BindingsGlobals
from widgets.bindingsListWidget import BindingsListWidget
from widgets.createBindingDialog import CreateBindingDialog


class BindingsWindow(QDialog):
    """
    Provides a QDialog to edit bindings
    """
    validate = pyqtSignal(str)
    refreshList = pyqtSignal(dict)

    def __init__(self, parent: QWidget, bindings: dict[int, BindingsGlobals.SorterAction], configPath: str,
                 forbiddenKeys: list = None):
        super().__init__(parent)
        if forbiddenKeys is None:
            forbiddenKeys = []
        self.forbiddenKeys = forbiddenKeys
        self.baseWidth = 800
        self.baseHeight = 480
        self.parentWindow = parent
        self.bindings = bindings
        self.validate.connect(parent.openConfig)
        self.configPath = configPath

        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.cancelButton = QPushButton("Cancel")
        self.validateButton = QPushButton("Validate")
        self.addButton = QPushButton("Add Binding")
        self.actionsAvailable = BindingsListWidget(self, self.bindings)
        self.initUI()
        self.refreshList.connect(self.actionsAvailable.buildBindingList)
        self.show()

    def initUI(self):
        self.resize(self.baseWidth, self.baseHeight)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.actionsAvailable)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.validateButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.actionsAvailable.buildBindingList()

        self.cancelButton.clicked.connect(self.closing)
        self.validateButton.clicked.connect(self.validating)
        self.addButton.clicked.connect(self.addBinding)

    @pyqtSlot()
    def closing(self):
        super().close()

    @pyqtSlot()
    def validating(self):
        if self.configPath != "":
            BindingsGlobals.saveBindings(self.configPath, self.bindings)
        else:
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.AnyFile)
            if fileDialog.exec():
                self.configPath = fileDialog.selectedFiles()[0]
                BindingsGlobals.saveBindings(self.configPath, self.bindings)

        self.validate.emit(self.configPath)
        super().close()

    def addBinding(self):
        _bindingWindow = CreateBindingDialog(self, forbiddenKeys=self.forbiddenKeys +
                                                                 [int(e) for e in self.bindings.keys()])

    def addBindingCallback(self, keyAdded: int):
        if keyAdded == 0:
            logging.info("No key was selected, assuming cancel.")
            return

        if keyAdded in self.bindings:
            logging.warning("Can't add this action as this key (%s) is already registered", keyAdded)
            return

        newAction = BindingsGlobals.SorterAction()
        newAction.path = ""
        newAction.keystr = QKeySequence(Qt.Key(keyAdded)).toString()
        self.bindings[keyAdded] = newAction
        self.refreshList.emit(self.bindings)
        logging.info("Key %s (%s) added with empty action", keyAdded, newAction.keystr)
