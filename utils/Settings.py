"""
This module provides everything related to settings
"""
import logging

from PyQt5.QtCore import Qt, QSize, QSettings, QPoint


class Settings:
    """
    This class embeds the MediaSorter settings. A few helper methods are provided to ease manipulation
    """
    def __init__(self):
        self.settings = QSettings()
        self.globalKeys = {}
        self.imageKeys = {}
        self.videoKeys = {}
        self.volume = 50
        self.historyLength = 20
        self.logLevel = logging.ERROR

    def save(self, size: QSize, pos: QPoint):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", size)
        self.settings.setValue("pos", pos)
        self.settings.endGroup()
        self.settings.beginGroup("KeyBindings")
        self.settings.setValue("globalKeys", self.globalKeys)
        self.settings.setValue("imageKeys", self.imageKeys)
        self.settings.setValue("videoKeys", self.videoKeys)
        self.settings.endGroup()
        self.settings.beginGroup("Global")
        self.settings.setValue("historyLength", self.historyLength)
        self.settings.setValue("logLevel", self.logLevel)
        self.settings.endGroup()
        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()
        self.settings.beginGroup("VideoSorter")
        self.settings.setValue("volume", self.volume)
        self.settings.endGroup()

    def restore(self) -> tuple[QSize, QPoint]:
        self.settings.beginGroup("MainWindow")
        size = self.settings.value("size", QSize(800, 600))
        pos = self.settings.value("pos", QPoint(0, 0))
        self.settings.endGroup()
        self.settings.beginGroup("KeyBindings")
        self.globalKeys = self.settings.value("defaultKeys", {Qt.Key_Right: "next", Qt.Key_Left: "prev",
                                                              Qt.Key_Home: "first", Qt.Key_End: "last",
                                                              Qt.Key_Delete: "delete", Qt.Key_Insert: "clipboard",
                                                              Qt.Key_Backspace: "hide"})
        self.imageKeys = self.settings.value("imageKeys", {Qt.Key_Plus: "zoomUp", Qt.Key_Minus: "zoomDown",
                                                           Qt.Key_0: "zoomReset", Qt.Key_1: "zoomRatio"})
        self.videoKeys = self.settings.value("videoKeys", {Qt.Key_Plus: "volumeUp", Qt.Key_Minus: "volumeDown",
                                                           Qt.Key_0: "volumeReset", Qt.Key_Space: "pause"})
        self.settings.endGroup()
        self.settings.beginGroup("Global")
        self.historyLength = self.settings.value("historyLength", 20)
        self.logLevel = self.settings.value("logLevel", logging.ERROR)
        self.settings.endGroup()
        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()
        self.settings.beginGroup("VideoSorter")
        self.volume = self.settings.value("volume", 50)
        self.settings.endGroup()
        return size, pos
