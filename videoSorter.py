#! /usr/bin/python3
"""
videoSorter

Provides the video version of mainWindow
"""
import logging
import os
import sys

from PyQt5.QtCore import Qt, QUrl, QSize, QPoint, QByteArray
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
        self.title = 'Video Sorter'
        self.forbiddenKeys += self.settings.videoKeys.keys()
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

        self.initUI()
        self.isActive = False
        self.nonexist = False
        self.show()
        self.prepareMediaList()

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
        # self.videoWidget.setVisible(False)

        super().adjustSplitter()

    def prepareMediaList(self, _triggered: bool = False, path: str = None, _matchingMime: list[QByteArray] = None):
        super().prepareMediaList(_triggered, path, [QByteArray(b'video/mp4'), QByteArray(b'video/webm'),
                                                    QByteArray(b'video/quicktime'), QByteArray(b'video/ogg')])

    def updateCurrentMedia(self):
        self.setFileName("None")
        self.nonexist = False
        if len(self.mediaList) > 0:
            relPath = self.mediaList[self.mediaListPosition].path
            absPath = os.path.abspath(relPath)
            if os.path.exists(absPath):
                self.isActive = True
                # self.videoWidget.setVisible(True)
                self.setFileName(relPath)
                self.videoPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(absPath)))
                self.playButton.setEnabled(True)
                if self.settings.video_autoplay:
                    self.videoPlayer.play()
                self.statusBar().showMessage("Playing.")
                return
            self.setFileName("File no longer exists")
            logging.info("File no longer exists")
            self.nonexist = True
        else:
            logging.info("No acceptable file found")
        self.isActive = False
        self.videoPlayer.pause()
        self.statusBar().showMessage("Pausing.")
        # self.videoWidget.setVisible(False)

    def play(self):
        if self.isActive:
            if self.videoPlayer.state() == QMediaPlayer.PlayingState:
                self.videoPlayer.pause()
                self.statusBar().showMessage("Pausing.")
            else:
                self.videoPlayer.play()
                self.statusBar().showMessage("Playing.")

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
            self.settings.volume = min(100, self.settings.volume + 5)
            self.statusBar().showMessage(f"Volume set to {self.settings.volume}.")
        else:
            self.settings.volume = max(0, self.settings.volume - 5)
            self.statusBar().showMessage(f"Volume set to {self.settings.volume}.")
        self.videoPlayer.setVolume(self.settings.volume)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        eventKey = event.key()
        if eventKey not in self.settings.videoKeys:
            return
        act = self.settings.videoKeys[eventKey]
        if act == "pause":
            self.play()
        elif act == "volumeUp":
            self.settings.volume = min(100, self.settings.volume + 5)
            self.videoPlayer.setVolume(self.settings.volume)
        elif act == "volumeDown":
            self.settings.volume = max(0, self.settings.volume - 5)
            self.videoPlayer.setVolume(self.settings.volume)
        elif act == "volumeReset":
            self.settings.volume = 50
            self.videoPlayer.setVolume(self.settings.volume)
        else:
            logging.error("Unsupported action from settings (%s). This should never happen", act)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoSorter()
    sys.exit(app.exec_())
