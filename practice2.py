'''
UTFPR - Cornélio Procópio
Disciplina: Processamento de Imagens
Aluno: Leonardo Batista
RA: 1885189
'''
######################################################
################### Prática 02 #######################
######################################################

import cv2 as cv
import argparse
import numpy as np

# Função que retorna a mascara a ser utilizada no filtro gaussiano
def mascara_gaussiana(tamanho_mascara):
    mascara_x = np.array(trianguloPascal(tamanho_mascara[0]-1))
    mascara_y = np.array(trianguloPascal(tamanho_mascara[1]-1))

    mascara = np.ndarray(tamanho_mascara, dtype=np.uint8)
    
    for i in range(tamanho_mascara[0]):
        for j in range(tamanho_mascara[1]):
            mascara[i][j] = mascara_x[i] * mascara_y[j]

    return mascara

# a) Realiza a equalização do histograma
def equalizationImage(gray):
    equ = cv.equalizeHist(gray)
    cv.imwrite('a-practice2.png',equ)

#

def main():
    parser = argparse.ArgumentParser(description="Image processing")
    parser.add_argument('-t', '--operation', help='The operation to apply on image', required=True)
    parser.add_argument('-i', '--image', help='Image path', required=True)
    args = vars(parser.parse_args())

    img = cv.imread(args['image'])               # Carregando Imagem
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)   # Transformando a imagem em escala de cinza

    if args['operation'] == 'equalization':
        equalizationImage(gray)
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