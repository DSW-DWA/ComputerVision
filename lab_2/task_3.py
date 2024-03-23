import numpy as np
from PIL import Image

from task_2 import load_image, rectangular_filter


def unsharp_masking(image_array, k, lambda_coefficient):
    """
    Применяет нерезкое маскирование к изображению для повышения резкости.
    """
    # сглаживание
    smoothed_image = np.array(rectangular_filter(image_array, k))
    # J(p) = (1 + λ)I(p) - λ*S(p) добавление усиленного детального компонента к исходному изображению для повышения резкости
    sharpened_image_array = (1 + lambda_coefficient)*np.array(image_array) - lambda_coefficient * smoothed_image
    # J′(p) = clip(J(p),0,255) ограничение значений пикселей полученного изображения диапазоном [0, 255]
    sharpened_image_array = np.clip(sharpened_image_array, 0, 255)
    return Image.fromarray(sharpened_image_array.astype('uint8'))


if __name__ == '__main__':
    input_image = load_image("../assets/image_bw.jpg")
    sharp_image = unsharp_masking(input_image, k=3, lambda_coefficient=1.5)
    sharp_image.save('task_3_result/sharp_image.jpg')
