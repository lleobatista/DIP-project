'''
UTFPR - Cornélio Procópio
Disciplina: Processamento de Imagens
Aluno: Leonardo Batista
RA: 1885189
'''
################### Prática 02 #######################

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread('Photos/cat2.jpg')

#alterar as dimensões da imagem
def rescaleFrame(frame, scale=0.2):                     
    width = int(frame.shape[1] * scale)
    heigth = int(frame.shape[0] * scale)
    dimensions = (width,heigth)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


resized_image = rescaleFrame(img)
img_cinza = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)
gray = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)    #transformando em cinza

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
hist,bins = np.histogram(gray.flatten(),256,[0,256])        
cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')       
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

equ = cv.equalizeHist(gray)
res = np.hstack((gray,equ)) #imagens lado-a-lado
cv.imwrite('res.png',res)

# b) Aplicar filtro da média
gray2 = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY) 
num_linhas = img_cinza.shape[0]
num_colunas = img_cinza.shape[1]
tamanho_mascara = (3,3)
x1 = int(tamanho_mascara[0]/2)
y1 = int(tamanho_mascara[1]/2)

for x in range(num_linhas):
    for y in range(num_colunas):
        mascara = np.ones(tamanho_mascara)

        for i in range(-x1, x1+1):
            for j in range(-y1, y1+1):
                # Quando a coordenada for fora do vetor da imagem, é ignorado
                if (x - i < 0 or y - j < 0) or (x - i >= num_linhas or y - j >= num_colunas):
                    mascara[i][j] = 0
                    continue
                mascara[i][j] = img_cinza[x - i][y - j] * mascara[i][j]

        media = np.mean(mascara.tolist())
        gray2[x][y] = media

nome_imagem = 'b-filtro da media.png'
print('Filtro da media aplicado...')
print('Imagem salva: {}'.format(nome_imagem))
cv.imwrite(nome_imagem, gray2)

# c) Aplicar filtro da mediana
gray3 = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY) 
for x in range(num_linhas):
    for y in range(num_colunas):
        mascara = np.ones(tamanho_mascara)

        for i in range(-x1, x1+1):
            for j in range(-y1, y1+1):
                # Quando a coordenada for fora do vetor da imagem, é ignorado
                if (x - i < 0 or y - j < 0) or (x - i >= num_linhas or y - j >= num_colunas):
                    mascara[i][j] = 0
                    continue
                mascara[i][j] = img_cinza[x - i][y - j] * mascara[i][j]

        mediana = np.median(mascara.tolist())
        gray3[x][y] = mediana

# d) Aplicar filtro Gaussiano
gray4 = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY) 
for x in range(num_linhas):
    for y in range(num_colunas):

        mascara = mascara_gaussiana(tamanho_mascara).astype(dtype=np.uint16)
        soma = 0

        # total_pesos = Soma dos pesos horizontais x soma dos pesos verticais
        total_pesos = sum(mascara[0][:]) * sum(mascara[:][0])

        for i in range(-x1, x1+1):
            for j in range(-y1, y1+1):
                # Quando a coordenada for fora do vetor da imagem, é ignorado
                if (x + i < 0 or y + j < 0) or (x + i >= num_linhas or y + j >= num_colunas):
                    continue
                soma += img_cinza[x + i][y + j] * mascara[i + x1][j + y1]

        # Calculando a media ponderada
        gaussiano = round(soma/total_pesos)
        gray4[x][y] = gaussiano

cv.waitKey(0)
cv.destroyAllWindows()