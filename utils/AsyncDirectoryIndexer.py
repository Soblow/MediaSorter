"""
AsyncDirectoryIndexer

Brings the ASyncDirectoryIndexer module
"""

import logging
import math
import multiprocessing
import os
import queue
import time
from PyQt5.QtCore import QMimeDatabase, QByteArray

import utils.fileUtils as fsUtils
from utils.MediaEntry import MediaEntry


class AsyncDirectoryIndexer:
    """
    Class allowing asynchronous indexing of directories
    """
    stopKeyword = "STOP"
    prefix = "indexWorker"

    def __init__(self, threads: int = -1):
        if threads != -1:
            self.threads = threads
        else:
            self.threads = max(math.ceil(len(os.sched_getaffinity(0))/2), 1)
        self.outputQueue = multiprocessing.Queue()
        self.inputQueue = multiprocessing.Queue()
        self.shutdownEvent = multiprocessing.Event()
        self.indexedCount = 0
        self.totalCount = 0
        self.rez = None
        self.recursive = False
        self.folderFiles = []
        self.mimeTypes = []
        logging.debug("Created AsyncDirectoryIndexer")

    def indexWorker(self, inQueue: multiprocessing.Queue, outQueue: multiprocessing.Queue, mimeTypes: list[QByteArray], timeout: float = 0.1):
        logging.debug("indexWorker process started")
        db = QMimeDatabase()
        while not self.shutdownEvent.is_set():
            try:
                item = inQueue.get(block=True, timeout=timeout)
                if item != self.stopKeyword:
                    outQueue.put(fsUtils.indexFile(item, mimeTypes, db))
            except queue.Empty:
                continue

            if item == self.stopKeyword:
                break
        logging.debug("indexWorker process exited")

    def startProcess(self):
        for i in range(self.threads):
            multiprocessing.Process(target=self.indexWorker, name=self.prefix + str(i), args=(self.inputQueue, self.outputQueue, self.mimeTypes, 0.5)).start()

    def stopProcess(self, finishTasks: bool = False):
        if not finishTasks:
            self.emptyTasks()
        while not self.inputQueue.empty():
            logging.debug("waiting for indexer processes to stop")
            time.sleep(0.5)
        self.shutdownEvent.set()
        self.cleanUp()

    def emptyTasks(self):
        item = True
        while item:
            try:
                item = self.inputQueue.get(block=False)
            except queue.Empty:
                break

    def cleanUp(self):
        self.emptyTasks()
        self.inputQueue.close()
        self.inputQueue.join_thread()
        self.inputQueue = None
        self.outputQueue.close()
        self.outputQueue.join_thread()
        self.outputQueue = None

    def asyncIndex(self, path: str, matchingMime: list[QByteArray], recursive=False) -> bool:
        if not os.path.exists(path):
            logging.warning("Unable to start indexing, the folder doesn't exist")
            return False

        self.recursive = recursive
        self.folderFiles: list[str] = []
        self.outputQueue = multiprocessing.Queue()
        self.inputQueue = multiprocessing.Queue()
        self.shutdownEvent = multiprocessing.Event()
        self.totalCount = 0
        self.indexedCount = 0

        self.mimeTypes = matchingMime
        self.startProcess()
        folderList = [path]
        while len(folderList) > 0:
            p = folderList.pop()
            for e in os.scandir(p):
                pa = e.path
                if e.is_file():
                    self.totalCount += 1
                    self.folderFiles.append(pa)
                    self.inputQueue.put(pa)
                elif self.recursive:
                    folderList.append(pa)

        return True

    def get(self) -> MediaEntry | None:
        if self.outputQueue.empty():
            return None
        a = self.outputQueue.get()
        self.indexedCount += 1
        return a

    def getBulk(self, maxItems: int = 5) -> list[MediaEntry] | None:
        if self.outputQueue.empty():
            return None
        rez = []
        itemCount = 0
        while itemCount < maxItems:
            item = self.get()
            if item is None:
                break
            itemCount += 1
            rez.append(item)
        return rez

    def getBulkTimed(self, timeLimit: int = 0.5) -> list[MediaEntry] | None:
        if self.outputQueue.empty():
            return None
        rez = []
        curTime = time.monotonic()
        finalTime = curTime + timeLimit
        while time.monotonic() < finalTime:
            item = self.getBulk(10)
            if item is None:
                break
            rez += item
        return rez

    def progress(self) -> tuple[int, int]:
        return self.indexedCount, self.totalCount
