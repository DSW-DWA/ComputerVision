import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
import matplotlib.pyplot as plt


class BrightnessProfileViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Brightness Profile Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.load_image_button = QPushButton("Load Image")
        self.load_image_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_image_button)

        self.profile_slider = QSlider(Qt.Orientation.Horizontal)
        self.profile_slider.setRange(0, 0)
        self.profile_slider.valueChanged.connect(self.update_brightness_profile)
        self.layout.addWidget(self.profile_slider)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.profile_label = QLabel()
        self.layout.addWidget(self.profile_label)

        self.image = None

    def load_image(self):
        self.image = cv2.imread("image.png", cv2.IMREAD_GRAYSCALE)
        self.update_image()

    def update_image(self):
        height, width = self.image.shape
        bytes_per_line = width
        q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.image_label.setPixmap(pixmap)

        self.profile_slider.setRange(0, height - 1)

    def update_brightness_profile(self, row):
        profile = self.image[row, :]
        plt.plot(profile, color='b')
        plt.xlabel('Pixel')
        plt.ylabel('Brightness')
        plt.title('Brightness Profile')
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrightnessProfileViewer()
    window.show()
    sys.exit(app.exec())
