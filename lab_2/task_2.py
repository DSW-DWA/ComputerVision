import numpy as np
from PIL import Image
import math


def load_image(file_path):
    return Image.open(file_path)


def save_image(image, file_path):
    image.save(file_path)


def get_pixel(image, x, y):
    return image.getpixel((x, y))


def set_pixel(image, x, y, value):
    image.putpixel((x, y), value)


def apply_kernel(image, kernel, f=False):
    width, height = image.size
    new_image = Image.new("L", (width, height))

    kernel_size = len(kernel)
    offset = kernel_size // 2

    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            new_pixel_value = 0
            for ky in range(kernel_size):
                for kx in range(kernel_size):
                    pixel_value = get_pixel(image, x + kx - offset, y + ky - offset)
                    new_pixel_value += pixel_value * kernel[ky][kx]
            if f:
                set_pixel(new_image, x, y, int(int(new_pixel_value) / kernel_size ** 2))
            else:
                set_pixel(new_image, x, y, int(new_pixel_value))

    return new_image


def absolute_difference(image1, image2):
    width, height = image1.size
    diff_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            diff_value = abs(get_pixel(image1, x, y) - get_pixel(image2, x, y))
            set_pixel(diff_image, x, y, diff_value)

    return diff_image


def rectangular_filter(image, kernel_size):
    kernel = [[1] * kernel_size for _ in range(kernel_size)]
    return apply_kernel(image, kernel, True)


def median_filter(image, kernel_size):
    width, height = image.size
    new_image = Image.new("L", (width, height))

    offset = kernel_size // 2

    for y in range(offset, height - offset):
        for x in range(offset, width - offset):
            pixel_values = []
            for ky in range(kernel_size):
                for kx in range(kernel_size):
                    pixel_values.append(get_pixel(image, x + kx - offset, y + ky - offset))
            median_value = sorted(pixel_values)[len(pixel_values) // 2]
            set_pixel(new_image, x, y, median_value)

    return new_image


def gaussian_filter(image, sigma, f=False):
    kernel_size = int(6 * sigma - 1)
    if kernel_size % 2 == 0:
        kernel_size += 1

    offset = kernel_size // 2
    kernel = [[0] * kernel_size for _ in range(kernel_size)]

    for y in range(-offset, offset + 1):
        for x in range(-offset, offset + 1):
            kernel[y + offset][x + offset] = (
                    1 / (2 * np.pi * sigma ** 2) *
                    np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
            )

    return apply_kernel(image, kernel, f)


def sigma_filter(image, sigma):
    width, height = image.size
    new_image = Image.new("L", (width, height))
    pixels = np.array(image).flatten()

    for y in range(height):
        for x in range(width):
            pixel_value = image.getpixel((x, y))
            indices = np.where((pixels > pixel_value - sigma) & (pixels < pixel_value + sigma))
            selected_pixels = pixels[indices]
            new_pixel_value = int(np.mean(selected_pixels))
            new_image.putpixel((x, y), new_pixel_value)

    return new_image



def sobel_operator(image):
    width, height = image.size
    Gx = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    Gy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    def get_gradient(x, y):
        sum_x = sum_y = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + j < width and 0 <= y + i < height:
                    pixel_value = get_pixel(image, x + j, y + i)  # Изменено здесь
                    sum_x += Gx[i + 1][j + 1] * pixel_value
                    sum_y += Gy[i + 1][j + 1] * pixel_value
        return math.sqrt(sum_x ** 2 + sum_y ** 2)

    total_gradient = 0
    for y in range(height):
        for x in range(width):
            total_gradient += get_gradient(x, y)

    avg_gradient = total_gradient / (width * height)
    return avg_gradient


def sharpness_measure(image):
    return sobel_operator(image)


if __name__ == "__main__":
    input_image = load_image("../assets/noise_image.jpg")

    # rectangular_filtered_image = rectangular_filter(input_image, kernel_size=3)
    # median_filtered_image = median_filter(input_image, kernel_size=3)
    gaussian_filtered_image = gaussian_filter(input_image, sigma=1)
    # sigma_filtered_image= sigma_filter(input_image, sigma=100)
    diff_image = absolute_difference(input_image, gaussian_filtered_image)

    # sharpness_level_original = sharpness_measure(input_image)
    # print(f"Уровень резкости исходного изображения: {sharpness_level_original}")
    # sharpness_level_rectangular = sharpness_measure(rectangular_filtered_image)
    # print(f"Уровень резкости после прямоугольного фильтра: {sharpness_level_rectangular}")
    # sharpness_level_median = sharpness_measure(median_filtered_image)
    # print(f"Уровень резкости после медианного фильтра: {sharpness_level_median}")
    # sharpness_level_gaussian = sharpness_measure(gaussian_filtered_image)
    # print(f"Уровень резкости после Гауссовского фильтра: {sharpness_level_gaussian}")
    # sharpness_level_sigma = sharpness_measure(sigma_filtered_image)
    # print(f"Уровень резкости после сигма-фильтрации: {sharpness_level_sigma}")
    # sharpness_level_diff = sharpness_measure(diff_image)
    # print(f"Уровень резкости разности изображений: {sharpness_level_diff}")

    # save_image(rectangular_filtered_image, "task_2_result/rectangular_filtered_image.jpg")
    # save_image(median_filtered_image, "task_2_result/median_filtered_image.jpg")
    save_image(gaussian_filtered_image, "task_2_result/gaussian_filtered_image.jpg")
    # save_image(sigma_filtered_image, "task_2_result/sigma_filtered_image.jpg")
    # save_image(diff_image, "task_2_result/absolute_difference_image.jpg")
