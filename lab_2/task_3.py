import numpy as np
from PIL import Image, ImageFilter


def unsharp_mask(image_path, k_size=5, lambda_factor=1.5):
    """
    Применение нерезкого маскирования к изображению.
    :param image_path: Путь к файлу изображения.
    :param k_size: Размер ядра для размытия.
    :param lambda_factor: Коэффициент усиления резкости.
    :return: Объект изображения PIL после применения нерезкого маскирования.
    """
    # Загрузка изображения
    original_image = Image.open(image_path).convert('RGB')
    # Применение размытия
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(k_size))
    # Преобразование изображений в массивы
    original_array = np.array(original_image, dtype=float)
    blurred_array = np.array(blurred_image, dtype=float)
    # Нерезкое маскирование
    mask = original_array - blurred_array
    sharp_array = np.clip(original_array + lambda_factor * mask, 0, 255)
    # Преобразование массива обратно в изображение
    sharp_image = Image.fromarray(sharp_array.astype('uint8'), 'RGB')
    return sharp_image


def sharpness_measure(image_path):
    """
    Оценка резкости изображения через средний градиент.
    :param image_path: Путь к файлу изображения.
    :return: Средний градиент резкости.
    """
    image = Image.open(image_path).convert('L')
    image_array = np.array(image, dtype=float)
    # Вычисление градиентов
    gx, gy = np.gradient(image_array)
    gnorm = np.sqrt(gx ** 2 + gy ** 2)
    # Среднее значение градиента
    sharpness = np.mean(gnorm)
    return sharpness


if __name__ == '__main__':
    image_path = '../assets/image.png'
    sharp_image = unsharp_mask(image_path, k_size=5, lambda_factor=1.5)
    sharp_image.save('task_3_result/sharp_image.jpg')

    sharpness_score = sharpness_measure(image_path)
    print(f"Sharpness measure: {sharpness_score}")
