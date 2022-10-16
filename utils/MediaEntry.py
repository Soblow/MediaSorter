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

    def getSize(self) -> int:
        if self.size == -1:
            self.size = os.stat(self.path).st_size
        return self.size

    def __lt__(self, other: "MediaEntry"):
        return self.path < other.path
