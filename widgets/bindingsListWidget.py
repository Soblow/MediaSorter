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
from utils import BindingsGlobals


class BindingsListWidget(QTableWidget):
    """
    A widget providing a list of bindings inside a QTableWidget.
    Buttons are automatically bound to edit/remove the bindings
    """

    def __init__(self, parent: QWidget, bindings: dict[int, BindingsGlobals.SorterAction], keyEditable: bool = False,
                 actionEditable: bool = True):
        super().__init__(1, 4, parent=parent)
        self.bindings = bindings
        self.keyEditable = keyEditable
        self.actionEditable = actionEditable

        # Signal creation
        self.signalRemove = QSignalMapper(self)
        self.signalEditAction = QSignalMapper(self)
        self.signalEditKey = QSignalMapper(self)
        # Here we set the signals to be mapped on all the instances of the buttons we'll have
        self.signalRemove.mapped[int].connect(self.removeBinding)
        self.signalEditAction.mapped[int].connect(self.editBinding)
        self.signalEditKey.mapped[int].connect(self.editKey)

        # Init UI
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setMinimumHeight(100)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def buildBindingList(self, newBindings: dict[int, BindingsGlobals.SorterAction] = None):
        """
        This function will rebuild the binding list, possibly using new bindings
        :param newBindings: new bindings list
        :return: None
        """
        if newBindings is not None:
            self.bindings = newBindings
        self.clearContents()
        self.setRowCount(len(self.bindings))

        i = 0
        for key in sorted(self.bindings.keys()):
            entry = self.bindings[key]
            removeButton = QPushButton("Remove")
            changeButton = QPushButton("Change")
            removeButton.setMaximumHeight(25)
            changeButton.setMaximumHeight(25)
            self.signalEditAction.setMapping(changeButton, i)
            self.signalRemove.setMapping(removeButton, i)
            changeButton.clicked.connect(self.signalEditAction.map)
            removeButton.clicked.connect(self.signalRemove.map)
            self.setCellWidget(i, 0, removeButton)
            self.setItem(i, 1, QTableWidgetItem(QKeySequence(Qt.Key(key)).toString()))
            desc = f"{entry.name} to {entry.path}"
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
        """
        Callback for each "Edit action" buttons
        :param widgetId: ID of the widget which called this (used to find which row is edited)
        :return: None
        """
        theKeyName = self.item(widgetId, 1).text()
        theId = int(QKeySequence(theKeyName)[0])
        theBinding = self.bindings[theId]
        _dialog = ChangeAction(self, widgetId, theBinding)

    def editKey(self, widgetId: int):
        """
        Callback for each "Edit key" buttons
        :param widgetId: ID of the widget which called this (used to find which row is edited)
        :return: None
        """
        pass

    def editAction(self, widgetId: int, act: BindingsGlobals.SorterAction):
        """
        Callback from the ChangeAction Dialog (opened with editBinding callback)
        Triggers buildBindingList()
        :param widgetId: ID of the widget which called this (used to find which row is edited)
        :param act: The new action
        :return: None
        """
        theKeyName = self.item(widgetId, 1).text()
        theId = int(QKeySequence(theKeyName)[0])
        self.bindings[theId] = act
        self.buildBindingList()

    def removeBinding(self, widgetId: int):
        """
        Callback for each "Remove" buttons
        Triggers buildBindingList()
        :param widgetId: ID of the widget which called this (used to find which row is edited)
        :return: None
        """
        theKeyName = self.item(widgetId, 1).text()
        theId = int(QKeySequence(theKeyName)[0])
        self.bindings.pop(theId)
        self.buildBindingList()
