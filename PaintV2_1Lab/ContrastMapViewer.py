import cv2
import numpy as np
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel
from PyQt6.QtGui import QImage, QPixmap


class ContrastMapViewer(QDialog):
    def __init__(self, image):
        super().__init__()

        self.setWindowTitle("Contrast Map Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.contrast_formula_combobox = QComboBox()
        self.contrast_formula_combobox.addItems(["4 Neighbors", "8 Neighbors", "Custom Window"])
        self.layout.addWidget(self.contrast_formula_combobox)

        self.calculate_contrast_button = QPushButton("Calculate Contrast Map")
        self.calculate_contrast_button.clicked.connect(self.calculate_contrast_map)
        self.layout.addWidget(self.calculate_contrast_button)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.contrast_map_label = QLabel()
        self.layout.addWidget(self.contrast_map_label)
        
        self.image = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)

    def update_image(self):
        height, width, channels = self.image.shape
        bytes_per_line = width
        q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.image_label.setPixmap(pixmap)

    def calculate_contrast_map(self):
        formula = self.contrast_formula_combobox.currentText()

        if formula == "4 Neighbors":
            contrast_map = self.calculate_contrast_4_neighbors(self.image)
        elif formula == "8 Neighbors":
            contrast_map = self.calculate_contrast_8_neighbors(self.image)
        elif formula == "Custom Window":
            ### Я попробовал чет нихуя 
            pass
        else:
            return

        cv2.normalize(contrast_map, contrast_map, 0, 255, cv2.NORM_MINMAX)
        contrast_map = contrast_map.astype(np.uint8)

        height, width, channels = contrast_map.shape
        bytes_per_line = width
        q_img = QImage(contrast_map.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.contrast_map_label.setPixmap(pixmap)

    def calculate_contrast_4_neighbors(self, image):
        contrast_map = np.zeros_like(image)
        height, width, channels = image.shape

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                contrast_map[y, x] = self.calculate_contrast(image[y, x],
                                                              image[y - 1, x],
                                                              image[y + 1, x],
                                                              image[y, x - 1],
                                                              image[y, x + 1])

        return contrast_map

    def calculate_contrast_8_neighbors(self, image):
        contrast_map = np.zeros_like(image)
        height, width, channels = image.shape

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                contrast_map[y, x] = self.calculate_contrast(image[y, x],
                                                              image[y - 1, x],
                                                              image[y + 1, x],
                                                              image[y, x - 1],
                                                              image[y, x + 1],
                                                              image[y - 1, x - 1],
                                                              image[y - 1, x + 1],
                                                              image[y + 1, x - 1],
                                                              image[y + 1, x + 1])

        return contrast_map

    def calculate_contrast(self, center, *neighbors):
        mean_neighbors = sum(neighbors) / len(neighbors)
        std_dev = np.std([center] + list(neighbors))
        return abs(center - mean_neighbors) / (std_dev + 1)