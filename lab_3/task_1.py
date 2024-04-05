import numpy as np
import cv2
import time
from PIL import Image
import math


def load_image(file_path):
    return Image.open(file_path).convert('L')


def save_image(image, file_path):
    image.save(file_path)


def sobel_filter(image, kernel_size):
    width, height = image.size

    if kernel_size == 3:
        kernel_x = np.array([[-1, 0, 1],
                             [-2, 0, 2],
                             [-1, 0, 1]])
        kernel_y = np.array([[-1, -2, -1],
                             [0, 0, 0],
                             [1, 2, 1]])
    elif kernel_size == 5:
        kernel_x = np.array([[-2, -1, 0, 1, 2],
                             [-3, -2, 0, 2, 3],
                             [-4, -3, 0, 3, 4],
                             [-3, -2, 0, 2, 3],
                             [-2, -1, 0, 1, 2]])
        kernel_y = np.array([[-2, -3, -4, -3, -2],
                             [-1, -2, -3, -2, -1],
                             [0, 0, 0, 0, 0],
                             [1, 2, 3, 2, 1],
                             [2, 3, 4, 3, 2]])
    elif kernel_size == 7:
        kernel_x = np.array([[-3, -2, -1, 0, 1, 2, 3],
                             [-4, -3, -2, 0, 2, 3, 4],
                             [-5, -4, -3, 0, 3, 4, 5],
                             [-6, -5, -4, 0, 4, 5, 6],
                             [-5, -4, -3, 0, 3, 4, 5],
                             [-4, -3, -2, 0, 2, 3, 4],
                             [-3, -2, -1, 0, 1, 2, 3]])
        kernel_y = np.array([[-3, -4, -5, -6, -5, -4, -3],
                             [-2, -3, -4, -5, -4, -3, -2],
                             [-1, -2, -3, -4, -3, -2, -1],
                             [0, 0, 0, 0, 0, 0, 0],
                             [1, 2, 3, 4, 3, 2, 1],
                             [2, 3, 4, 5, 4, 3, 2],
                             [3, 4, 5, 6, 5, 4, 3]])

    new_image = Image.new("L", (width, height))

    for y in range(((kernel_size - 1) // 2), height - ((kernel_size - 1) // 2)):
        for x in range(((kernel_size - 1) // 2), width - ((kernel_size - 1) // 2)):
            pixel_x = sum(image.getpixel((x + i, y + j)) * kernel_x[i][j] for i in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)) for j in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)))
            pixel_y = sum(image.getpixel((x + i, y + j)) * kernel_y[i][j] for i in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)) for j in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)))
            gradient_magnitude = int(math.sqrt(pixel_x ** 2 + pixel_y ** 2))
            new_image.putpixel((x, y), gradient_magnitude)

    return new_image


def main():
    input_image = load_image("../assets/image_bw.jpg")

    kernel_sizes = [3, 5, 7]
    for kernel_size in kernel_sizes:
        start_time = time.time()
        sobel_result = sobel_filter(input_image, kernel_size)
        end_time = time.time()
        print(f"Kernel size {kernel_size}x{kernel_size}: {end_time - start_time:.5f} seconds")

        save_image(sobel_result, f"./task_1_result/sobel_{kernel_size}x{kernel_size}.jpg")


if __name__ == "__main__":
    main()
