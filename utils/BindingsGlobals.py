"""
BindingsGlobals

Module providing description of different bindings actions
"""
import enum
import json
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

CURRENTBINDINGSVERSION = 2


class SorterAction:
    """Basic Action, parent class for all other actions"""
    name = "none"

    def __init__(self):
        self.path = ""
        self.keystr = ""

    def unserialize(self, a: dict):
        self.path = a["path"]
        self.keystr = a["keystr"]

    def __repr__(self):
        return f"SorterAction{{name: {self.name}; path: {self.path}; keystr: {self.keystr}}}"


class Move_SorterAction(SorterAction):
    """Move Action, allows to move files"""
    name = "move"


class Copy_SorterAction(SorterAction):
    """Copy Action, allows to copy files"""
    name = "copy"


AVAILABLESORTERACTIONS = {SorterAction.name: SorterAction,
                          Move_SorterAction.name: Move_SorterAction,
                          Copy_SorterAction.name: Copy_SorterAction}

def serializeAction(a: SorterAction) -> dict:
    rez = {"name": a.name, "data": a.__dict__}
    return rez


def deserializeAction(j: dict) -> SorterAction:
    a = AVAILABLESORTERACTIONS[j["name"]]()
    a.unserialize(j["data"])
    return a


def saveBindings(path: str, bindings: dict[int, SorterAction]):
    logging.info("Writing configuration to %s", path)
    serializedbindings = {}
    for e in bindings.keys():
        serializedbindings[e] = serializeAction(bindings[e])
    configFileContent = {'bindings': serializedbindings, 'version': CURRENTBINDINGSVERSION}
    with open(path, "w", encoding="us-ascii") as file:
        json.dump(configFileContent, file)


def loadBindings(path: str) -> dict[int, SorterAction]:
    logging.info("Loading configuration from %s", path)
    configFileContent = None
    with open(path, 'r', encoding="us-ascii") as configFile:
        configFileContent = json.load(configFile)
    if configFileContent is None:
        return {}

    # If version is lower than current, update then recursively call us
    if ("version" not in configFileContent) or (configFileContent["version"] < CURRENTBINDINGSVERSION):
        updateBindings(path, configFileContent)
        return loadBindings(path)

    deserializedBindings = {}
    for e in configFileContent["bindings"].keys():
        deserializedBindings[int(e)] = deserializeAction(configFileContent["bindings"][e])
    return deserializedBindings


def updateBindings(path: str, content: dict):
    if "version" not in content:
        # Config from before we added "version", time for a conversion to new format
        content["bindings"] = {}
        for k in content["keys"]:
            entry = content["keys"][k]
            newAction = SorterAction()
            if entry["action"] == "move":
                newAction = Move_SorterAction()
                newAction.path = entry["path"]
            elif entry["action"] == "copy":
                newAction = Copy_SorterAction()
                newAction.path = entry["path"]
            newAction.keystr = QKeySequence(Qt.Key(k)).toString()
            content["bindings"][int(k)] = newAction
        content["version"] = 1
    if content["version"] == 1:
        # Dummy version bump
        content["version"] = CURRENTBINDINGSVERSION
    logging.info("Upgraded config to version %s", CURRENTBINDINGSVERSION)
    saveBindings(path, content["bindings"])
