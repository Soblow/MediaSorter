"""
fileUtils

Module providing lots of functions related to file manipulation, mimetypes, etc...
"""
import logging
import os
import uuid
import shutil

from PyQt5.QtCore import QDir, QMimeDatabase, QFile, QByteArray
from PyQt5.QtWidgets import QWidget, QFileDialog

from utils.MediaEntry import MediaEntry
from utils.UndoRedo import HistoryEntry


def listFiles(path: str, matchingMime: list) -> list[MediaEntry]:
    filters = matchingMime
    if filters is None:
        logging.warning("Calling listFiles without a matchingMime argument will return an empty list")
        return []
    result = []
    myFiles: list[str] = QDir(path).entryList(filters=(QDir.Files | QDir.NoDotAndDotDot))

    for e in myFiles:
        fullpath = path + "/" + e
        entry = indexFile(fullpath, filters, QMimeDatabase())
        if entry:
            result.append(entry)

    return result


def indexFile(fileInfo: str, filters: list[QByteArray], db: QMimeDatabase) -> MediaEntry | None:
    fileType = db.mimeTypeForFile(fileInfo).name()
    # magic.from_file(fullpath, mime=True)
    if fileType in filters:
        media = MediaEntry()
        media.path = fileInfo
        media.mime = fileType
        return media
    return None


def getRandomName(path: str) -> str:
    randomPath = uuid.uuid4().hex
    splitText = os.path.splitext(path)
    return splitText[0] + "-" + randomPath + splitText[1]


def deleteFile(original: str) -> HistoryEntry | None:
    if not os.path.exists(original):
        logging.warning("Source (%s) doesn't exist", original)
        return None

    result, newFilename = QFile.moveToTrash(original)
    if not result:
        return None

    hist = HistoryEntry()
    hist.action = "move"
    hist.oldPath = original
    hist.newPath = newFilename
    return hist


def moveFile(original: str, newDirectory: str) -> HistoryEntry | None:
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

    hist = HistoryEntry()
    hist.action = "move"
    hist.oldPath = original
    hist.newPath = newFilename
    return hist


def copyFile(original: str, newDirectory: str) -> HistoryEntry | None:
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

    hist = HistoryEntry()
    hist.action = "copy"
    hist.oldPath = original
    hist.newPath = newFilename
    return hist


def deleteCopyFile(original: str, newFilename: str) -> HistoryEntry | None:
    if not os.path.exists(newFilename):
        logging.warning("File (%s) doesn't exist", newFilename)
        return None
    os.remove(newFilename)
    splitText = os.path.split(newFilename)

    hist = HistoryEntry()
    hist.action = "delete_copy"
    hist.oldPath = original
    hist.newPath = splitText[0]
    return hist


def chooseDirectory(parent: QWidget) -> tuple[bool, str]:
    dialog = QFileDialog(parent)
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    rez = dialog.exec()
    return (rez == 1), str(dialog.selectedFiles()[0])
