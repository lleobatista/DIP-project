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
gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)  #alterar a cor para cinza
hist = cv.calcHist([gray], [0], None, [256], [0,256])
invert = gray
hist = cv.calcHist([invert], [0], None, [256], [0,256])

for a in range(0,gray.shape[0]):                    #correndo a imagem e alterando cada pixel
    for b in range(0,gray.shape[1]):
          gray.itemset((a,b), 255 - gray[a,b])
    
for c in range(0,invert.shape[0]):                  #alterando as colunas e linhas pares por impar             
    for d in range(0,invert.shape[1]):
        if((b%2) == 0):
            invert_column = invert[a,b]
            invert.itemset((a,b), inverte[a,b+1])
            invert.itemset((a,b+1), invert_column)
        if((a%2) == 0):
            invert_row = invert[a,b]
            invert.itemset((a,b), inverte[a+1,b])
            invert.itemset((a+1,b), invert_row)
        

plt.hist(gray.ravel(),256,[0,256])                     #plotando hist
plt.show()
plt.hist(invert.ravel(),256,[0,256])
plt.show()

cv.imshow('Cat - inverted', invert)                    #exibindo imagem
cv.imshow('Cat', gray)
cv.waitKey(0)