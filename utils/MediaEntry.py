"""
This module provides utilities & common classes for the Media handling
"""


class MediaEntry:
    """
    This class represents a Media entry in the media list, common to all types of media
    """
    def __init__(self):
        self.path = None
        self.mime = None

    def __lt__(self, other: "MediaEntry"):
        return self.path < other.path
