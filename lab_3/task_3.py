import cv2
import numpy as np
from PIL import Image
import math
import time

def sobel_filter(image, kernel_size):
    width, height = image.shape

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

    new_image = image.copy()

    for y in range(((kernel_size - 1) // 2), height - ((kernel_size - 1) // 2)):
        for x in range(((kernel_size - 1) // 2), width - ((kernel_size - 1) // 2)):
            pixel_x = sum(image[x + i][y + j] * kernel_x[i][j] for i in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)) for j in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)))
            pixel_y = sum(image[x + i][y + j] * kernel_y[i][j] for i in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)) for j in
                          range(-1 * ((kernel_size - 1) // 2), ((kernel_size - 1) // 2 + 1)))
            gradient_magnitude = int(math.sqrt(pixel_x ** 2 + pixel_y ** 2))
            
            new_image[x][y] = gradient_magnitude

    return new_image

def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sobel_result = sobel_filter(frame, 3)
    return sobel_result

def video_processing(input_path):
    
    cap = cv2.VideoCapture(input_path)

    if (cap.isOpened()== False): 
        print("Error opening video file") 
    
    while(cap.isOpened()): 
        
        ret, frame = cap.read() 
        if ret == True:  
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


