'''
UTFPR - Cornélio Procópio
Disciplina: Processamento de Imagens
Aluno: Leonardo Batista
RA: 1885189
'''
'''
executar código com: 
python -t OPERATION -i imagem.jpg
OPERATION disponíveis: 
a) inverse
b) change-column
c) change-row
d) histogram-strechting
'''
######################################################
################### Prática 01 #######################
######################################################

import cv2 as cv
import numpy as np
import argparse

#a) inverter os valores de intensidade da imagem, tal que o valor 255 passa a ser 0, 254 passa a ser 1,assim por diante.
def inverse(gray):
    rows = gray.shape[0]
    cols = gray.shape[1]
    new_gray = np.ndarray((rows, cols))

    for i in range(rows):
        for j in range(cols):
            new_gray[i][j] = 255 - gray[i][j]

    cv.imwrite('a_practice1.png', new_gray)
    print('the image has complete inversed')

#b) altera as colunas 
def changeCols(gray):
    rows = gray.shape[0]
    cols = gray.shape[1]
    new_gray = np.ndarray((rows, cols))

    for i in range(rows):
        for j in range(0, cols, 2):
            try:
                new_gray[i][j] = gray[i][j + 1]
                new_gray[i][j + 1] = gray[i][j]
            except:
                continue
    cv.imwrite('b_practice1.png', new_gray)
    print('the column has changed')

#c) altera as linhas
def changeRows(gray):
    rows = gray.shape[0]
    cols = gray.shape[1]
    new_gray = np.ndarray((rows, cols))

    for i in range(0, rows, 2):
        for j in range(cols):
            try:
                new_gray[i][j] = gray[i + 1][j]
                new_gray[i + 1][j] = gray[i][j]
            except:
                continue
    cv.imwrite('c_practice1.png', new_gray)
    print('the row has changed')

#d) histogram strechting
def histogramStrechting(gray, gmax, gmin):
    rows = gray.shape[0]
    cols = gray.shape[1]
    new_gray = np.ndarray((rows, cols))

    fmax = np.max(gray)
    fmin = np.min(gray)

    # Loop em cada pixel para ser recalculado o novo valor de intensidade
    for row in range(rows):
        for column in range(cols):
            f = gray[row][column]
            g = ((gmax - gmin)/(fmax-fmin))*(f - fmin) + gmin
            new_gray[row][column] = int(g)

    cv.imwrite('d_practice1.jpg', gray)

def main():
    parser = argparse.ArgumentParser(description="Image processing")
    parser.add_argument('-t', '--operation', help='The operation to apply on image', required=True)
    parser.add_argument('-i', '--image', help='Image path', required=True)
    args = vars(parser.parse_args())

    img = cv.imread(args['image'])               # Carregando Imagem
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)   # Transformando a imagem em escala de cinza

    if args['operation'] == 'inverse':
        inverse(gray)
    elif args['operation'] == 'change-column':
        changeCols(gray)
    elif args['operation'] == 'change-row':
        changeRows(gray)
    elif args['operation'] == 'histogram-strechting':
        histogramStrechting(gray, 255, 0)
    else:
        print('The operation informed is incorrect')

if __name__ == '__main__':
    main()