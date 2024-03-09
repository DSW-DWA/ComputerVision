from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)


class ChannelExchangeDialog(QDialog):
    channelChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Color Channel Swap")

        self.initUI()
        self.setupConnections()

    def initUI(self):
        # Radio Buttons for Source Color Channel
        self.sourceLabel = QLabel("Source Channel:")
        self.blueRadioButton = QRadioButton("Blue")
        self.redRadioButton = QRadioButton("Red")
        self.greenRadioButton = QRadioButton("Green")
        self.blueRadioButton.setChecked(True)  # Setting Blue as default

        # Radio Buttons for Destination Color Channel
        self.destinationLabel = QLabel("Destination Channel:")
        self.blueDestRadioButton = QRadioButton("Blue")
        self.redDestRadioButton = QRadioButton("Red")
        self.greenDestRadioButton = QRadioButton("Green")
        self.greenDestRadioButton.setChecked(True)  # Setting Green as default

        # Кнопки
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(self.sourceLabel)
        layout.addWidget(self.blueRadioButton)
        layout.addWidget(self.redRadioButton)
        layout.addWidget(self.greenRadioButton)

        layout.addWidget(self.destinationLabel)
        layout.addWidget(self.blueDestRadioButton)
        layout.addWidget(self.redDestRadioButton)
        layout.addWidget(self.greenDestRadioButton)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.okButton)
        buttonsLayout.addWidget(self.cancelButton)

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def setupConnections(self):
        # Connect radio buttons to signal
        self.blueRadioButton.toggled.connect(
            lambda: (
                self.channelChanged.emit("Blue", self.getDestinationChannel())
                if self.blueRadioButton.isChecked()
                else None
            )
        )
        self.redRadioButton.toggled.connect(
            lambda: (
                self.channelChanged.emit("Red", self.getDestinationChannel())
                if self.redRadioButton.isChecked()
                else None
            )
        )
        self.greenRadioButton.toggled.connect(
            lambda: (
                self.channelChanged.emit("Green", self.getDestinationChannel())
                if self.greenRadioButton.isChecked()
                else None
            )
        )

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def getDestinationChannel(self):
        if self.blueDestRadioButton.isChecked():
            return "Blue"
        elif self.redDestRadioButton.isChecked():
            return "Red"
        elif self.greenDestRadioButton.isChecked():
            return "Green"
