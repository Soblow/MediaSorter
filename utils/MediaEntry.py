"""
This module provides utilities & common classes for the Media handling
"""
import os


class MediaEntry:
    """
    This class represents a Media entry in the media list, common to all types of media
    """
    def __init__(self):
        self.path = None
        self.mime = None
        self.stat: os.stat_result = None

    def __stat__(self):
        if self.stat is None:
            self.stat = os.stat(self.path)

    def getModifDate(self):
        self.__stat__()
        return self.stat.st_mtime

    def getCreatDate(self):
        self.__stat__()
        return self.stat.st_ctime

    def getSize(self) -> int:
        self.__stat__()
        return self.stat.st_size

    def __lt__(self, other: "MediaEntry"):
        return self.path < other.path
