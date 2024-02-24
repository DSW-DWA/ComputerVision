import sys

import cv2
import numpy as np
from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QAction, QColor, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ImageEditor(QMainWindow):
    layout: QVBoxLayout
    currentFilePath: str

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint v0")
        self.setGeometry(100, 100, 800, 600)
        self.centerWindow()

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.layout = QVBoxLayout()
        self.mainWidget.setLayout(self.layout)

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.imageLabel)

        self.histogramLayout = QHBoxLayout()
        self.layout.addLayout(self.histogramLayout)

        self.createActions()
        self.createButtons()

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.openImage)
        self.saveAct = QAction("&Save As...", self, shortcut="Ctrl+S", triggered=self.saveImage)

    def createButtons(self):
        self.openButton = QPushButton("&Open...")
        self.openButton.clicked.connect(self.openImage)
        self.layout.addWidget(self.openButton)

        self.saveButton = QPushButton("&Save As...")
        self.saveButton.clicked.connect(self.saveImage)
        self.layout.addWidget(self.saveButton)

        self.analyzeButton = QPushButton("&Analyze Image")
        self.analyzeButton.clicked.connect(self.analyzeImage)
        self.layout.addWidget(self.analyzeButton)

    def centerWindow(self):
        centerPoint = QCoreApplication.instance().primaryScreen().geometry().center()
        frameGm = self.frameGeometry()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def openImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.bmp *.jpg *.jpeg *.tiff)")
        if filePath:
            self.currentFilePath = filePath
            image = QImage(filePath)
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            for i in reversed(range(self.histogramLayout.count())):
                self.histogramLayout.itemAt(i).widget().setParent(None)

    def saveImage(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG (*.png);;BMP (*.bmp);;JPEG (*.jpg *.jpeg);;TIFF (*.tiff)"
        )
        if filePath:
            self.imageLabel.pixmap().save(filePath)

    def analyzeImage(self):
        if hasattr(self, "currentFilePath") and self.currentFilePath:
            image = cv2.imread(self.currentFilePath)
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_pixmap = self.convertCvImageToQtPixmap(grayscale)
            gray_label = QLabel()
            gray_label.setPixmap(gray_pixmap)
            self.histogramLayout.addWidget(gray_label)

            colors = ['b', 'g', 'r']
            for i, color in enumerate(colors):
                channel = image[:, :, i]
                hist_pixmap = self.drawHistogram(channel)
                hist_label = QLabel()
                hist_label.setPixmap(hist_pixmap)
                self.histogramLayout.addWidget(hist_label)
    def convertCvImageToQtPixmap(self, cv_image):
        if len(cv_image.shape) == 3:
            height, width, channels = cv_image.shape
            bytes_per_line = channels * width
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            qt_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        else:
            height, width = cv_image.shape
            bytes_per_line = width
            qt_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        qt_pixmap = QPixmap.fromImage(qt_image)
        return qt_pixmap

    def drawHistogram(self, cv_image):
        hist = cv2.calcHist([cv_image], [0], None, [256], [0, 256])
        hist_image = np.zeros((300, 256, 1), dtype=np.uint8)
        cv2.normalize(hist, hist, alpha=0, beta=300, norm_type=cv2.NORM_MINMAX)

        for x, y in enumerate(hist):
            cv2.line(hist_image, (x, 299), (x, 299 - int(y)), (255,), 1)

        return self.convertCvImageToQtPixmap(hist_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec())
