import numpy as np
from PIL import Image
import math


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
