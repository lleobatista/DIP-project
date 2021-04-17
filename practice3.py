#Leonardo Batista
#RA:1885189

import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('Photos/cat.jpg')

def rescaleFrame(frame, scale=0.2):        #alterar as dimensões da imagem
    width = int(frame.shape[1] * scale)
    heigth = int(frame.shape[0] * scale)
    dimensions = (width,heigth)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(img)

cv.imshow('Cat', gray)
cv.waitKey(0)