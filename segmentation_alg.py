from PIL import Image, ImageFilter, ImageEnhance
from itertools import product
import numpy as np


import cv2

# rio = (12, 47, 206, 255)
# plantacao = (68, 109, 66, 255)
# floresta = (8, 183, 0, 255)
queimada = (168, 28, 13, 255)
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



#Binarizar com regras
def encontrar_pixels_de_queimadas(img):
    pix = img.load()

    width, height = img.size
    pixels_queimadas = []
    
    for y, x in product(range(height), range(width)):
        r,g,b,a = pix[x,y]
        if(r > 63 and r < 114 and g > 63 and g < 117 and b > 40 and b < 92):
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



def main(nome_imagem):
    # nome_imagem = "area-queimada.png"
    print(nome_imagem)
    img = abrir_imagem(nome_imagem)
    
    img2 = encontrar_pixels_de_queimadas(img)
    img2.save("generated_images/segmentada-cores.png")


    img3 = diferenca(img2)
    img3.save('generated_images/diferenca.png')
    
    img4 = cv2.imread('generated_images/diferenca.png',0)
    kernel = np.ones((4,4),np.uint8)

    opening = cv2.morphologyEx(img4, cv2.MORPH_OPEN, kernel)
    cv2.imwrite('resultado_final.png', opening)
    return 'resultado_final.png'

    
    # mostrar_imagem(nome_imagem+"-segmentada"+".png")

# if __name__ == '__main__':
#     main()