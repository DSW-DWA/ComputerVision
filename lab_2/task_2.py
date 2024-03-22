import time
import numpy as np
from PIL import Image, ImageFilter


# Загрузка изображения и преобразование в массив numpy
def load_image(image_path):
    image = Image.open(image_path)
    return np.array(image)


# Сохранение массива numpy как изображение
def save_image(image_array, output_path):
    image = Image.fromarray(image_array)
    image.save(output_path)


# Прямоугольный фильтр
def average_filter(image_array, kernel_size=3):
    return np.array(Image.fromarray(image_array).filter(ImageFilter.BoxBlur((kernel_size - 1) / 2)))


# Медианный фильтр
def median_filter(image_array, kernel_size=3):
    return np.array(Image.fromarray(image_array).filter(ImageFilter.MedianFilter(size=kernel_size)))


# Фильтр Гаусса
def gaussian_filter(image_array, sigma=1.0):
    return np.array(Image.fromarray(image_array).filter(ImageFilter.GaussianBlur(radius=sigma)))


# Сигма-фильтр
def sigma_filter(image_array, sigma=1.0, kernel_size=3):
    pad_width = kernel_size // 2
    padded_image = np.pad(image_array, pad_width=pad_width, mode='constant', constant_values=0)
    result = np.zeros_like(image_array)

    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            local_patch = padded_image[x:x+kernel_size, y:y+kernel_size]
            local_mean = np.mean(local_patch)
            local_std = np.std(local_patch)

            threshold = local_std * sigma
            mask = np.abs(local_patch - local_mean) < threshold
            result[x, y] = np.mean(local_patch[mask])

    return result


# Визуальная оценка качества
def absolute_difference(original, processed):
    return np.abs(original - processed)


if __name__ == '__main__':
    image_path = '../assets/image.png'
    image_array = load_image(image_path)

    # Прямоугольный фильтр
    start_time = time.time()
    filtered_image_array = average_filter(image_array)
    end_time = time.time()
    print(f"Average filter took {end_time - start_time} seconds.")
    save_image(filtered_image_array, 'task_2_result/average_filtered.jpg')
    diff = absolute_difference(image_array, filtered_image_array)
    save_image(diff.astype(np.uint8), 'task_2_result/average_filtered_difference.jpg')

    # Медианный фильтр
    start_time = time.time()
    filtered_image_array = median_filter(image_array)
    end_time = time.time()
    print(f"Median filter took {end_time - start_time} seconds.")
    save_image(filtered_image_array, 'task_2_result/median_filtered.jpg')
    diff = absolute_difference(image_array, filtered_image_array)
    save_image(diff.astype(np.uint8), 'task_2_result/median_filtered_difference.jpg')

    # Фильтр Гаусса
    start_time = time.time()
    filtered_image_array = gaussian_filter(image_array, sigma=2.0)
    end_time = time.time()
    print(f"Gaussian filter took {end_time - start_time} seconds.")
    save_image(filtered_image_array, 'task_2_result/gaussian_filtered.jpg')
    diff = absolute_difference(image_array, filtered_image_array)
    save_image(diff.astype(np.uint8), 'task_2_result/gaussian_filtered_difference.jpg')

    # Сигма-фильтр
    start_time = time.time()
    filtered_image_array = sigma_filter(image_array, sigma=2.0)
    end_time = time.time()
    print(f"Sigma filter took {end_time - start_time} seconds.")
    save_image(filtered_image_array, 'task_2_result/sigma_filtered.jpg')
    diff = absolute_difference(image_array, filtered_image_array)
    save_image(diff.astype(np.uint8), 'task_2_result/sigma_filtered_difference.jpg')
