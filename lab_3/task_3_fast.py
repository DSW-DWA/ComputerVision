import cv2
import numpy as np
import time
import math
from concurrent.futures import ThreadPoolExecutor
from numba import jit

def gaussian_kernel(size, sigma=1.0):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    return g

@jit(nopython=True)
def convolve2d(image, kernel):
    kernel_height, kernel_width = kernel.shape
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    padded_image = np.zeros((image.shape[0] + pad_height * 2, image.shape[1] + pad_width * 2))
    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

    convolved = np.zeros(image.shape)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            convolved[i, j] = np.sum(kernel * padded_image[i:i + kernel_height, j:j + kernel_width])

    return convolved


def laplacian_of_gaussian(image, kernel_size=5, sigma=1.0):
    gaussian_k = gaussian_kernel(kernel_size, sigma)
    smoothed_image = convolve2d(image, gaussian_k)
    laplacian_k = np.array([[0, 1, 0],
                            [1, -4, 1],
                            [0, 1, 0]])
    return convolve2d(smoothed_image, laplacian_k)

@jit(nopython=True)
def process_chunk(image, new_image, kernel_x, kernel_y, chunk):
    for x in range(chunk[0], chunk[0] + chunk[2]):
        for y in range(chunk[1], chunk[1] + chunk[3]):
            pixel_x = np.sum(image[x - 1:x + 2, y - 1:y + 2] * kernel_x)
            pixel_y = np.sum(image[x - 1:x + 2, y - 1:y + 2] * kernel_y)
            gradient_magnitude = int(math.sqrt(pixel_x ** 2 + pixel_y ** 2))
            new_image[x][y] = gradient_magnitude

def sobel_filter(image, kernel_x, kernel_y):
    width, height = image.shape
    new_image = np.zeros_like(image)
    chunk_size = 150
    chunks = [(x, y, min(chunk_size, width - x - 1), min(chunk_size, height - y - 1)) for x in
              range(1, width - 1, chunk_size)
              for y in range(1, height - 1, chunk_size)]

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_chunk, image, new_image, kernel_x, kernel_y, chunk) for chunk in chunks]
        for future in futures:
            future.result()

    return new_image

def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    # sobel_result = sobel_filter(frame, kernel_x, kernel_y)
    log_image = laplacian_of_gaussian(frame, sigma=1.0999)
    return log_image

def video_processing(input_path):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error opening video file")

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            start_time = time.time()
            processed_frame = process_frame(frame)
            end_time = time.time()
            execution_time = end_time - start_time

            cv2.imshow('Frame', processed_frame)

            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            print(f'Current frame: {current_frame} , Execution time: {execution_time:.5f} seconds')
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_video_path = '../assets/sample_640x360.mp4'
    video_processing(input_video_path)
