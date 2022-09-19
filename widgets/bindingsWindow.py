"""
bindingsWindow

Module provinding the bindings editing window
"""

import json
import logging

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget

from widgets.bindingsListWidget import BindingsListWidget
from widgets.createBindingDialog import CreateBindingDialog


class BindingsWindow(QDialog):
    """
    Provides a QDialog to edit bindings
    """
    validate = pyqtSignal(str)
    refreshList = pyqtSignal(dict)

    def __init__(self, parent: QWidget, bindings: dict, configPath: str, forbiddenKeys: list = None):
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
            self.writeConfig(self.configPath)
        else:
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.AnyFile)
            if fileDialog.exec():
                self.configPath = fileDialog.selectedFiles()[0]
                self.writeConfig(self.configPath)

        self.validate.emit(self.configPath)
        super().close()

    def writeConfig(self, path: str):
        logging.info("Writing configuration to %s", path)
        with open(path, "w", encoding="us-ascii") as file:
            json.dump(self.bindings, file)

    def addBinding(self):
        _bindingWindow = CreateBindingDialog(self, forbiddenKeys=self.forbiddenKeys + [int(e) for e in self.bindings['keys']])

    def addBindingCallback(self, keyAdded: int):
        if keyAdded != 0:
            strKey = str(keyAdded)
            if strKey in self.bindings['keys']:
                logging.warning("Can't add this binding as key is already registered")
            else:
                self.bindings['keys'][strKey] = {}
                self.bindings['keys'][strKey]["action"] = "nothing"
                self.bindings['keys'][strKey]["path"] = ""
                self.refreshList.emit(self.bindings)
        else:
            logging.info("No key was selected, assuming cancel.")
