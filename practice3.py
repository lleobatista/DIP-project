'''
UTFPR - Cornélio Procópio
Disciplina: Processamento de Imagens
Aluno: Leonardo Batista
RA: 1885189
'''
'''
executar código com: 
python -t OPTION -i imagem.jpg
OPERATION disponíveis: 
    - a: Ridler e Calvard
    - b: Otsu

Existem também alguns valores opcionais que podem ser passados:
python3 prog.py -t OPTION -i imagem.jpg [-p POLITICA] [-o OTSU_MIN_MAX]
POLITICA disponíveis: 
	- Políticas de limiarização:
		- b: binária;
		- t: truncada; 
		- z: zero.
(padrão é 'b')

- OTSU_MIN_MAX: 	
	- Maneiras de encontrar o limiar:
		- min: mínima variância intraclasse;
		- max: máxima variância entre classes.
(padrão é 'min')

'''
######################################################
################### Prática 03 #######################
######################################################


import matplotlib.pyplot as plt
import numpy as np
import cv2
import argparse as ag

def main():

    parser = ag.ArgumentParser(description = 'Prática 3')

    #Argumentos obrigatórios na chamada do programa (Operação e Imagem).
    parser.add_argument('-t', action = 'store', dest = 'operation', choices = ['a', 'b'], required = True, help = 'operation')
    parser.add_argument('-i', action = 'store', dest = 'image', required = True, help = 'image\'s path')

    #Argumento opcional (politica), se não for passado, o padrão é b.
    parser.add_argument('-p', action = 'store', dest = 'politica', choices = ['b', 't', 'z'], help = 'politica_limiarização', default = 'b')

    #Argumento opcional (otsu_min_max), se não for passado, o padrão é min.
    parser.add_argument('-o', action = 'store', dest = 'otsu_min_max', choices = ['min', 'max'], help = 'otsu_min_max', default = 'min')

    args = parser.parse_args()

    op = args.operation
    img = args.image

    #Cria e inicializa a variável para a imagem.
    img_antes = cv2.imread(img, 0)

    #Salva o número de linhas e colunas que a imagem tem, 
    #essa informação será usada várias vezes.
    n_linhas = img_antes.shape[0]
    n_colunas = img_antes.shape[1]

    if op == 'a':
        img_depois = op_a(img_antes, n_linhas, n_colunas, args.politica)

    elif op == 'b':
        img_depois = op_b(img_antes, n_linhas, n_colunas, args.politica, args.otsu_min_max)

    #Mostra as imagens original e modificada lado a lado.
    res = np.hstack((img_antes, img_depois)) 

    cv2.imshow("Comparacao", res)
    cv2.waitKey(20000)
    cv2.destroyAllWindows()

def op_a(img_antes, n_linhas, n_colunas, politica):
    
    # limiar inicial - intensidade média da imagem
    soma = 0
    for linha in range(n_linhas):
        for coluna in range(n_colunas):
            soma += img_antes[linha, coluna]

    T = soma/(n_colunas * n_linhas)
    TAnterior = 0

    # Encontrar novo limiar até que a diferença |Ti+1 − Ti| entre os limiares T nas iterações i e i + 1 torna-se suficientemente pequena.
    while(True):

        soma1 = 0
        cont1 = 0
        soma2 = 0
        cont2 = 0

        for linha in range(n_linhas):
            for coluna in range(n_colunas):
                if img_antes[linha, coluna] <= T:
                    soma1 += img_antes[linha, coluna]
                    cont1 += 1
                else:
                    soma2 += img_antes[linha, coluna]
                    cont2 += 1

        TAnterior = T
        T = ((soma1 / cont1) + (soma2 / cont2)) / 2

        if TAnterior == T:
            break

    # Limiarizar imagem com limiar encontrado de acordo com a política definida
    return limiarizar(politica, img_antes, T, n_linhas, n_colunas)

def op_b(img_antes, n_linhas, n_colunas, politica, otsu_min_max):
    #Cria o histograma.
    histograma_img = histograma(img_antes, n_linhas, n_colunas)

    size = img_antes.size
    tam_histograma = len(histograma_img)

    #Encontra o limiar T com o método de Otsu.
    T = otsu(histograma_img, otsu_min_max, size, tam_histograma)

    # Limiarizar imagem com limiar encontrado de acordo com a política definida.
    return limiarizar(politica, img_antes, T, n_linhas, n_colunas)

#Encontra o histograma
def histograma(img, n_linhas, n_colunas):
    histograma_img = [0]*256

    #Determina os valores do histograma da imagem original
    for linha in range(n_linhas):
        for coluna in range(n_colunas):
            histograma_img[img[linha, coluna]] += 1

    return histograma_img

#Encontra o liminar pelo método Otsu.
def otsu(histograma_img, otsu_min_max, size, tam_histograma):

    variancias = [0]*tam_histograma

    if(otsu_min_max == 'min'):
        for l in range(tam_histograma):
            #Encontra a variância das duas classes e a soma dos valores dos histograamas respectivos.
            classe_a, soma_histograma_a, classe_b, soma_histograma_b = otsu_variancia(histograma_img, l, tam_histograma)

            #Calcula a variância encontrada para cada limiar.
            variancias[l] = classe_a * (soma_histograma_a * (1 / size)) + classe_b * (soma_histograma_b * (1 / size))

    else:
        for l in range(tam_histograma):
            #Encontra a variância das duas classes e a soma dos valores dos histograamas respectivos.
            classe_a, soma_histograma_a, classe_b, soma_histograma_b = otsu_variancia(histograma_img, l, tam_histograma)

            #Calcula a variância encontrada para cada limiar.
            variancias[l] = abs(classe_a * (soma_histograma_a * (1 / size)) - classe_b * (soma_histograma_b * (1 / size)))
    
    #Encontra o limiar ótimo dentre as variâncias.
    #Nos dois casos, o valor a ser encontrado foi o mínimo, mesmo quando o objetivo era 
    #maximizar a variância, pois a maneira que o max foi calculado tornou possível isso.
    return variancias.index(min(variancias))

#Encontra as variâncias das classes.
def otsu_variancia(histograma_img, l, tam_histograma):
    #Situação especial para quando l = 0
    if(l == 0):
        media_a = 0
        soma_histograma_a = 0
        classe_a = 0

        media_b, soma_histograma_b = media(histograma_img[l:tam_histograma])
        classe_b = variancia(histograma_img[l:tam_histograma], media_b, soma_histograma_b)

    else:
        media_a, soma_histograma_a = media(histograma_img[0:l])
        classe_a = variancia(histograma_img[0:l], media_a, soma_histograma_a)

        media_b, soma_histograma_b = media(histograma_img[l:tam_histograma])
        classe_b = variancia(histograma_img[l:tam_histograma], media_b, soma_histograma_b)

    return classe_a, soma_histograma_a, classe_b, soma_histograma_b

#Encontra a variância dada uma lista.
def variancia(histograma_img, media, soma_histograma):
    var1 = 0

    if(media == 0 or soma_histograma == 0):
        return 0

    else:
        for i in range(len(histograma_img)):
            var1 += ((i - media) ** 2) * histograma_img[i]

        return var1 / soma_histograma

#Encontra a média dada uma lista.
def media(histograma_img):
    media1 = 0
    soma_histograma = 0

    for i in range(len(histograma_img)):
        media1 += i * histograma_img[i]
        soma_histograma += histograma_img[i]

    if(media1 == 0 or soma_histograma == 0):
        return 0, 0

    else:
        return media1 / soma_histograma, soma_histograma

#Limiariza o histograma da imagem
def limiarizar(politica, img_antes, limiarT, n_linhas, n_colunas): # Função para retornar a imagem limiarizada de acordo com a política escolhida
    #auxImage = grayImage.copy() # Copiando imagem para alterar apenas a sua cópia
    img_depois = np.copy(img_antes)    

    if politica == "b": # Binária
        for linha in range(n_linhas):
            for coluna in range(n_colunas):
                if img_antes[linha, coluna] < limiarT:
                    img_depois[linha, coluna] = 0
                elif img_antes[linha, coluna] > limiarT:
                    img_depois[linha, coluna] = 255

    elif politica == "t": # Truncada
        for linha in range(n_linhas):
            for coluna in range(n_colunas):
                if img_antes[linha, coluna] > limiarT:
                    img_depois[linha, coluna] = round(limiarT)

    elif politica == "z": # Zero
        for linha in range(n_linhas):
            for coluna in range(n_colunas):
                if img_antes[linha, coluna] < limiarT:
                    img_depois[linha, coluna] = 0

    return img_depois

if __name__ == "__main__":
    main()