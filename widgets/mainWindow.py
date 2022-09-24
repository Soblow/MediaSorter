#! /usr/bin/python3
"""
mainWindow

Module providing the base for creating a Sorter
imageSorter & videoSorter herit from this base class
"""

import copy
import json
import logging
import pickle
import math

from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QPoint, QByteArray, QCoreApplication
from PyQt5.QtGui import QKeySequence, QGuiApplication, QWheelEvent, QKeyEvent, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, \
    QAction, QTableWidget, QAbstractItemView, QTableWidgetItem, QFileDialog, QSplitter, QVBoxLayout, QWidget, QLabel, \
    QSizePolicy, QHBoxLayout, QMessageBox

from utils import fileUtils as fsUtils
from utils import AsyncDirectoryIndexer
from utils import BindingsGlobals
from utils.Settings import Settings
from utils.UndoRedo import HistoryEntry, doHistory
from widgets.QJumpWindow import QJumpWindow
from widgets.bindingsWindow import BindingsWindow


class MainWindow(QMainWindow):
    """
    Base class for Sorters. They provide common features of other sorters.

    This is a virtual class, some features aren't implemented and will raise NotImplemented exceptions
    """

    def __init__(self, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, flags)

        QCoreApplication.setOrganizationName("OrganizationName")
        QCoreApplication.setApplicationName("MediaSorter")
        self.settings = Settings()
        # logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
        logging.getLogger().setLevel(self.settings.logLevel)
        self.title = "MediaSorter"
        self.mediaListPosition = 0
        self.mediaList = []
        self.path = ".."
        self.configFilePath = ""
        self.eventsConfig = {"keys": {}}
        self.forbiddenKeys = [Qt.Key_Escape]
        self.forbiddenKeys += self.settings.globalKeys.keys()
        self.isActive = False
        self.nonexist = False
        self.undoHistory = []
        self.redoHistory = []
        self.origPos = None
        self.origHor = None
        self.origVer = None

        self.fileMenu = self.menuBar().addMenu("File")
        self.actionMenu = self.menuBar().addMenu("Action")
        self.helpMenu = self.menuBar().addMenu("Help")
        self.openDirectoryAction = QAction("Open Directory")
        self.saveDirectoryIndexAction = QAction("Save Directory Index")
        self.openDirectoryIndexAction = QAction("Open Directory Index")
        self.openConfigAction = QAction("Open Config")
        self.newConfigAction = QAction("New Config")
        self.reloadAction = QAction("Reload")
        self.quitAction = QAction("Quit")
        self.undoAction = QAction("Undo")
        self.redoAction = QAction("Redo")
        self.jumpToAction = QAction("Jump To")
        self.editConfigAction = QAction("Edit config")
        self.aboutAction = QAction("About")
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QWidget()
        self.myWidget = QSplitter(Qt.Horizontal)
        self.actionLayout = QVBoxLayout()
        self.actionWidget = QWidget()
        self.fileNameLabel = QLabel("Current file : None")
        self.actionsAvailable = QTableWidget(1, 2, self)
        self.progressionLabel = QLabel("0/0")
        self.bottomLayout = QHBoxLayout()

        self.clipboard = QGuiApplication.clipboard()

        self.asyncIndexer = AsyncDirectoryIndexer.AsyncDirectoryIndexer()
        self.asyncIndexerTimer = QTimer()

        # initUI will be called on herited classes

    def initUI(self):
        # Main window params
        self.setWindowTitle(self.title)

        size, pos = self.settings.restore()
        self.resize(size)
        self.move(pos)

        self.fileMenu.addAction(self.openDirectoryAction)
        self.fileMenu.addAction(self.saveDirectoryIndexAction)
        self.fileMenu.addAction(self.openDirectoryIndexAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openConfigAction)
        self.fileMenu.addAction(self.newConfigAction)
        self.fileMenu.addAction(self.reloadAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        self.actionMenu.addAction(self.undoAction)
        self.actionMenu.addAction(self.redoAction)
        self.actionMenu.addSeparator()
        self.actionMenu.addAction(self.jumpToAction)
        self.actionMenu.addSeparator()
        self.actionMenu.addAction(self.editConfigAction)
        self.helpMenu.addAction(self.aboutAction)

        self.quitAction.triggered.connect(self.close)
        self.reloadAction.triggered.connect(self.prepareMediaList)
        self.undoAction.triggered.connect(self.undo)
        self.redoAction.triggered.connect(self.redo)
        self.jumpToAction.triggered.connect(self.jumpTo)
        self.openDirectoryAction.triggered.connect(self.chooseDir)
        self.saveDirectoryIndexAction.triggered.connect(self.saveDirIndex)
        self.openDirectoryIndexAction.triggered.connect(self.loadDirIndex)
        self.openConfigAction.triggered.connect(self.chooseConfig)
        self.newConfigAction.triggered.connect(self.newConfig)
        self.aboutAction.triggered.connect(self.showAbout)
        self.myWidget.splitterMoved.connect(self.splitterMovedEvent)
        self.editConfigAction.triggered.connect(self.editConfig)

        self.setCentralWidget(self.mainWidget)
        self.actionWidget.setLayout(self.actionLayout)
        self.actionLayout.addWidget(self.actionsAvailable)
        self.myWidget.addWidget(self.actionWidget)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.myWidget)
        self.mainLayout.addLayout(self.bottomLayout)
        self.bottomLayout.addWidget(self.fileNameLabel)
        self.bottomLayout.addWidget(self.progressionLabel)

        self.actionsAvailable.setSelectionMode(QAbstractItemView.NoSelection)
        self.actionsAvailable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.actionsAvailable.setFocusPolicy(Qt.NoFocus)
        self.actionsAvailable.setColumnWidth(0, 1)
        self.actionsAvailable.setColumnWidth(1, 500)

        self.fileNameLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.GrowFlag | QSizePolicy.ShrinkFlag)
        self.fileNameLabel.setWordWrap(True)
        self.progressionLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        self.progressionLabel.setAlignment(Qt.AlignRight)
        self.progressionLabel.setWordWrap(False)

        self.asyncIndexerTimer.timeout.connect(self.asyncPeriodicChecker)
        self.statusBar().showMessage("Ready.")

    def adjustSplitter(self):
        # Initial repartition of the screen : 35%/65%
        ttx = max(1, math.ceil(0.35 * self.myWidget.size().width()))
        tty = max(1, math.ceil(0.65 * self.myWidget.size().width()))
        self.myWidget.setSizes([ttx, tty])
        # self.myWidget.setSizes([math.ceil(self.sizeHint().width()*0.35), math.ceil(self.sizeHint().width()*0.65)])
        # self.myWidget.moveSplitter(math.ceil(self.myWidget.size().width()/3), 1)

    def prepareMediaList(self, _triggered: bool = False, path: str = None, matchingMime: list[QByteArray] = None):
        if path is not None:
            self.path = path
        self.mediaListPosition = 0
        self.mediaList = []
        self.emptyUndoRedo()
        self.updateCurrentMedia()
        self.isActive = False

        if self.asyncIndexer.asyncIndex(self.path, matchingMime):
            logging.debug("Asynchronous indexing started")
            self.statusBar().showMessage(f"Starting to index {self.path}.")
            self.asyncIndexerTimer.start(50)  # 50ms

    def asyncPeriodicChecker(self):
        progress = self.asyncIndexer.progress()
        newEntries = self.asyncIndexer.getBulk(50)
        if newEntries and len(newEntries) > 0:
            flag = (len(self.mediaList) == 0)
            self.mediaList += newEntries
            if flag:
                self.updateCurrentMedia()
                self.isActive = True
                logging.info("Asynchronous indexing found suitable files, activating the window")
            self.updateProgress()
        if progress[0] == progress[1]:
            self.statusBar().showMessage("Directory indexing has finished.")
            logging.debug("Asynchronous Indexing ended, stopping periodic check")
            self.asyncIndexerTimer.stop()
            self.asyncIndexer.stopProcess()

    def addNewUndo(self, action: HistoryEntry):
        self.redoHistory = []
        self.redoAction.setEnabled(False)
        self.undoHistory.append(action)
        self.undoAction.setEnabled(len(self.undoHistory) > 0)
        if len(self.undoHistory) > self.settings.historyLength:
            self.undoHistory.pop(0)

    def emptyUndoRedo(self):
        self.undoHistory = []
        self.redoHistory = []
        self.undoAction.setEnabled(False)
        self.redoAction.setEnabled(False)

    def undo(self):
        msg, self.mediaListPosition = doHistory(self.settings.historyLength, self.undoHistory, self.redoHistory, self.mediaList, self.mediaListPosition)
        self.statusBar().showMessage(f"Undo: {msg}.")
        self.updateProgress()
        self.updateCurrentMedia()
        self.undoAction.setEnabled(len(self.undoHistory) > 0)
        self.redoAction.setEnabled(len(self.redoHistory) > 0)

    def redo(self):
        msg, self.mediaListPosition = doHistory(self.settings.historyLength, self.redoHistory, self.undoHistory, self.mediaList, self.mediaListPosition)
        self.statusBar().showMessage(f"Redo: {msg}.")
        self.updateProgress()
        self.updateCurrentMedia()
        self.undoAction.setEnabled(len(self.undoHistory) > 0)
        self.redoAction.setEnabled(len(self.redoHistory) > 0)

    def setFileName(self, fileName: str, clean: bool = False):
        if not clean:
            fileName = "Current file : " + fileName
        self.fileNameLabel.setText(fileName)

    def chooseDir(self):
        rez = fsUtils.chooseDirectory(self)
        if rez[0]:
            self.path = str(rez[1])
            self.statusBar().showMessage(f"Opening directory {self.path}.")
            self.prepareMediaList()
            self.updateProgress()

    def saveDirIndex(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        rez = fileDialog.exec()
        if rez == 1:
            chosenFile = fileDialog.selectedFiles()[0]
            with open(chosenFile, 'wb') as f:
                pickle.dump((self.path, self.mediaList, self.mediaListPosition), f)
            logging.info("Saved directory index in %s", chosenFile)
            self.statusBar().showMessage(f"Saved directory index at {chosenFile}.")

    def loadDirIndex(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        rez = fileDialog.exec()
        if rez == 1:
            chosenFile = fileDialog.selectedFiles()[0]
            with open(chosenFile, 'rb') as f:
                (self.path, self.mediaList, self.mediaListPosition) = pickle.load(f)
            logging.info("Loaded directory index from %s", chosenFile)
            self.statusBar().showMessage(f"Loaded directory index from {chosenFile}.")
            self.mediaListPosition = 0
            self.updateCurrentMedia()
            self.isActive = True
            self.updateProgress()

    def chooseConfig(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        rez = dialog.exec()
        if rez == 1:
            chosenConfig = dialog.selectedFiles()[0]
            self.configFilePath = str(chosenConfig)
            self.statusBar().showMessage(f"Opening config from file {chosenConfig}.")
            self.openConfig()

    def newConfig(self):
        self.eventsConfig = {"keys": {}}
        self.actionsAvailable.setRowCount(1)
        self.actionsAvailable.clearContents()
        self.configFilePath = ""
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.AnyFile)
        if fileDialog.exec():
            self.configFilePath = fileDialog.selectedFiles()[0]
            self.statusBar().showMessage(f"Opening new config in file {self.configFilePath}.")
            logging.info("Opening new config in file %s", self.configFilePath)

    @pyqtSlot(str)
    def openConfig(self, newPath: str = None):
        if newPath is not None:
            self.configFilePath = newPath
        if self.configFilePath == "":
            return
        with open(self.configFilePath, 'r', encoding="us-ascii") as configFile:
            self.eventsConfig = json.load(configFile)
        self.actionsAvailable.clearContents()
        self.actionsAvailable.setRowCount(len(self.eventsConfig['keys'].keys()))
        i = 0
        for key in sorted(self.eventsConfig['keys'].keys()):
            entry = self.eventsConfig['keys'][key]
            self.actionsAvailable.setItem(i, 0, QTableWidgetItem(QKeySequence(Qt.Key(key)).toString()))
            newEntry = QTableWidgetItem("")
            newEntry.setText(f"{entry['action']} to {entry['path']}")
            self.actionsAvailable.setItem(i, 1, newEntry)
            i += 1
        self.actionsAvailable.resizeRowsToContents()

    def showAbout(self):
        _temp = QMessageBox.about(self, "About", "This project was made by Soblow. Available under license provided in LICENSE.md")

    def editConfig(self):
        _temp = BindingsWindow(self, copy.deepcopy(self.eventsConfig), self.configFilePath, self.forbiddenKeys)

    def jumpTo(self):
        _temp = QJumpWindow(self, maxNumber=len(self.mediaList), curPos=self.mediaListPosition + 1)

    def jumpToCallback(self, jump_id: int):
        self.statusBar().showMessage(f"Jumping to image number {jump_id}.")
        self.mediaListPosition = jump_id - 1
        self.updateProgress()
        self.updateCurrentMedia()

    def previous(self, move: bool = True):
        if move:
            self.mediaListPosition -= 1
        self.mediaListPosition = max(self.mediaListPosition, 0)
        if len(self.mediaList) == 0:
            self.isActive = False
        self.updateProgress()
        self.updateCurrentMedia()

    def next(self, move: bool = True):
        if move:
            self.mediaListPosition += 1
        if self.mediaListPosition >= len(self.mediaList):
            self.mediaListPosition = len(self.mediaList) - 1
        self.updateProgress()
        self.updateCurrentMedia()

    def homeKey(self):
        if self.isActive:
            self.mediaListPosition = 0
            self.updateProgress()
            self.updateCurrentMedia()

    def endKey(self):
        if self.isActive:
            self.mediaListPosition = len(self.mediaList) - 1
            self.updateProgress()
            self.updateCurrentMedia()

    def actDelete(self):
        if self.isActive:
            self.statusBar().showMessage(f"Deleting file {self.mediaList[self.mediaListPosition].path}.")
            newUndo = fsUtils.deleteFile(self.mediaList[self.mediaListPosition].path)
            if newUndo is not None:
                newUndo.position = self.mediaListPosition
                newUndo.entry = self.mediaList[self.mediaListPosition]
                self.addNewUndo(newUndo)
                self.mediaList.pop(self.mediaListPosition)
                self.next(move=False)
            else:
                self.statusBar().showMessage(f"Failed to delete file {self.mediaList[self.mediaListPosition].path}.")


    def moveFile(self, newDirectory: str):
        if self.isActive:
            self.statusBar().showMessage(f"Moving file to {newDirectory}.")
            newUndo = fsUtils.moveFile(self.mediaList[self.mediaListPosition].path, newDirectory)
            if newUndo is not None:
                newUndo.position = self.mediaListPosition
                newUndo.entry = self.mediaList[self.mediaListPosition]
                self.addNewUndo(newUndo)
                self.mediaList.pop(self.mediaListPosition)
                self.next(move=False)
            else:
                self.statusBar().showMessage(f"Failed to move file to {newDirectory}.")

    def copyFile(self, newDirectory: str):
        if self.isActive:
            self.statusBar().showMessage(f"Copying file to {newDirectory}.")
            newUndo = fsUtils.copyFile(self.mediaList[self.mediaListPosition].path, newDirectory)
            if newUndo is not None:
                newUndo.position = self.mediaListPosition
                self.addNewUndo(newUndo)
            else:
                self.statusBar().showMessage(f"Failed to copy file to {newDirectory}.")

    def hideFile(self):
        if self.isActive or self.nonexist:
            self.statusBar().showMessage("Removing file from list.")
            hist = HistoryEntry()
            hist.action = "hide"
            hist.entry = self.mediaList[self.mediaListPosition]
            hist.position = self.mediaListPosition
            self.addNewUndo(hist)
            self.mediaList.pop(self.mediaListPosition)
            self.next(move=False)

    def copyCurrentToClipboard(self):
        # Won't make it mandatory to implement if it isn't possible to put file in clipboard (videos...)
        logging.info("Copying to clipboard isn't available on this mode")

    def nothing(self):
        logging.info('"Nothing" callback was called, and it did nothing else than printing this message')

    def updateCurrentMedia(self):
        raise NotImplementedError()

    def updateProgress(self):
        self.progressionLabel.setText(f"{self.mediaListPosition + 1}/{len(self.mediaList)}")

    # def resizeEvent(self, event):
    # 	self.image.rescale()
    # 	event.accept()

    def zoom(self, factor: QPoint):
        raise NotImplementedError()

    def wheelEvent(self, event: QWheelEvent):
        self.zoom(event.angleDelta())
        event.accept()

    def splitterMovedEvent(self, _pos: int, _index: int):
        self.actionsAvailable.resizeRowsToContents()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.settings.save(self.size(), self.pos())
        super().closeEvent(a0)
        a0.accept()

    def keyPressEvent(self, event: QKeyEvent):
        # Note: Please note that events may also be handled by herited classes
        eventKey = event.key()
        logging.debug("mainWindow : Key pressed %s", eventKey)
        if eventKey == Qt.Key_Escape:
            self.close()
            event.accept()
        elif eventKey in self.settings.globalKeys:
            act = self.settings.globalKeys[eventKey]
            if act == "next":
                self.next()
            elif act == "prev":
                self.previous()
            elif act == "first":
                self.homeKey()
            elif act == "last":
                self.endKey()
            elif act == "delete":
                self.actDelete()
            elif act == "clipboard":
                self.copyCurrentToClipboard()
            elif act == "hide":
                self.hideFile()
            else:
                logging.error("Unsupported action from settings (%s). This should never happen", act)
            event.accept()
        elif (str(event.key()) in self.eventsConfig['keys']) and self.isActive:
            action = self.eventsConfig['keys'][str(event.key())]["action"]
            if BindingsGlobals.BindingActionType.fileModification in BindingsGlobals.bindingActions[action]:
                if action == "move":
                    self.moveFile(self.eventsConfig['keys'][str(event.key())]['path'])
                elif action == "copy":
                    self.copyFile(self.eventsConfig['keys'][str(event.key())]['path'])
            else:
                self.nothing()
            event.accept()
