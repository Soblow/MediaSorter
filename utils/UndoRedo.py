"""
This module provides utilities & common classes for the Undo/Redo features
"""


class HistoryEntry:
    """
    This class provides basic description of an undo/redoable action
    """
    def __init__(self):
        self.action = None
        self.entry = None
        self.position = None
        self.oldPath = None
        self.newPath = None
