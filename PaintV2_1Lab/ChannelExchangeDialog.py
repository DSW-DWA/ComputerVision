from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)


class ChannelExchangeDialog(QDialog):
    channelChanged = pyqtSignal(str, str)  # Signal to emit channel changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Color Channel Exchange")

        self.initUI()
        self.setupConnections()

    def initUI(self):
        self.sourceLabel = QLabel("Source Channel:")
        self.destinationLabel = QLabel("Destination Channel:")

        self.redRadioButtonSource = QRadioButton("Red")
        self.greenRadioButtonSource = QRadioButton("Green")
        self.blueRadioButtonSource = QRadioButton("Blue")

        self.redRadioButtonDestination = QRadioButton("Red")
        self.greenRadioButtonDestination = QRadioButton("Green")
        self.blueRadioButtonDestination = QRadioButton("Blue")

        self.redRadioButtonSource.setChecked(True)  # Setting Red as default for source
        self.redRadioButtonDestination.setChecked(True)  # Setting Red as default for destination

        sourceLayout = QVBoxLayout()
        sourceLayout.addWidget(self.sourceLabel)
        sourceLayout.addWidget(self.redRadioButtonSource)
        sourceLayout.addWidget(self.greenRadioButtonSource)
        sourceLayout.addWidget(self.blueRadioButtonSource)

        destinationLayout = QVBoxLayout()
        destinationLayout.addWidget(self.destinationLabel)
        destinationLayout.addWidget(self.redRadioButtonDestination)
        destinationLayout.addWidget(self.greenRadioButtonDestination)
        destinationLayout.addWidget(self.blueRadioButtonDestination)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(sourceLayout)
        mainLayout.addLayout(destinationLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def setupConnections(self):
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        source_group = QButtonGroup(self)
        source_group.addButton(self.redRadioButtonSource)
        source_group.addButton(self.greenRadioButtonSource)
        source_group.addButton(self.blueRadioButtonSource)

        destination_group = QButtonGroup(self)
        destination_group.addButton(self.redRadioButtonDestination)
        destination_group.addButton(self.greenRadioButtonDestination)
        destination_group.addButton(self.blueRadioButtonDestination)

        source_group.buttonToggled.connect(self.emitChannelChange)
        destination_group.buttonToggled.connect(self.emitChannelChange)

    def emitChannelChange(self):
        source_channel = ""
        destination_channel = ""

        if self.redRadioButtonSource.isChecked():
            source_channel = "Red"
        elif self.greenRadioButtonSource.isChecked():
            source_channel = "Green"
        elif self.blueRadioButtonSource.isChecked():
            source_channel = "Blue"

        if self.redRadioButtonDestination.isChecked():
            destination_channel = "Red"
        elif self.greenRadioButtonDestination.isChecked():
            destination_channel = "Green"
        elif self.blueRadioButtonDestination.isChecked():
            destination_channel = "Blue"

        self.channelChanged.emit(source_channel, destination_channel)
