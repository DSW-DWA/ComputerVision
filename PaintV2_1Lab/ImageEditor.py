import cv2
import numpy as np


class ImageEditor:
    def __init__(self, original_image):
        self.original_image: np.ndarray = original_image
        self.change_image: np.ndarray = np.copy(original_image)
        self.temp_change_image: np.ndarray = np.copy(original_image)
        self.save_image: np.ndarray = np.copy(original_image)

    def getImage(self):
        return self.change_image

    def save(self):
        self.save_image = self.change_image

    def cancel(self):
        self.change_image = self.save_image
        self.temp_change_image = self.save_image

    def change_channel_intensity_and_cantrast(self, channel, brightness_factor, contrast_factor):
        """
        Изменение интенсивности одного из цветовых каналов + контрастности.
        """
        contrast_factor = np.interp(contrast_factor, [-100, 100], [0.5, 2.0])
        b, g, r = cv2.split(self.original_image)
        if channel == 'r':
            r = cv2.convertScaleAbs(r, beta=brightness_factor, alpha=contrast_factor)
        elif channel == 'g':
            g = cv2.convertScaleAbs(g, beta=brightness_factor, alpha=contrast_factor)
        elif channel == 'b':
            b = cv2.convertScaleAbs(b, beta=brightness_factor, alpha=contrast_factor)

        self.change_image = cv2.merge((b, g, r))

    def invert_image(self):
        """
        Получение негатива изображения.
        """
        self.change_image = cv2.bitwise_not(self.change_image)

    def swap_channels(self, channel1, channel2):
        """
        Обмен цветовыми каналами.
        """
        b, g, r = cv2.split(self.original_image)
        if channel1 == 'Red' and channel2 == 'Green':
            self.change_image = cv2.merge((g, b, r))
        elif channel1 == 'Red' and channel2 == 'Blue':
            self.change_image = cv2.merge((r, g, b))
        elif channel1 == 'Green' and channel2 == 'Blue':
            self.change_image = cv2.merge((r, b, g))
        elif channel1 == 'Green' and channel2 == 'Red':
            self.change_image = cv2.merge((b, r, g))
        elif channel1 == 'Blue' and channel2 == 'Red':
            self.change_image = cv2.merge((g, r, b))
        elif channel1 == 'Blue' and channel2 == 'Green':
            self.change_image = cv2.merge((r, b, g))
        return self.change_image

    def flip_image(self, flip_code):
        """
        Отражение изображения.
        """
        self.change_image = cv2.flip(self.original_image, flip_code)
        return self.change_image

    def blur_image(self, kernel_size):
        """
        Размытие изображения.
        """
        self.change_image = cv2.blur(self.original_image, (kernel_size, kernel_size))
        return self.change_image

    def create_mosaic(self, block_size):
        """
        Создает мозаику на изображении.
        """
        height, width = self.original_image.shape[:2]
        mosaic_image = self.original_image.copy()

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = self.original_image[y : y + block_size, x : x + block_size]
                mean_color = np.mean(block, axis=(0, 1)).astype(int)
                mosaic_image[y : y + block_size, x : x + block_size] = mean_color

        self.change_image = mosaic_image
        return self.change_image
