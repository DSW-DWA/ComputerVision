import cv2
import numpy as np
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QLineEdit
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

        self.image = self.custom_cvtColor(image)

        # Custom Window parameters
        self.custom_window_width_label = QLabel("Custom neighbors:")
        self.layout.addWidget(self.custom_window_width_label)
        self.custom_window_width_input = QLineEdit()
        self.layout.addWidget(self.custom_window_width_input)

    def update_image(self):
        height, width, channels = self.image.shape
        bytes_per_line = width
        q_img = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.image_label.setPixmap(pixmap)

    def contrast_map(self, gray_image, method='4_neighbors', Window_size=3):
        height, width = self.image.shape
        contrast_map = np.zeros_like(gray_image, dtype=np.float32)

        for i in range(height):
            for j in range(width):
                if method == '4_neighbors':
                    neighbors = [
                        gray_image[max(i-1, 0), j],
                        gray_image[min(i+1, height-1), j],
                        gray_image[i, max(j-1, 0)],
                        gray_image[i, min(j+1, width-1)]
                    ]
                elif method == '8_neighbors':
                    neighbors = [
                        gray_image[max(i-1, 0), max(j-1, 0)],
                        gray_image[max(i-1, 0), j],
                        gray_image[max(i-1, 0), min(j+1, width-1)],
                        gray_image[i, max(j-1, 0)],
                        gray_image[i, min(j+1, width-1)],
                        gray_image[min(i+1, height-1), max(j-1, 0)],
                        gray_image[min(i+1, height-1), j],
                        gray_image[min(i+1, height-1), min(j+1, width-1)]
                    ]
                else:
                    window_size = Window_size
                    half_window = window_size // 2
                    neighbors = []
                    for m in range(-half_window, half_window+1):
                        for n in range(-half_window, half_window+1):
                            if 0 <= i+m < height and 0 <= j+n < width:
                                neighbors.append(gray_image[i+m, j+n])

                contrast_map[i, j] = max(neighbors) - min(neighbors)

        return contrast_map
    def calculate_contrast_map(self):
        formula = self.contrast_formula_combobox.currentText()

        if formula == "4 Neighbors":
            contrast_map = self.contrast_map(self.image, "4_neighbors")
        elif formula == "8 Neighbors":
            contrast_map = self.contrast_map(self.image, "8_neighbors")
        elif formula == "Custom Window":
            window_size = int(self.custom_window_width_input.text())
            contrast_map = self.contrast_map(self.image, "custom_window", window_size)
        else:
            return

        self.custom_normalize(contrast_map, contrast_map, 0, 255)
        contrast_map = contrast_map.astype(np.uint8)

        height, width = contrast_map.shape
        bytes_per_line = width
        q_img = QImage(contrast_map.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.contrast_map_label.setPixmap(pixmap)


        self.custom_normalize(contrast_map, contrast_map, 0, 255)
        contrast_map = contrast_map.astype(np.uint8)

        height, width = contrast_map.shape
        bytes_per_line = width
        q_img = QImage(contrast_map.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        pixmap = pixmap.scaledToWidth(400)
        self.contrast_map_label.setPixmap(pixmap)

    def custom_normalize(self, src, dst, alpha, beta):
        src_min = np.min(src)
        src_max = np.max(src)
        src_range = src_max - src_min
        dst_range = beta - alpha
        dst[:] = (src - src_min) * (dst_range / src_range) + alpha
    
    def custom_cvtColor(self, image):
        gray_weights = np.array([0.114, 0.587, 0.299])
        gray_image = np.dot(image[..., :3], gray_weights)
        return gray_image.astype(np.uint8)