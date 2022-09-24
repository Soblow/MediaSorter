#!/usr/bin/python3
"""
imageSorter

Provides the image version of mainWindow
"""
import os.path
import sys

from PyQt5.QtCore import QCoreApplication, QSettings, Qt, QSize, QPoint, QByteArray
from PyQt5.QtGui import QImageReader, QMouseEvent, QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from widgets.QConstantRatioImage import QConstantRatioImage
from widgets.QNoWheeleventScrollArea import QNoWheeleventScrollArea
from widgets.mainWindow import MainWindow


class ImageSorter(MainWindow):
    """
    ImageSorter version window
    """

    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        QCoreApplication.setOrganizationName("lRdG")
        QCoreApplication.setApplicationName("PyQt5 Image Library Sorter")
        self.settings = QSettings("./settings.ini", QSettings.IniFormat)
        self.title = 'PyQt5 Image Sorter'
        self.forbiddenKeys += [Qt.Key_Plus, Qt.Key_Minus, Qt.Key_0, Qt.Key_1]
        self.dummyWidgetSA = QWidget()
        self.dummyLayoutSA = QVBoxLayout()
        self.scrollArea = QNoWheeleventScrollArea()
        self.image = QConstantRatioImage("", self, (0.8, 1.25))
        self.initUI()
        self.prepareMediaList(path=".")
        self.isActive = False
        self.nonexist = False
        self.show()

    def initUI(self):
        super().initUI()
        self.scrollArea.setWidget(self.image)
        self.dummyWidgetSA.setLayout(self.dummyLayoutSA)
        self.dummyLayoutSA.addWidget(self.scrollArea)
        self.myWidget.addWidget(self.dummyWidgetSA)
        self.image.initUI()

        super().adjustSplitter()

    def prepareMediaList(self, _triggered: bool = False, path: str = None, _matchingMime: list[QByteArray] = None):
        super().prepareMediaList(_triggered, path, QImageReader.supportedMimeTypes())

    def updateCurrentMedia(self):
        self.setFileName("None")
        self.nonexist = False
        scrollAreaSize = (self.scrollArea.size()-QSize(50, 50)).expandedTo(QSize(50, 50))
        if len(self.mediaList) > 0:
            currpath = self.mediaList[self.mediaListPosition].path
            if os.path.exists(currpath):
                self.isActive = True
                self.image.show()
                self.image.updateImage(currpath, scrollAreaSize, self.mediaList[self.mediaListPosition].mime)
                self.setFileName(currpath)
                self.image.rescale()
                return
            self.setFileName("File no longer exists")
            self.nonexist = True
        self.isActive = False
        self.image.hide()

    def resizeEvent(self, event: QResizeEvent):
        scrollAreaSize = (self.scrollArea.size()-QSize(50, 50)).expandedTo(QSize(50, 50))
        self.image.calcIdealFactor(scrollAreaSize)
        self.image.rescale()
        event.accept()

    def zoom(self, factor: QPoint):
        if factor.y() > 0:
            self.image.zoomUp()
        else:
            self.image.zoomDown()

    def splitterMovedEvent(self, pos: int, index: int):
        super().splitterMovedEvent(pos, index)
        self.image.rescale()

    def copyCurrentToClipboard(self):
        self.statusBar().showMessage("Copying image to clipboard.")
        self.clipboard.setImage(self.image.getImage())

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MiddleButton:
            delta = event.pos() - self.origPos
            self.scrollArea.verticalScrollBar().setValue(self.origVer + delta.y())
            self.scrollArea.horizontalScrollBar().setValue(self.origHor + delta.x())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() in [Qt.MiddleButton, Qt.LeftButton]:
            self.origPos = event.pos()
            self.origHor = self.scrollArea.horizontalScrollBar().value()
            self.origVer = self.scrollArea.verticalScrollBar().value()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() in [Qt.MiddleButton, Qt.LeftButton]:
            self.origPos = None
            self.origHor = None
            self.origVer = None
            event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        eventKey = event.key()
        if eventKey == Qt.Key_Plus:
            self.image.zoomUp()
            event.accept()
        elif eventKey == Qt.Key_Minus:
            self.image.zoomDown()
            event.accept()
        elif eventKey == Qt.Key_0:
            self.image.resetZoom()
            event.accept()
        elif eventKey == Qt.Key_1:
            self.image.originalRatio()
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSorter()
    sys.exit(app.exec_())
