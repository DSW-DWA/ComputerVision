import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QVBoxLayout, QDialog, QLineEdit, QLabel
import sys

image = cv2.imread('../assets/example_image.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# а) Увеличение/уменьшение интенсивности яркости и отдельных цветовых каналов
def adjust_brightness(image, alpha, beta):
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

# b) Повышение/снижение контрастности изображения
def adjust_contrast(image, alpha, beta):
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

# c) Получение негатива яркости или цветовых каналов
def invert_colors(image):
    inverted = cv2.bitwise_not(image)
    return inverted

# d) Обмен цветовых каналов
def swap_channels(image):
    b, g, r = cv2.split(image)
    swapped = cv2.merge([r, g, b])  # меняем местами каналы
    return swapped

# e) Симметричное отображение изображения по горизонтали или вертикали
def flip_image(image, direction):
    flipped = cv2.flip(image, direction)
    return flipped

# f) Удаление шума методом размытия изображения
def remove_noise(image, method='blur', ksize=3):
    if method == 'blur':
        blurred = cv2.blur(image, (ksize, ksize))
    elif method == 'median':
        blurred = cv2.medianBlur(image, ksize)
    else:
        blurred = image
    return blurred

# brightened_image = adjust_brightness(image, alpha=1.5, beta=0)
# contrasted_image = adjust_contrast(image, alpha=1.5, beta=0)
# inverted_image = invert_colors(image)
# swapped_channels_image = swap_channels(image)
# flipped_horizontally_image = flip_image(image, 1)
# flipped_vertically_image = flip_image(image, 0)
# blurred_image = remove_noise(image, method='blur', ksize=5)
# median_blurred_image = remove_noise(image, method='median', ksize=5)

# cv2.imshow('Original Image', image)
# cv2.imshow('Brightened Image', brightened_image)
# cv2.imshow('Contrasted Image', contrasted_image)
# cv2.imshow('Inverted Image', inverted_image)
# cv2.imshow('Swapped Channels Image', swapped_channels_image)
# cv2.imshow('Flipped Horizontally Image', flipped_horizontally_image)
# cv2.imshow('Flipped Vertically Image', flipped_vertically_image)
# cv2.imshow('Blurred Image', blurred_image)
# cv2.imshow('Median Blurred Image', median_blurred_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

class Form(QDialog):

    def __init__(self, parent=None, image=None):
        self.image = image

        super(Form, self).__init__(parent)
        self.button = QPushButton('Show image')
        self.button.clicked.connect(self.show_image)

        self.sliderBrightness = QSlider(Qt.Orientation.Horizontal)
        self.sliderBrightness.setMaximum(500)
        self.sliderBrightness.setMinimum(0)
        self.sliderBrightness.setValue(100)

        layout = QVBoxLayout()
        layout.addWidget(self.sliderBrightness)
        layout.addWidget(self.button)
        self.setLayout(layout)
        

    def show_image(self):
        brightness = self.sliderBrightness.value()
        adj_image = adjust_brightness(self.image, alpha=brightness / 100, beta=-1)
        cv2.imshow('Adjusted Image', adj_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form(image=image)
    form.show()
    sys.exit(app.exec())