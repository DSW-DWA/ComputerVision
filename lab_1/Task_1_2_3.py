import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_color_image(image):
    cv2.imshow('Color Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_gray_and_channels(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b, g, r = cv2.split(image)
    
    cv2.imshow('Gray Image', gray_image)
    cv2.imshow('Blue Channel', b)
    cv2.imshow('Green Channel', g)
    cv2.imshow('Red Channel', r)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    hist_gray = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])

    return hist_gray, hist_b, hist_g, hist_r

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        img_copy = np.copy(image)
        roi = image[y - 5:y + 6, x - 5:x + 6]

        mean, std_dev = cv2.meanStdDev(roi)

        print(f"Coordinates: ({x}, {y})")
        print("RGB values:", image[y, x])
        print("Intensity:", np.mean(image[y, x]))
        print("Mean:", mean)
        print("Standard Deviation:", std_dev)
        print()

        cv2.rectangle(img_copy, (x - 5, y - 5), (x + 5, y + 5), (0, 255, 0), 1)
        cv2.imshow('Color Image', img_copy)
        
image = cv2.imread('image.png')

show_color_image(image)

hist_gray, hist_b, hist_g, hist_r = show_gray_and_channels(image)
for hist, name in zip([hist_gray, hist_b, hist_g, hist_r], ['Gray', 'Blue', 'Green', 'Red']):
    plt.plot(hist, color = name)
    plt.xlim([0, 256])
    plt.show()

cv2.namedWindow('Color Image')
cv2.setMouseCallback('Color Image', mouse_callback)
cv2.waitKey(0)
cv2.destroyAllWindows()
