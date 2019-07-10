from PIL import Image, ImageFilter, ImageEnhance
from itertools import product
import numpy as np


import cv2

# rio = (12, 47, 206, 255)
# plantacao = (68, 109, 66, 255)
# floresta = (8, 183, 0, 255)
queimada = (168, 28, 13, 255)
branco = (255,255,255, 255)
caminho = "/home/fernando/Documentos/UFT/9 Período/Estagio Supervisionado/Estagio/generated_images/"

#Abre uma imagem
def abrir_imagem(nome_img):
    return Image.open(nome_img)

#Converte a imagem para escala de cinza
def escala_de_cinza(img):
    return img.convert('L')

def gerar_matriz (n_linhas, n_colunas):
    matriz = np.zeros((n_linhas, n_colunas), dtype=np.str)
    return matriz

def imprimir_matriz(matriz):
    print(np.asarray(matriz))

def matriz_da_imagem(img):
    return np.asarray(img.convert('L'))

def nova_imagem(img):
    new_img = Image.new('RGB', (img.width, img.height), color='black')
    # new_img.save('nova_imagem.png')
    # new_img.show()
    return new_img


def imprimir_valores(img):
    pix = img.load()
    width, height = img.size
    for y, x in product(range(height), range(width)):
        if pix[x,y] != 0:
            time.sleep(0.1)
        print("x: {}| y: {} = {}".format(x, y, pix[x,y]))

def mostrar_imagem(nome_img):
    call(["ristretto", nome_img])

# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------



# Binarizar com regras
def encontrar_pixels_de_queimadas(img, segmentacao):
    pix = img.load()

    width, height = img.size
    pixels_queimadas = []
    
    #Segmentacao de Palmas
    if segmentacao == 1:
        for y, x in product(range(height), range(width)):
            r,g,b,a = pix[x,y]
            if(r > 63 and r < 114 and g > 63 and g < 117 and b > 40 and b < 99):
                pixels_queimadas.append((x,y))
    
    #Segmentacao do resto
    if segmentacao == 2:
        for y, x in product(range(height), range(width)):
            r,g,b,a = pix[x,y]
            if(r > 80 and r < 190 and g > 35 and g < 132 and b > 110 and b < 215):
                pixels_queimadas.append((x,y))
    

    for pixel in pixels_queimadas:
        x,y = pixel
        pix[x,y] = queimada
    

    return img



def diferenca(img):
    new_img = nova_imagem(img)
    pix  = img.load()
    pix2 = new_img.load()


    width, height = img.size
    

    for y, x in product(range(height), range(width)):
        if pix[x,y] == queimada:
            pix2[x,y] = (255,255,255)
        else:
            pix2[x,y] = (0,0,0)
    
    # new_img.save('diferenca.png')


    return new_img


def area_de_queimada(img):
    pix  = img.load()
    width, height = img.size
    qtd_pontos = 0
    
    for y, x in product(range(height), range(width)):
        # print ("pix[x,y] {}".format(pix[x,y]))
        if pix[x,y] == 255: # se for uma area detectada com regiao de queimada
            qtd_pontos +=1

    #cada pixel equivale a 73 metros²
    return qtd_pontos*7

def main(nome_imagem, abertura, segmentacao):
    # nome_imagem = "area-queimada.png"
    aux = nome_imagem
    nome_imagem = "static/"+nome_imagem
    print("Nome image: {}".format(nome_imagem))
    print("Open par: {}".format(abertura))
    print("Segm par: {}".format(segmentacao))
    
    img = abrir_imagem(nome_imagem)
    
    img2 = encontrar_pixels_de_queimadas(img, segmentacao)
    img2.save("static/segmentada-cores.png")


    img3 = diferenca(img2)
    img3.save('static/diferenca.png')
    
    img4 = cv2.imread('static/diferenca.png',0)
    kernel = np.ones((abertura,abertura),np.uint8)

    opening = cv2.morphologyEx(img4, cv2.MORPH_OPEN, kernel)
    nome = "static/resultado"+str(abertura)+str(segmentacao)+aux
    print("Nome local salvar: {}".format(nome))
    cv2.imwrite(nome, opening)
    
    # img5 = abrir_imagem(nome)
    area = area_de_queimada(abrir_imagem(nome))
    print("Area de queimada: {}m²".format(area))
    return area

    # return 'static/resultado_final.png'

    
    # mostrar_imagem(nome_imagem+"-segmentada"+".png")

# if __name__ == '__main__':
#     main()