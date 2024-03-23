import numpy as np
from PIL import Image

from task_2 import gaussian_filter, load_image


def unsharp_masking(image_array, sigma, lambda_coefficient):
    """
    Применяет нерезкое маскирование к изображению для повышения резкости.
    """
    # сглаживание
    smoothed_image = np.array(gaussian_filter(image_array, sigma))
    # R(p) = I(p) – S(p) вычисление высокочастотного (детального) компонента изображения
    high_freq_image_array = image_array - smoothed_image
    # J(p) = I(p) + λ*R(p) добавление усиленного детального компонента к исходному изображению для повышения резкости
    sharpened_image_array = image_array + lambda_coefficient * high_freq_image_array
    # J′(p) = clip(J(p),0,255) ограничение значений пикселей полученного изображения диапазоном [0, 255]
    sharpened_image_array = np.clip(sharpened_image_array, 0, 255)
    return Image.fromarray(sharpened_image_array.astype('uint8'))


if __name__ == '__main__':
    input_image = load_image("../assets/image_bw.jpg")
    sharp_image = unsharp_masking(input_image, sigma=1, lambda_coefficient=1.5)
    sharp_image.save('task_3_result/sharp_image.jpg')
