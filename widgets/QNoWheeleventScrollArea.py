"""
QNoWheeleventScrollArea

Module providing a ScrollArea ignoring Scroll events
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent, QKeyEvent
from PyQt5.QtWidgets import QScrollArea, QWidget


class QNoWheeleventScrollArea(QScrollArea):
    """
    ScrollArea ignoring Scroll events
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(False)

    def wheelEvent(self, event: QWheelEvent):
        event.ignore()

    def keyPressEvent(self, event: QKeyEvent):
        event.ignore()
