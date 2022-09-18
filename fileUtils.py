"""
fileUtils

Module providing lots of functions related to file manipulation, mimetypes, etc...
"""
import logging
import os
import uuid
import shutil

from PyQt5.QtCore import QDir, QMimeDatabase
from PyQt5.QtWidgets import QWidget, QFileDialog

ANIMATEDFORMATS = ["image/gif", "image/webp"]


def defaultFilters() -> set[str]:
    return {"image/png", "image/jpg"}


def listFiles(path: str, matchingMime: list = None) -> list[dict]:
    filters = matchingMime
    if filters is None:
        filters = defaultFilters()
    result = []
    myFiles: list[str] = QDir(path).entryList(filters=(QDir.Files | QDir.NoDotAndDotDot))

    for e in myFiles:
        fullpath = path + "/" + e
        entry = indexFile(fullpath, filters, QMimeDatabase())
        if entry:
            result.append(entry)

    return result


def indexFile(fileInfo: str, filters: list, db: QMimeDatabase) -> dict | None:
    fileType = db.mimeTypeForFile(fileInfo).name()
    # magic.from_file(fullpath, mime=True)
    if fileType in filters:
        return {"path": fileInfo, "mime": fileType}
    return None


def getRandomName(path: str) -> str:
    randomPath = uuid.uuid4().hex
    splitText = os.path.splitext(path)
    return splitText[0] + "-" + randomPath + splitText[1]


def moveFile(original: str, newDirectory: str) -> dict | None:
    if not os.path.isdir(newDirectory):
        logging.warning("Destination (%s) doesn't exist", newDirectory)
        return None
    if not os.path.exists(original):
        logging.warning("Source (%s) doesn't exist", original)
        return None
    splitText = os.path.split(original)
    newFilename = newDirectory + "/" + splitText[1]
    if os.path.exists(newFilename):
        randomName = getRandomName(splitText[1])
        while os.path.exists(newDirectory + "/" + randomName):
            randomName = getRandomName(splitText[1])
        newFilename = newDirectory + "/" + randomName
    # Using shutil to work between FS if needed
    shutil.move(original, newFilename)
    return {"action": "move", "oldpath": original, "newpath": newFilename}


def copyFile(original: str, newDirectory: str) -> dict | None:
    if not os.path.isdir(newDirectory):
        logging.warning("Destination (%s) doesn't exist", newDirectory)
        return None
    if not os.path.exists(original):
        logging.warning("Source (%s) doesn't exist", original)
        return None
    splitText = os.path.split(original)
    newFilename = os.path.join(newDirectory, splitText[1])
    if os.path.exists(newFilename):
        randomName = getRandomName(splitText[1])
        while os.path.exists(os.path.join(newDirectory, randomName)):
            randomName = getRandomName(splitText[1])
        newFilename = os.path.join(newDirectory, randomName)
    # Using copy2 to preserve metadata
    shutil.copy2(original, newFilename)
    return {"action": "copy", "oldpath": original, "newpath": newFilename}


def deleteFile(original: str, newFilename: str) -> dict | None:
    if not os.path.exists(newFilename):
        logging.warning("File (%s) doesn't exist", newFilename)
        return None
    os.remove(newFilename)
    splitText = os.path.split(newFilename)
    return {"action": "delete_copy", "oldpath": original, "newpath": splitText[0]}


def chooseDirectory(parent: QWidget) -> tuple[bool, str]:
    dialog = QFileDialog(parent)
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    rez = dialog.exec()
    return (rez == 1), str(dialog.selectedFiles()[0])
