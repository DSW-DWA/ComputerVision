from PIL import Image
import numpy as np


def log_transform(image, c):
    pixels = np.array(image)
    pixels = c * np.log(1 + pixels)
    return Image.fromarray(pixels.astype('uint8'))


def power_transform(image, gamma, c):
    pixels = np.array(image)
    pixels = c * np.power(pixels, gamma)
    return Image.fromarray(pixels.astype('uint8'))


def binary_transform(image, threshold):
    pixels = np.array(image)
    pixels[pixels <= threshold] = 0
    pixels[pixels > threshold] = 255
    return Image.fromarray(pixels.astype('uint8'))


def range_cut(image, min_val, max_val, constant_value=None):
    pixels = np.array(image)
    if constant_value is not None:
        pixels[pixels < min_val] = constant_value
        pixels[pixels > max_val] = constant_value
    else:
        up = pixels < max_val
        down = pixels > min_val
        pixels[up & down] = 255
    return Image.fromarray(pixels.astype('uint8'))


if __name__ == "__main__":
    input_image = Image.open("../assets/image.png")

    log_transformed_image = log_transform(input_image, c=30)
    power_transformed_image = power_transform(input_image, gamma=0.9, c=2)
    binary_transformed_image = binary_transform(input_image, threshold=100)
    range_cut_image_constant = range_cut(input_image, min_val=50, max_val=200, constant_value=0)
    range_cut_image_original = range_cut(input_image, min_val=60, max_val=70)

    log_transformed_image.save("task_1_result/log_transformed_image.jpg")
    power_transformed_image.save("task_1_result/power_transformed_image.jpg")
    binary_transformed_image.save("task_1_result/binary_transformed_image.jpg")
    range_cut_image_constant.save("task_1_result/range_cut_image_constant.jpg")
    range_cut_image_original.save("task_1_result/range_cut_image_original.jpg")
