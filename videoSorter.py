#! /usr/bin/python3
"""
videoSorter

Provides the video version of mainWindow
"""
import logging
import os
import sys

from PyQt5.QtCore import QCoreApplication, QSettings, Qt, QUrl, QSize, QPoint
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QSlider, QStyle, QVBoxLayout

from widgets.mainWindow import MainWindow


class VideoSorter(MainWindow):
    """
    VideoSorter version window
    """

    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        QCoreApplication.setOrganizationName("lRdG")
        QCoreApplication.setApplicationName("PyQt5 Video Library Sorter")
        self.settings = QSettings("./settings.ini", QSettings.IniFormat)
        self.title = 'PyQt5 Video Sorter'
        self.forbiddenKeys += [Qt.Key_Space, Qt.Key_Plus, Qt.Key_Minus, Qt.Key_0]
        self.dummy = QWidget()
        self.dummyLayout = QVBoxLayout()
        self.videoPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.playButton = QPushButton("Play")
        self.playButton.setFixedHeight(24)
        btnSize = QSize(16, 16)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.playButton.setFocusPolicy(Qt.NoFocus)
        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setFocusPolicy(Qt.NoFocus)
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        self.volume = 50
        self.initUI()
        self.prepareMediaList(path=".")
        self.isActive = False
        self.show()

    def initUI(self):
        super().initUI()
        self.videoPlayer.setVideoOutput(self.videoWidget)
        self.dummy.setLayout(self.dummyLayout)
        self.dummyLayout.addWidget(self.videoWidget)
        self.dummyLayout.addLayout(self.controlLayout)
        self.dummyLayout.addWidget(self.positionSlider)
        self.myWidget.addWidget(self.dummy)
        self.videoPlayer.stateChanged.connect(self.mediaStateChanged)
        self.videoPlayer.positionChanged.connect(self.positionChanged)
        self.videoPlayer.durationChanged.connect(self.durationChanged)
        self.videoPlayer.error.connect(self.handleError)

        super().adjustSplitter()

    def prepareMediaList(self, _triggered: bool = False, path: str = None, _matchingMime: str = None):
        super().prepareMediaList(_triggered, path, ['video/mp4', 'video/webm', 'video/quicktime',
                                                    'video/ogg'])
        # # QImageReader.supportedMimeTypes()

    def updateCurrentMedia(self):
        if len(self.mediaList) == 0:
            self.isActive = False
            self.videoPlayer.pause()
            self.videoWidget.hide()
            self.setFileName("None")
            logging.info("No acceptable file found")
        else:
            self.isActive = True
            self.videoWidget.show()
            relPath = self.mediaList[self.mediaListPosition].path
            self.setFileName(self.mediaList[self.mediaListPosition].path)
            relPath = os.path.abspath(relPath)
            self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(relPath)))
            self.playButton.setEnabled(True)
            self.play()

    def play(self):
        if self.videoPlayer.state() == QMediaPlayer.PlayingState:
            self.videoPlayer.pause()
            self.statusBar().showMessage("Playing.")
        else:
            self.videoPlayer.play()
            self.statusBar().showMessage("Pausing.")

    def mediaStateChanged(self, state: QMediaPlayer.MediaStatus):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position: int):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration: int):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position: int):
        self.videoPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.setFileName("Error: " + self.videoPlayer.errorString(), clean=True)
        self.statusBar().showMessage("Enable to play video.")

    def zoom(self, factor: QPoint):
        if factor.y() > 0:
            self.volume = min(100, self.volume + 5)
            self.statusBar().showMessage(f"Volume set to {self.volume}.")
        else:
            self.volume = max(0, self.volume - 5)
            self.statusBar().showMessage(f"Volume set to {self.volume}.")
        self.videoPlayer.setVolume(self.volume)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        eventKey = event.key()
        if eventKey == Qt.Key_Space:
            self.play()
            event.accept()
        elif eventKey == Qt.Key_Plus:
            self.volume = min(100, self.volume + 5)
            self.videoPlayer.setVolume(self.volume)
            event.accept()
        elif eventKey == Qt.Key_Minus:
            self.volume = max(0, self.volume - 5)
            self.videoPlayer.setVolume(self.volume)
            event.accept()
        elif eventKey == Qt.Key_0:
            self.volume = 50
            self.videoPlayer.setVolume(self.volume)
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoSorter()
    sys.exit(app.exec_())
