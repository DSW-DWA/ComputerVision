from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class BrightnessContrastDialog(QDialog):
    brightnessChanged = pyqtSignal(int)
    contrastChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Отрегулируйте яркость и контрастность")

        # Создаем виджеты
        self.initUI()
        # Настраиваем соединения
        self.setupConnections()

    def initUI(self):
        # Яркость
        self.brightnessSlider = QSlider(Qt.Orientation.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessLabel = QLabel("Brightness: 0")

        # Контраст
        self.contrastSlider = QSlider(Qt.Orientation.Horizontal)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastLabel = QLabel("Contrast: 0")

        # Кнопки
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")

        # Размещаем элементы
        layout = QVBoxLayout()
        layout.addWidget(self.brightnessLabel)
        layout.addWidget(self.brightnessSlider)
        layout.addWidget(self.contrastLabel)
        layout.addWidget(self.contrastSlider)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.okButton)
        buttonsLayout.addWidget(self.cancelButton)

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def setupConnections(self):
        self.brightnessSlider.valueChanged.connect(self.updateBrightnessLabel)
        self.contrastSlider.valueChanged.connect(self.updateContrastLabel)
        self.brightnessSlider.valueChanged.connect(self.brightnessChanged.emit)
        self.contrastSlider.valueChanged.connect(self.contrastChanged.emit)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def updateBrightnessLabel(self, value):
        self.brightnessLabel.setText(f"Brightness: {value}")

    def updateContrastLabel(self, value):
        self.contrastLabel.setText(f"Contrast: {value}")

    def values(self):
        return self.brightnessSlider.value(), self.contrastSlider.value()