import numpy as np
from PIL import Image

from task_2 import load_image, rectangular_filter, gaussian_filter, median_filter


def unsharp_masking(image_array, filter_coefficients, lambda_coefficient, filter):
    """
    Применяет нерезкое маскирование к изображению для повышения резкости.
    """
    # сглаживание
    smoothed_image = np.array(filter(image_array, filter_coefficients))
    # J(p) = (1 + λ)I(p) - λ*S(p) добавление усиленного детального компонента к исходному изображению для повышения резкости
    sharpened_image_array = (1 + lambda_coefficient)*np.array(image_array) - lambda_coefficient * smoothed_image
    # J′(p) = clip(J(p),0,255) ограничение значений пикселей полученного изображения диапазоном [0, 255]
    sharpened_image_array = np.clip(sharpened_image_array, 0, 255)
    return Image.fromarray(sharpened_image_array.astype('uint8'))


if __name__ == '__main__':
    input_image = load_image("../assets/image_bw.jpg")
    sharp_image = unsharp_masking(input_image, filter_coefficients=3, lambda_coefficient=1.5, filter=rectangular_filter)
    sharp_image.save('task_3_result/sharp_image_rect.jpg')
    sharp_image = unsharp_masking(input_image, filter_coefficients=1.2, lambda_coefficient=1.5, filter=gaussian_filter)
    sharp_image.save('task_3_result/sharp_image_gauss.jpg')
    sharp_image = unsharp_masking(input_image, filter_coefficients=3, lambda_coefficient=1.5, filter=median_filter)
    sharp_image.save('task_3_result/sharp_image_median.jpg')
