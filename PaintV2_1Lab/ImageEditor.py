from PyQt6.QtGui import QImage, QColor


class ImageEditor:
    def __init__(self, image: QImage):
        self.image = image

    def adjustBrightnessContrast(self, brightness=0, contrast=0):
        """Регулировка яркости и контрастности"""
        # brightness: -255 to 255; contrast: -100 to 100
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                pixel = self.image.pixel(x, y)
                color = QColor(pixel)
                r = self._clamp(color.red() + brightness)
                g = self._clamp(color.green() + brightness)
                b = self._clamp(color.blue() + brightness)

                # Простой способ регулировки контраста
                r = self._clamp(round(((r - 127) * contrast / 100) + 127))
                g = self._clamp(round(((g - 127) * contrast / 100) + 127))
                b = self._clamp(round(((b - 127) * contrast / 100) + 127))

                self.image.setPixel(x, y, QColor(r, g, b).rgba())
        return self.image

    def invertColors(self):
        """Инверсия цветов"""
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                pixel = self.image.pixel(x, y)
                color = QColor(pixel)
                color.setRed(255 - color.red())
                color.setGreen(255 - color.green())
                color.setBlue(255 - color.blue())
                self.image.setPixel(x, y, color.rgba())
        return self.image

    def swapColorChannels(self, channel1, channel2):
        """Обмен цветовых каналов"""
        for y in range(self.image.height()):
            for x in range(self.image.width()):
                pixel = self.image.pixel(x, y)
                color = QColor(pixel)
                if channel1 == 'r' and channel2 == 'g':
                    color.setRed(color.green())
                    color.setGreen(color.red())
                elif channel1 == 'r' and channel2 == 'b':
                    color.setRed(color.blue())
                    color.setBlue(color.red())
                # Добавьте другие комбинации по необходимости
                self.image.setPixel(x, y, color.rgba())
        return self.image

    def mirror(self, direction='horizontal'):
        """Отражение изображения"""
        mirroredImage = self.image.mirrored(direction == 'horizontal', direction == 'vertical')
        self.image = mirroredImage
        return self.image

    def rotate(self, angle):
        """Поворот изображения"""
        # Этот метод требует дополнительной реализации
        pass

    def applyNoiseReduction(self):
        """Удаление шума"""
        # Этот метод требует использования внешних библиотек или сложных алгоритмов
        pass

    def applySharpening(self):
        """Увеличение резкости изображения"""
        # Этот метод требует использования внешних библиотек или сложных алгоритмов
        pass

    def _clamp(self, value, min_value=0, max_value=255):
        """Ограничение значения"""
        return max(min_value, min(max_value, value))
