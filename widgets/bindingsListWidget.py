"""
bindingsListWidget

A module proving the BindingsListWidget widget, a simple widget for the BindingsWindow
It allows listing of bindings, and editing
"""

from PyQt5.QtCore import Qt, QSignalMapper
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHeaderView, QAbstractItemView, \
    QAbstractScrollArea, QSizePolicy, QLabel

from widgets.changeActionWidget import ChangeAction


class BindingsListWidget(QTableWidget):
    """
    A widget provinding a list of bindings inside a QTableWidget.
    Buttons are automatically bound to edit/remove the bindings
    """

    def __init__(self, parent: QWidget, data: dict):
        super().__init__(1, 4, parent)
        self.bindings = data
        self.signalRemove = QSignalMapper(self)
        self.signalEdit = QSignalMapper(self)

        self.signalRemove.mapped[int].connect(self.removeBinding)
        self.signalEdit.mapped[int].connect(self.editBinding)

        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setMinimumHeight(100)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def buildBindingList(self, newBindings: dict = None):
        if newBindings is not None:
            self.bindings = newBindings
        self.clearContents()
        self.setRowCount(len(self.bindings['keys'].keys()))
        i = 0
        for key in sorted(self.bindings['keys'].keys()):
            entry = self.bindings['keys'][key]
            removeButton = QPushButton("Remove")
            changeButton = QPushButton("Change")
            removeButton.setMaximumHeight(25)
            changeButton.setMaximumHeight(25)
            self.signalEdit.setMapping(changeButton, i)
            self.signalRemove.setMapping(removeButton, i)
            changeButton.clicked.connect(self.signalEdit.map)
            removeButton.clicked.connect(self.signalRemove.map)
            self.setCellWidget(i, 0, removeButton)
            self.setItem(i, 1, QTableWidgetItem(QKeySequence(Qt.Key(key)).toString()))
            desc = f"{entry['action']} to {entry['path']}"
            newEntry = QLabel(desc)
            newEntry.setToolTip(desc)
            newEntry.setWordWrap(True)
            newEntry.adjustSize()
            newEntry.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
            self.setCellWidget(i, 2, newEntry)
            self.setCellWidget(i, 3, changeButton)
            i += 1
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(3)

    def editBinding(self, widgetId: int):
        theKeyName = self.item(widgetId, 1).text()
        theBinding = self.bindings['keys'][str(QKeySequence(theKeyName)[0])]
        _dialog = ChangeAction(self, widgetId, theBinding["action"], theBinding["path"])

    def editAction(self, actId: int, act: str, path: str):
        theKeyName = self.item(actId, 1).text()
        self.bindings['keys'][str(QKeySequence(theKeyName)[0])]["action"] = act
        self.bindings['keys'][str(QKeySequence(theKeyName)[0])]["path"] = path
        self.buildBindingList()

    def removeBinding(self, widgetId: int):
        theKeyName = self.item(widgetId, 1).text()
        self.bindings['keys'].pop(str(QKeySequence(theKeyName)[0]))
        self.buildBindingList()
