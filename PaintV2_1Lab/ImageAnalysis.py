import cv2
import numpy as np
from matplotlib import pyplot as plt
from ContrastMapViewer import ContrastMapViewer
from BrightnessProfileViewer import BrightnessProfileViewer
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class ImageAnalysis:
    def __init__(self, image):
        self.image = image

    def mouse_callback(self, event, x, y, flags, param):
        cv2.imshow('Color Image', self.image)
        if event == cv2.EVENT_MOUSEMOVE:
            
            img_copy = np.copy(self.image)
            roi = self.image[y - 5:y + 6, x - 5:x + 6]

            mean, std_dev = 0,[0,0,0]
            for i in roi:
                for j in i:
                    mean += np.mean(j)
            
            mean /= 121

            for k in [0,1,2]:
                mean_ch = 0
                for i in roi:
                    for j in i:
                        mean_ch += j[k]
                
                mean_ch /= (roi.shape[0] * roi.shape[1])
                
                for i in roi:
                    for j in i:
                        std_dev[k] = np.sqrt(np.sum((j[k] - mean_ch) ** 2) / (roi.shape[0] * roi.shape[1]))

            print(f"Coordinates: ({x}, {y})")
            print("RGB values:", self.image[y, x])
            print("Intensity:", np.mean(self.image[y, x]))
            print("Mean:", mean)
            print("Standard Deviation:", std_dev)
            print()

            cv2.rectangle(img_copy, (x - 5, y - 5), (x + 5, y + 5), (0, 255, 0), 1)
            cv2.imshow('Color Image', img_copy)

    def blackWhite(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        cv2.imshow('Gray Image', gray_image)

        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()
    
    def redChannel(self):
        b, g, r = cv2.split(self.image)
        hist = cv2.calcHist([r], [0], None, [256], [0, 256])
        cv2.imshow('Red Channel', r)

        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()

    def greenChannel(self):
        b, g, r = cv2.split(self.image)
        hist = cv2.calcHist([g], [0], None, [256], [0, 256])
        cv2.imshow('Green Channel', g)

        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()
    
    def blueChannel(self):
        b, g, r = cv2.split(self.image)
        hist = cv2.calcHist([b], [0], None, [256], [0, 256])
        cv2.imshow('Blue Channel', b)

        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()


    def RegionAnalysis(self):
        cv2.namedWindow('Color Image')
        cv2.setMouseCallback('Color Image', self.mouse_callback)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def ContrastMapViewer(self):
        dlg = ContrastMapViewer(self.image)
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

    
    def BrightnessProfileViewer(self):
        dlg = BrightnessProfileViewer(self.image)
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")