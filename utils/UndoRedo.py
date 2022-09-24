"""
This module provides utilities & common classes for the Undo/Redo features
"""

import copy
import os

from utils.MediaEntry import MediaEntry
import utils.fileUtils as fsUtils


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


def doHistory(historySize: int, history: list[HistoryEntry], otherHistory: list[HistoryEntry], mediaList: list[MediaEntry], mediaListPosition: int) -> tuple[str, int]:
    act_msg = "no action"
    newPos = mediaListPosition
    if len(history) > 0:
        previousAction = history.pop()
        newAction = copy.deepcopy(previousAction)
        # if "oldPos" in previousAction:
        #     newPos = previousAction.position

        if previousAction.action == "move":
            newAction = fsUtils.moveFile(previousAction.newPath, os.path.split(previousAction.oldPath)[0])
            if newAction is not None:
                # newAction.entry = previousAction.entry
                # newAction.position = previousAction.position
                act_msg = "move "+previousAction.oldPath
                # if os.path.exists(previousAction.entry["path"]):
                #     mediaList.insert(previousAction.position, previousAction.entry)
                # else:
                #     mediaList.pop(mediaListPosition)
                #     newPos = mediaListPosition
        elif previousAction.action == "copy":
            newAction = fsUtils.deleteCopyFile(previousAction.oldPath, previousAction.newPath)
            if newAction is not None:
                act_msg = "copy "+previousAction.oldPath
        elif previousAction.action == "delete_copy":
            newAction = fsUtils.copyFile(previousAction.oldPath, previousAction.newPath)
            if newAction is not None:
                act_msg = "delete_copy "+previousAction.oldPath
        elif previousAction.action == "hide":
            newAction = None
            act_msg = "hide "+previousAction.entry.path
            mediaList.insert(previousAction.position, previousAction.entry)
            newPos = min(previousAction.position, len(mediaList)+1)
        if newAction is not None:
            otherHistory.append(newAction)
        if len(otherHistory) > historySize:
            otherHistory.pop(0)
    return act_msg, newPos
