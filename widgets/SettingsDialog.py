"""
SettingsDialog

Module providing a dialog window to modify MediaSorter's settings
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel, \
    QDoubleSpinBox, QCheckBox, QComboBox

from utils.Settings import Settings, SortMethod


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
        self.global_indexing_async = QCheckBox()
        self.global_indexing_threads = QSpinBox()
        self.global_indexing_refreshPeriod = QSpinBox()
        self.global_indexing_batchSize = QSpinBox()
        self.global_indexing_batchTime = QCheckBox()
        self.global_indexing_batchTimeLimit = QDoubleSpinBox()
        self.global_indexing_recursive = QCheckBox()
        self.global_autosort = QCheckBox()
        self.global_sort_method = QComboBox()

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
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Use Async indexing, highly recommended especially on slow storage/huge folders (Default: True)"))
        layout.addWidget(self.global_indexing_async)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Set amount of threads for async indexing (-1/0 means half available cores)"))
        layout.addWidget(self.global_indexing_threads)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Set indexing refresh period (default: 50ms)"))
        layout.addWidget(self.global_indexing_refreshPeriod)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Set batching size for indexing (default: 50 per call)"))
        layout.addWidget(self.global_indexing_batchSize)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Enable/Disable batching limit on time rather than amount (default: False)"))
        layout.addWidget(self.global_indexing_batchTime)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Set batching time limit (default: 0.5s)"))
        layout.addWidget(self.global_indexing_batchTimeLimit)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Index recursively (default: False)"))
        layout.addWidget(self.global_indexing_recursive)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Auto-sort list when indexing completes (default: False)"))
        layout.addWidget(self.global_autosort)
        layout = QHBoxLayout()
        self.layoutGlobal.addLayout(layout)
        layout.addWidget(QLabel("Select sorting method (default: none)"))
        layout.addWidget(self.global_sort_method)

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
        self.global_indexing_threads.setMinimum(-1)
        self.global_indexing_threads.setMaximum(100)
        self.global_indexing_refreshPeriod.setMinimum(5)
        self.global_indexing_refreshPeriod.setMaximum(1000)
        self.global_indexing_batchSize.setMinimum(1)
        self.global_indexing_batchSize.setMaximum(10000)
        self.global_indexing_batchTimeLimit.setMinimum(0.01)
        self.global_indexing_batchTimeLimit.setMaximum(1.0)
        self.global_sort_method.addItem("none", SortMethod.none)
        self.global_sort_method.addItem("name (alphabetical)", SortMethod.name)
        self.global_sort_method.addItem("name (reverse)", SortMethod.nameRev)
        self.global_sort_method.addItem("size (increasing)", SortMethod.size)
        self.global_sort_method.addItem("size (decreasing)", SortMethod.sizeDec)

        self.cancelButton.clicked.connect(self.reject)
        self.validateButton.clicked.connect(self.accept)

        self.video_volume.setValue(self.settings.volume)
        self.global_historyLength.setValue(self.settings.historyLength)
        self.global_indexing_async.setChecked(self.settings.indexing_async)
        self.global_indexing_threads.setValue(self.settings.indexing_threads)
        self.global_indexing_refreshPeriod.setValue(self.settings.indexing_refreshPeriod)
        self.global_indexing_batchSize.setValue(self.settings.indexing_batchSize)
        self.global_indexing_batchTime.setChecked(self.settings.indexing_batchTime)
        self.global_indexing_batchTimeLimit.setValue(self.settings.indexing_batchTimeLimit)
        self.global_indexing_recursive.setChecked(self.settings.indexing_recursive)
        self.global_autosort.setChecked(self.settings.autosort)
        self.global_sort_method.setCurrentIndex(self.settings.sort_method.value)

    def accept(self) -> None:
        self.settings.volume = self.video_volume.value()
        self.settings.historyLength = self.global_historyLength.value()
        self.settings.indexing_async = self.global_indexing_async.isChecked()
        self.settings.indexing_threads = self.global_indexing_threads.value()
        self.settings.indexing_refreshPeriod = self.global_indexing_refreshPeriod.value()
        self.settings.indexing_batchSize = self.global_indexing_batchSize.value()
        self.settings.indexing_batchTime = self.global_indexing_batchTime.isChecked()
        self.settings.indexing_batchTimeLimit = self.global_indexing_batchTimeLimit.value()
        self.settings.indexing_recursive = self.global_indexing_recursive.isChecked()
        self.settings.autosort = self.global_autosort.isChecked()
        self.settings.sort_method = SortMethod(self.global_sort_method.currentIndex())
        super().accept()
