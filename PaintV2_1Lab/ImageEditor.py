from PyQt6.QtGui import QImage, QColor
import cv2
import numpy as np


class ImageEditor:
    def __init__(self, original_image):
        self.original_image: np.ndarray = original_image
        self.image = np.copy(original_image)

    def resetImage(self):
        self.image = np.copy(self.original_image)

    def adjustBrightnessContrast(self, brightness=0, contrast=0):
        brightness = np.interp(brightness, [-100, 100], [-255, 255])
        contrast = np.interp(contrast, [-100, 100], [0.5, 2.0])

        self.image = cv2.convertScaleAbs(self.original_image, alpha=contrast, beta=brightness)
        return self.image

    def _clamp(self, value, min_value=0, max_value=255):
        """Ограничение значения"""
        return max(min_value, min(max_value, value))
