import cv2
import numpy as np
import time
import math
from concurrent.futures import ThreadPoolExecutor
from numba import jit

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
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_result = sobel_filter(frame, kernel_x, kernel_y)
    return sobel_result

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
