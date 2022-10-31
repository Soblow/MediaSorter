"""
This module provides everything related to settings
"""
import enum
import logging
import pickle

from PyQt5.QtCore import Qt, QSize, QSettings, QPoint

CURRENTSETTINGSVERSION = 4

class SortMethod(enum.Enum):
    """
    Type of sorting methods available
    """
    none = 0  # Do nothing
    name = 1  # Name (alphabetical)
    nameRev = 2  # Name (reverse alphabetical)
    size = 3  # File Size (increasing)
    sizeDec = 4  # File Size (decreasing)
    creatDate = 5  # Date of creation
    creatDateDec = 6  # Date of creation (reverse)
    modifDate = 7  # Date of modification
    modifDateDec = 8  # Date of modification (reverse)

class Settings:
    """
    This class embeds the MediaSorter settings. A few helper methods are provided to ease manipulation
    """

    def __init__(self):
        self.settings = QSettings()

        # KeyBindings
        self.globalKeys = {}
        self.imageKeys = {}
        self.videoKeys = {}

        # Global
        self.settingsVersion = CURRENTSETTINGSVERSION
        self.historyLength = 20
        self.logLevel = logging.ERROR
        self.indexing_async = True
        self.indexing_threads = -1
        self.indexing_refreshPeriod = 0.5
        self.indexing_batchSize = 10
        self.indexing_batchTime = False
        self.indexing_batchTimeLimit = 0.5
        self.indexing_recursive = False
        self.autosort = False
        self.sort_method = SortMethod.none

        # ImageSorter

        # VideoSorter
        self.volume = 50
        self.video_autoplay = True

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
        self.settings.setValue("settingsVersion", self.settingsVersion)
        self.settings.setValue("historyLength", self.historyLength)
        self.settings.setValue("logLevel", pickle.dumps(self.logLevel))
        self.settings.setValue("indexing_async", self.indexing_async)
        self.settings.setValue("indexing_threads", self.indexing_threads)
        self.settings.setValue("indexing_refreshPeriod", self.indexing_refreshPeriod)
        self.settings.setValue("indexing_batchSize", self.indexing_batchSize)
        self.settings.setValue("indexing_batchTime", self.indexing_batchTime)
        self.settings.setValue("indexing_batchTimeLimit", self.indexing_batchTimeLimit)
        self.settings.setValue("indexing_recursive", self.indexing_recursive)
        self.settings.setValue("autosort", self.autosort)
        self.settings.setValue("sort_method", pickle.dumps(self.sort_method))
        self.settings.endGroup()

        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()

        self.settings.beginGroup("VideoSorter")
        self.settings.setValue("volume", self.volume)
        self.settings.setValue("video_autoplay", self.video_autoplay)
        self.settings.endGroup()

    def restore(self) -> tuple[QSize, QPoint]:
        self.settings.beginGroup("MainWindow")
        emptyConf = not self.settings.contains("size")
        if emptyConf:
            logging.info("No config found, we're gonna create it with latest version.\
             Perhaps it's the first time you start the app?")
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
        if emptyConf:
            self.settingsVersion = CURRENTSETTINGSVERSION
        else:
            self.settingsVersion = self.settings.value("settingsVersion", 1, type=int)
        self.historyLength = self.settings.value("historyLength", 20, type=int)
        self.logLevel = pickle.loads(self.settings.value("logLevel", pickle.dumps(logging.ERROR)))

        self.indexing_async = self.settings.value("indexing_async", False, type=bool)
        self.indexing_threads = self.settings.value("indexing_threads", -1, type=int)
        self.indexing_refreshPeriod = self.settings.value("indexing_refreshPeriod", 50, type=int)
        self.indexing_batchSize = self.settings.value("indexing_batchSize", 50, type=int)
        self.indexing_batchTime = self.settings.value("indexing_batchTime", False, type=bool)
        self.indexing_batchTimeLimit = self.settings.value("indexing_batchTimeLimit", 0.5, type=float)
        self.indexing_recursive = self.settings.value("indexing_recursive", False, type=bool)
        self.autosort = self.settings.value("autosort", False, type=bool)
        self.sort_method = pickle.loads(self.settings.value("sort_method", pickle.dumps(SortMethod.none)))
        self.settings.endGroup()

        self.settings.beginGroup("ImageSorter")
        self.settings.endGroup()

        self.settings.beginGroup("VideoSorter")
        self.volume = self.settings.value("volume", 50, type=int)
        self.video_autoplay = self.settings.value("video_autoplay", True, type=bool)
        self.settings.endGroup()

        logging.getLogger().setLevel(self.logLevel)
        if self.settingsVersion != CURRENTSETTINGSVERSION:
            self.updateSettings(size, pos)
        return size, pos

    def updateSettings(self, size: QSize, pos: QPoint):
        logging.info("Updating config from version %s to version %s", self.settingsVersion, CURRENTSETTINGSVERSION)
        if self.settingsVersion <= 1:
            self.settingsVersion = 3
            self.imageKeys.update({Qt.Key_4: "rotateLeft", Qt.Key_6: "rotateRight"})
            # Version 3 adds new entries so no update required
        self.settingsVersion = CURRENTSETTINGSVERSION
        self.save(size, pos)
