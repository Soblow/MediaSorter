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
        self.size = -1

    def compareSize(self, other: "MediaEntry"):
        if self.size == -1:
            self.getSize()
        if other.size == -1:
            other.getSize()
        return self.size < other.size

    def getSize(self):
        self.size = os.stat(self.path).st_size

    def __lt__(self, other: "MediaEntry"):
        return self.path < other.path
