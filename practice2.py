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
a) equalization
b) averaging
c) median
d) gaussian
'''
######################################################
################### Prática 02 #######################
######################################################

import cv2 as cv
import argparse
import numpy as np

###### -----------> AS MÁSCAS APLICADAS SÃO 5X5 <----------- ######

# a) Realiza a equalização do histograma
def equalizationImage(gray):
    equ = cv.equalizeHist(gray)
    cv.imwrite('a-practice2.png',equ)

# b) Aplicar filtro da média
def averageFiltering(gray):
    kernel = np.ones((5,5),np.float32)/25
    dst = cv.filter2D(gray,-1,kernel)
    cv.imwrite('b-practice2.png', dst)
    print('the filter has applied')

# c) Aplicar Filtro da mediana
def medianFiltering(gray):
    median = cv.medianBlur(gray, 5)
    cv.imwrite('c-practice2.png',median)
    print('the filter has applied')

# d) Aplicar filtro Gaussiano
def gaussianFiltering(gray):
    gaus = cv.GaussianBlur(gray, (5,5), 0)
    cv.imwrite('d-practice2.png',gaus)
    print('the filter has applied')

def main():
    parser = argparse.ArgumentParser(description="Image processing")
    parser.add_argument('-t', '--operation', help='The operation to apply on image', required=True)
    parser.add_argument('-i', '--image', help='Image path', required=True)
    args = vars(parser.parse_args())

    img = cv.imread(args['image'])               # Carregando Imagem
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)   # Transformando a imagem em escala de cinza

    if args['operation'] == 'equalization':
        equalizationImage(gray)
    elif args['operation'] == 'averaging':
        averageFiltering(gray)
    elif args['operation'] == 'median':
        medianFiltering(gray)
    elif args['operation'] == 'gaussian':
        gaussianFiltering(gray)
    else:
        print('The operation informed is incorrect')

if __name__ == '__main__':
    main()