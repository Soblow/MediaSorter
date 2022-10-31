"""
SettingsDialog

Module providing a dialog window to modify MediaSorter's settings
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, \
    QDoubleSpinBox, QCheckBox, QComboBox, QFormLayout, QGroupBox

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
        self.layoutGlobalGlobal = QFormLayout()
        self.widgetIndexing = QGroupBox("Indexing")
        self.layoutIndexing = QFormLayout()
        self.widgetImage = QWidget()
        self.layoutImage = QFormLayout()
        self.widgetVideo = QWidget()
        self.layoutVideo = QFormLayout()

        self.global_historyLength = QSpinBox()
        self.global_autosort = QCheckBox()
        self.global_sort_method = QComboBox()
        self.global_indexing_async = QCheckBox()
        self.global_indexing_threads = QSpinBox()
        self.global_indexing_refreshPeriod = QSpinBox()
        self.global_indexing_batchSize = QSpinBox()
        self.global_indexing_batchTime = QCheckBox()
        self.global_indexing_batchTimeLimit = QDoubleSpinBox()
        self.global_indexing_recursive = QCheckBox()

        self.video_volume = QSpinBox()
        self.video_autoplay = QCheckBox()

        self.initUI()

    def initUI(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainWidget.addTab(self.widgetGlobal, "Global")
        self.mainWidget.addTab(self.widgetImage, "ImageSorter")
        self.mainWidget.addTab(self.widgetVideo, "VideoSorter")
        self.widgetGlobal.setLayout(self.layoutGlobal)
        self.widgetIndexing.setLayout(self.layoutIndexing)
        self.widgetImage.setLayout(self.layoutImage)
        self.widgetVideo.setLayout(self.layoutVideo)
        self.layoutGlobal.addLayout(self.layoutGlobalGlobal)
        self.layoutGlobal.addWidget(self.widgetIndexing)

        self.layoutGlobalGlobal.addRow("Undo/Redo history length", self.global_historyLength)
        self.layoutGlobalGlobal.addRow("Auto-sort list when indexing completes (default: False)", self.global_autosort)
        self.layoutGlobalGlobal.addRow("Select sorting method (default: none)", self.global_sort_method)
        self.layoutIndexing.addRow("Use Async indexing, highly recommended especially on slow storage/huge folders ("
                                 "Default: True)", self.global_indexing_async)
        self.layoutIndexing.addRow("Set amount of threads for async indexing (-1/0 means half available cores)",
                                 self.global_indexing_threads)
        self.layoutIndexing.addRow("Set indexing refresh period (default: 50ms)", self.global_indexing_refreshPeriod)
        self.layoutIndexing.addRow("Set batching size for indexing (default: 50 items)", self.global_indexing_batchSize)
        self.layoutIndexing.addRow("Enable/Disable batching limit on time rather than amount (default: False)",
                                 self.global_indexing_batchTime)
        self.layoutIndexing.addRow("Set batching time limit (default: 0.5s)", self.global_indexing_batchTimeLimit)
        self.layoutIndexing.addRow("Index recursively (default: False)", self.global_indexing_recursive)

        self.layoutVideo.addRow("Video volume", self.video_volume)
        self.layoutVideo.addRow("Auto-play videos", self.video_autoplay)

        self.buttonLayout.addWidget(self.validateButton)
        self.buttonLayout.addWidget(self.cancelButton)

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
        self.global_sort_method.addItem("creation date (increasing)", SortMethod.creatDate)
        self.global_sort_method.addItem("creation date (decreasing)", SortMethod.creatDateDec)
        self.global_sort_method.addItem("modification date (increasing)", SortMethod.modifDate)
        self.global_sort_method.addItem("modification date (decreasing)", SortMethod.modifDateDec)

        self.video_volume.setMinimum(0)
        self.video_volume.setMaximum(100)

        self.cancelButton.clicked.connect(self.reject)
        self.validateButton.clicked.connect(self.accept)

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

        self.video_volume.setValue(self.settings.volume)
        self.video_autoplay.setChecked(self.settings.video_autoplay)

    def accept(self) -> None:
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

        self.settings.volume = self.video_volume.value()
        self.settings.video_autoplay = self.video_autoplay.isChecked()
        super().accept()
