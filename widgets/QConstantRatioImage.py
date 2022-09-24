"""
QConstantRatioImage

Module providing a QLabel-herited class with zoom support, which ensures respecting image original ratio
"""
import logging

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QMovie, QImage
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget


class QConstantRatioImage(QLabel):
    """
    Widget to display images with zoom support, which ensures respecting image original ratio
    """

    def __init__(self, path: str, parent: QWidget = None, zoomFactors: tuple[float, float] = (0.8, 1.25)):
        super().__init__(parent)
        self.tempPolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.zoomPosition = 0
        self.scaleFactor = 1.0
        self.minFactor = 0.0
        self.idealFactor = 1.0
        self.myPixmap = QPixmap()
        self.defaultPath = path
        self.movie = QMovie()
        self.zoomFactors = zoomFactors

        self.initUI()
        self.updateImage(self.defaultPath)

    def initUI(self):
        self.setSizePolicy(self.tempPolicy)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)

    def zoomUp(self):
        self.zoomPosition += 1
        if not self.zoom():
            self.zoomPosition -= 1

    def zoomDown(self):
        self.zoomPosition -= 1
        if not self.zoom():
            self.zoomPosition += 1

    def zoom(self) -> bool:
        newFactor = self.idealFactor
        if self.zoomPosition < 0:
            newFactor *= self.zoomFactors[0] ** (-1 * self.zoomPosition)
        elif self.zoomPosition > 0:
            newFactor *= self.zoomFactors[1] ** self.zoomPosition
        if newFactor > self.scaleFactor or newFactor >= self.minFactor:
            self.scaleFactor = newFactor
            self.rescale()
            return True
        return False

    def resetZoom(self):
        self.zoomPosition = 0
        self.scaleFactor = self.idealFactor
        self.rescale()

    def originalRatio(self):
        self.zoomPosition = 0
        self.scaleFactor = 1.0
        self.rescale()

    def rescale(self):
        pixmap = self.myPixmap
        if not pixmap:
            pixmap = self.movie.currentPixmap()
        self.resize(self.scaleFactor * pixmap.size())

    def getImage(self) -> QImage:
        pixmap = self.myPixmap
        if not pixmap:
            pixmap = self.movie.currentPixmap()
        return pixmap.toImage()

    def calcIdealFactor(self, windowSize: QSize):
        pixmap = self.myPixmap
        if not pixmap:
            pixmap = self.movie.currentPixmap()
        if pixmap.size().height() > windowSize.height() or pixmap.size().width() > windowSize.width():
            # dim = True if height is the dim to study
            self.idealFactor = min(windowSize.height() / pixmap.size().height(), windowSize.width() / pixmap.size().width())
            self.idealFactor = min(1.0, self.idealFactor)

    def updateImage(self, newFilename: str, windowSize: QSize = QSize(1920, 1080), mimeType: str = None):
        if newFilename:
            # For some reason, QMovie.supporterFormats returns only the last part of the mimetype...
            if mimeType.split('/')[-1] in QMovie.supportedFormats():
                self.movie = QMovie(newFilename)
                if not self.movie.isValid():
                    logging.error("Movie (%s) isn't valid ", newFilename)
                else:
                    self.setMovie(self.movie)
                    self.movie.start()
                self.myPixmap = None
            else:
                self.myPixmap = QPixmap(newFilename)
                if self.myPixmap.isNull():
                    self.myPixmap = QPixmap(self.defaultPath)
                self.setPixmap(self.myPixmap)

                self.minFactor = 100/max(self.myPixmap.size().height(), self.myPixmap.size().width())

                self.calcIdealFactor(windowSize)

                self.scaleFactor = self.idealFactor
                self.zoomPosition = 0

                self.adjustSize()
                self.movie = None
