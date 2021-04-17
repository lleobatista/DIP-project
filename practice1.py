'''
UTFPR - Cornélio Procópio
Disciplina: Processamento de Imagens
Aluno: Leonardo Batista
RA: 1885189
'''
################### Prática 01 #######################

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('Photos/cat.jpg')

#alterar as dimensões da imagem
def rescaleFrame(frame, scale=0.2):                                 
    width = int(frame.shape[1] * scale)
    heigth = int(frame.shape[0] * scale)
    dimensions = (width,heigth)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#transformando imagem em cinza e criando um histograma. Contem novas variáveis do mesmo shape que a imagem gray.
resized_image = rescaleFrame(img)
gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY) 
gray2 = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)             
hist = cv.calcHist([gray], [0], None, [256], [0,256])
cols = gray.shape[0]
rows = gray.shape[1]
new_gray = np.ndarray((cols, rows))
invert_col = np.ndarray((cols, rows))
invert_row = np.ndarray((cols, rows))

#a) inverter os valores de intensidade da imagem, tal que o valor 255 passa a ser 0, 254 passa a ser 1,assim por diante.
for i in range(0, gray.shape[0]):
    for j in range(0, gray.shape[1]):
          gray.itemset((i,j), 255 - gray[i,j])

#b) altera as colunas 
for i in range(invert_col.shape[0]):
        for j in range(0, invert_col.shape[1], 2):
            try:
                invert_col[i][j] = new_gray[i][j + 1]
                invert_col[i][j + 1] = new_gray[i][j]
            except:
                continue   

#c) altera as linhas
for i in range(0, invert_row.shape[0], 2):
        for j in range(invert_row.shape[1]):
            try:
                invert_row[i][j] = new_gray[i + 1][j]
                invert_row[i + 1][j] = new_gray[i][j]
            except:
                continue

#d) histogram strechting
fmax = np.max(gray2)
fmin = np.min(gray2)

for linha in range(gray2.shape[0]):
    for coluna in range(gray.shape[1]):
        f = gray2[linha][coluna]
        g = ((255)/(fmax-fmin))*(f - fmin)
        gray2[linha][coluna] = int(g)


#plotando histogram
plt.hist(gray.ravel(),256,[0,256])                                  
plt.show()

#exibindo imagens
cv.imshow('histogram-strechting.jpg', gray2)
cv.imshow('inverted col', invert_col)
cv.imshow('inverted row', invert_row)                                    
cv.imshow('Cat', gray)
cv.waitKey(0)