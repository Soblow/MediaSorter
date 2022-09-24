"""
SettingsDialog

Module providing a dialog window to modify MediaSorter's settings
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel

from utils.Settings import Settings


class SettingsDialog(QDialog):
    """
    This class provides the Dialow window with all the customizable options for MediaSorter
    """
    def __init__(self, settings: Settings, parent: QWidget = None, flags: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.settings = settings
        self.resize(QSize(800, 480))

        self.mainLayout = QVBoxLayout()
        self.mainWidget = QTabWidget()
        self.buttonLayout = QHBoxLayout()
        self.validateButton = QPushButton("Validate")
        self.cancelButton = QPushButton("Cancel")

        self.widgetGlobal = QWidget()
        self.layoutGlobal = QVBoxLayout()
        self.widgetImage = QWidget()
        self.layoutImage = QVBoxLayout()
        self.widgetVideo = QWidget()
        self.layoutVideo = QVBoxLayout()

        self.global_historyLength = QSpinBox()
        self.video_volume = QSpinBox()

        self.initUI()

    def initUI(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainWidget.addTab(self.widgetGlobal, "Global")
        self.mainWidget.addTab(self.widgetImage, "ImageSorter")
        self.mainWidget.addTab(self.widgetVideo, "VideoSorter")
        self.widgetGlobal.setLayout(self.layoutGlobal)
        self.widgetImage.setLayout(self.layoutImage)
        self.widgetVideo.setLayout(self.layoutVideo)

        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Undo/Redo history length"))
        layout.addWidget(self.global_historyLength)
        layout = QHBoxLayout()
        self.layoutVideo.addLayout(layout)
        layout.addWidget(QLabel("Video volume"))
        layout.addWidget(self.video_volume)

        self.buttonLayout.addWidget(self.validateButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.video_volume.setMinimum(0)
        self.video_volume.setMaximum(100)
        self.global_historyLength.setMinimum(5)
        self.global_historyLength.setMaximum(100)

        self.cancelButton.clicked.connect(self.reject)
        self.validateButton.clicked.connect(self.accept)

        self.video_volume.setValue(self.settings.volume)
        self.global_historyLength.setValue(self.settings.historyLength)

    def accept(self) -> None:
        self.settings.volume = self.video_volume.value()
        self.settings.historyLength = self.global_historyLength.value()
        super().accept()
