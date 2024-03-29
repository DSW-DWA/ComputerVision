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

    def reset(self):
        self.change_image = np.copy(self.original_image)
        self.temp_change_image = np.copy(self.original_image)

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
            r = self.custom_convertScaleAbs(r, brightness_factor, contrast_factor)
        elif channel == 'g':
            g = self.custom_convertScaleAbs(g, brightness_factor, contrast_factor)
        elif channel == 'b':
            b = self.custom_convertScaleAbs(b, brightness_factor, contrast_factor)

        self.change_image = cv2.merge((b, g, r))

    def invert_image(self):
        """
        Получение негатива изображения.
        """
        self.change_image = self.custom_bitwise_not(self.change_image)

    def custom_bitwise_not(self, image):
        max_value = np.iinfo(image.dtype).max
        inverted_image = max_value - image
        return inverted_image


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
        self.change_image =self.custom_flip_image(self.change_image, flip_code)
        return self.change_image
    
    def custom_flip_image(self, image, flip_code):
        height, width = image.shape[:2]
        flipped_image = np.zeros_like(image)

        if flip_code == 0:
            for y in range(height):
                flipped_image[y, :] = image[height - y - 1, :]
        elif flip_code == 1:
            for x in range(width):
                flipped_image[:, x] = image[:, width - x - 1]
        elif flip_code == -1:
            for y in range(height):
                flipped_image[y, :] = image[height - y - 1, ::-1]

        return flipped_image

    def blur_image(self, kernel_size):
        """
        Размытие изображения.
        """
        self.change_image = self.custom_blur_image(self.change_image, kernel_size)
        return self.change_image

    def custom_blur_image(self, image, kernel_size):
        height, width = image.shape[:2]
        blurred_image = np.zeros_like(image)

        for c in range(image.shape[2]):
            for y in range(height):
                for x in range(width):
                    total = 0
                    count = 0
                    for j in range(-kernel_size//2, kernel_size//2 + 1):
                        for i in range(-kernel_size//2, kernel_size//2 + 1):
                            if (0 <= x + i < width) and (0 <= y + j < height):
                                total += image[y + j, x + i, c]
                                count += 1
                    blurred_image[y, x, c] = total // count

        return blurred_image

    def create_mosaic(self, block_size):
        """
        Создает мозаику на изображении.
        """
        height, width = self.change_image.shape[:2]
        mosaic_image = self.change_image.copy()

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = self.change_image[y : y + block_size, x : x + block_size]
                mean_color = np.mean(block, axis=(0, 1)).astype(int)
                mosaic_image[y : y + block_size, x : x + block_size] = mean_color

        self.change_image = mosaic_image
        return self.change_image

    def custom_convertScaleAbs(self, src, brightness_factor, contrast_factor):
        scaled_src = src.astype(np.float32) * contrast_factor + brightness_factor
        scaled_src = np.clip(scaled_src, 0, 255)
        dst = scaled_src.astype(np.uint8)
        return dst
