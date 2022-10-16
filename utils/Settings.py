"""
This module provides everything related to settings
"""
import logging
import pickle

from PyQt5.QtCore import Qt, QSize, QSettings, QPoint


CURRENTSETTINGSVERSION = 2


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
        self.settingsVersion = CURRENTSETTINGSVERSION
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
        self.settings.setValue("logLevel", pickle.dumps(self.logLevel))
        self.settings.setValue("settingsVersion", self.settingsVersion)
        self.settings.endGroup()
        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()
        self.settings.beginGroup("VideoSorter")
        self.settings.setValue("volume", self.volume)
        self.settings.endGroup()

    def restore(self) -> tuple[QSize, QPoint]:
        self.settings.beginGroup("MainWindow")
        emptyConf = not self.settings.contains("size")
        logging.info("No config found, we're gonna create it with latest version")
        size = self.settings.value("size", QSize(800, 600))
        pos = self.settings.value("pos", QPoint(0, 0))
        self.settings.endGroup()
        self.settings.beginGroup("KeyBindings")
        self.globalKeys = self.settings.value("defaultKeys", {Qt.Key_Right: "next", Qt.Key_Left: "prev",
                                                              Qt.Key_Home: "first", Qt.Key_End: "last",
                                                              Qt.Key_Delete: "delete", Qt.Key_Insert: "clipboard",
                                                              Qt.Key_Backspace: "hide"})
        self.imageKeys = self.settings.value("imageKeys", {Qt.Key_Plus: "zoomUp", Qt.Key_Minus: "zoomDown",
                                                           Qt.Key_0: "zoomReset", Qt.Key_1: "zoomRatio",
                                                           Qt.Key_4: "rotateLeft", Qt.Key_6: "rotateRight"})
        self.videoKeys = self.settings.value("videoKeys", {Qt.Key_Plus: "volumeUp", Qt.Key_Minus: "volumeDown",
                                                           Qt.Key_0: "volumeReset", Qt.Key_Space: "pause"})
        self.settings.endGroup()
        self.settings.beginGroup("Global")
        self.historyLength = int(self.settings.value("historyLength", 20))
        self.logLevel = pickle.loads(self.settings.value("logLevel", pickle.dumps(logging.ERROR)))
        if emptyConf:
            self.settingsVersion = CURRENTSETTINGSVERSION
        else:
            self.settingsVersion = int(self.settings.value("settingsVersion", 1))
        self.settings.endGroup()
        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()
        self.settings.beginGroup("VideoSorter")
        self.volume = int(self.settings.value("volume", 50))
        self.settings.endGroup()

        logging.getLogger().setLevel(self.logLevel)
        if self.settingsVersion != CURRENTSETTINGSVERSION:
            self.updateSettings()
        return size, pos

    def updateSettings(self):
        logging.info("Updating config from version %s to version %s", self.settingsVersion, CURRENTSETTINGSVERSION)
        if self.settingsVersion <= 1:
            self.settingsVersion += 1
            self.imageKeys.update({Qt.Key_4: "rotateLeft", Qt.Key_6: "rotateRight"})
