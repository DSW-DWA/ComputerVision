import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import cv2
import numpy as np
import matplotlib.pyplot as plt


class BrightnessProfileViewer(QDialog):
    def __init__(self, image):
        super().__init__()

        self.setWindowTitle("Brightness Profile Viewer")
        self.setGeometry(100, 100, 800, 600)

        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.profile_slider = QSlider(Qt.Orientation.Horizontal)
        self.profile_slider.setRange(0, 0)
        self.profile_slider.tickInterval()
        # self.profile_slider.valueChanged.connect(self.update_brightness_profile)
        self.layout.addWidget(self.profile_slider)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.profile_label = QLabel()
        self.layout.addWidget(self.profile_label)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.image = self.custom_cvtColor(image)
        self.update_image()

        self.show_hist_button = QPushButton("Show hist")
        self.show_hist_button.clicked.connect(self.update_brightness_profile)
        self.layout.addWidget(self.show_hist_button)

    def update_image(self):
        height, width= self.image.shape
        bytes_per_line = width
        q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.image_label.setPixmap(pixmap)

        self.profile_slider.setRange(0, height - 1)
        self.profile_slider.setTickPosition(QSlider.TickPosition.TicksBelow) 

    def update_brightness_profile(self):
        ax = self.figure.add_subplot(111)
        profile = self.image[self.profile_slider.value(),:]
        ax.plot(profile, color='b')
        self.canvas.draw()

    def custom_cvtColor(self, image):
        gray_weights = np.array([0.114, 0.587, 0.299])
        gray_image = np.dot(image[..., :3], gray_weights)
        return gray_image.astype(np.uint8)
