import cv2
import numpy as np
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QLabel, QFileDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QImage, QPixmap


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.modified_image = None

    def load_image(self, filename):
        self.image = cv2.imread(filename)
        self.modified_image = np.copy(self.image)

    def apply_brightness(self, value):
        self.modified_image = cv2.add(self.image, np.array([value, value, value]))

    def apply_contrast(self, value):
        alpha = float(131 * (value + 127)) / (127 * (131 - value))
        self.modified_image = cv2.addWeighted(self.image, alpha, self.image, 0, 0)

    def apply_negative(self):
        self.modified_image = 255 - self.image

    def swap_channels(self):
        self.modified_image = self.image[:, :, [2, 1, 0]].copy()

    def flip_image(self, direction):
        if direction == 'horizontal':
            self.modified_image = cv2.flip(self.image, 1)
        elif direction == 'vertical':
            self.modified_image = cv2.flip(self.image, 0)

    def apply_blur(self):
        self.modified_image = cv2.blur(self.image, (5, 5))


class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_processor = ImageProcessor()

        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_image_button = QPushButton("Load Image")
        self.load_image_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_image_button)

        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.valueChanged.connect(self.apply_brightness)
        self.layout.addWidget(QLabel("Brightness"))
        self.layout.addWidget(self.brightness_slider)

        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.valueChanged.connect(self.apply_contrast)
        self.layout.addWidget(QLabel("Contrast"))
        self.layout.addWidget(self.contrast_slider)

        self.negative_button = QPushButton("Negative")
        self.negative_button.clicked.connect(self.apply_negative)
        self.layout.addWidget(self.negative_button)

        self.swap_channels_button = QPushButton("Swap Channels")
        self.swap_channels_button.clicked.connect(self.swap_channels)
        self.layout.addWidget(self.swap_channels_button)

        self.horizontal_flip_button = QPushButton("Horizontal Flip")
        self.horizontal_flip_button.clicked.connect(self.horizontal_flip)
        self.layout.addWidget(self.horizontal_flip_button)

        self.vertical_flip_button = QPushButton("Vertical Flip")
        self.vertical_flip_button.clicked.connect(self.vertical_flip)
        self.layout.addWidget(self.vertical_flip_button)

        self.blur_button = QPushButton("Blur")
        self.blur_button.clicked.connect(self.apply_blur)
        self.layout.addWidget(self.blur_button)

    def load_image(self):
        self.image_processor.load_image('image.png')
        self.update_image()

    def update_image(self):
        height, width, channel = self.image_processor.modified_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(self.image_processor.modified_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def apply_brightness(self, value):
        self.image_processor.apply_brightness(value)
        self.update_image()

    def apply_contrast(self, value):
        self.image_processor.apply_contrast(value)
        self.update_image()

    def apply_negative(self):
        self.image_processor.apply_negative()
        self.update_image()

    def swap_channels(self):
        self.image_processor.swap_channels()
        self.update_image()

    def horizontal_flip(self):
        self.image_processor.flip_image('horizontal')
        self.update_image()

    def vertical_flip(self):
        self.image_processor.flip_image('vertical')
        self.update_image()

    def apply_blur(self):
        self.image_processor.apply_blur()
        self.update_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec())
