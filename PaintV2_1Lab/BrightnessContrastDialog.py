from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSlider,
    QVBoxLayout,
)


class BrightnessContrastDialog(QDialog):
    brightnessChanged = pyqtSignal(int)
    contrastChanged = pyqtSignal(int)
    channelChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adjust Brightness, Contrast, and Color Channels")

        self.initUI()
        self.setupConnections()

    def initUI(self):
        # Яркость
        self.brightnessSlider = QSlider(Qt.Orientation.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessLabel = QLabel("Brightness: 0")

        # Radio Buttons for Color Channels
        self.blueRadioButton = QRadioButton("Blue")
        self.redRadioButton = QRadioButton("Red")
        self.greenRadioButton = QRadioButton("Green")
        self.blueRadioButton.setChecked(True)  # Setting Blue as default

        # Контраст
        self.contrastSlider = QSlider(Qt.Orientation.Horizontal)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastLabel = QLabel("Contrast: 0")

        # Кнопки
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.resetButton = QPushButton("Reset")

        layout = QVBoxLayout()
        layout.addWidget(self.brightnessLabel)
        layout.addWidget(self.brightnessSlider)

        layout.addWidget(self.blueRadioButton)
        layout.addWidget(self.redRadioButton)
        layout.addWidget(self.greenRadioButton)

        layout.addWidget(self.contrastLabel)
        layout.addWidget(self.contrastSlider)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.okButton)
        buttonsLayout.addWidget(self.cancelButton)
        buttonsLayout.addWidget(self.resetButton)

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def createColorChannelSlider(self, label, min_value, max_value, default_value):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(default_value)
        return slider

    def setupConnections(self):
        self.brightnessSlider.valueChanged.connect(
            lambda: self.updateLabel(self.brightnessLabel, "Brightness", self.brightnessSlider.value())
        )
        self.contrastSlider.valueChanged.connect(
            lambda: self.updateLabel(self.contrastLabel, "Contrast", self.contrastSlider.value())
        )

        self.brightnessSlider.valueChanged.connect(self.brightnessChanged.emit)
        self.contrastSlider.valueChanged.connect(self.contrastChanged.emit)

        # Connect radio buttons to signal
        self.blueRadioButton.toggled.connect(
            lambda: self.channelChanged.emit("Blue") if self.blueRadioButton.isChecked() else None
        )
        self.redRadioButton.toggled.connect(
            lambda: self.channelChanged.emit("Red") if self.redRadioButton.isChecked() else None
        )
        self.greenRadioButton.toggled.connect(
            lambda: self.channelChanged.emit("Green") if self.greenRadioButton.isChecked() else None
        )

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.resetButton.clicked.connect(self.resetValues)
        self.channelChanged.connect(self.getActiveRadioButton)
        self.resetButton.clicked.connect(self.resetValues)

    def updateLabel(self, label, prefix, value, isPercentage=False):
        label.setText(f"{prefix}: {value}{'%' if isPercentage else ''}")

    def getActiveRadioButton(self):
        if self.blueRadioButton.isChecked():
            return "b"
        elif self.redRadioButton.isChecked():
            return "r"
        elif self.greenRadioButton.isChecked():
            return "g"

    def resetValues(self):
        self.brightnessSlider.setValue(0)
        self.contrastSlider.setValue(0)
        self.blueRadioButton.setChecked(True)
