# -*- coding: utf-8 -*-

import numpy as np
import cv2

# Função para calcular Kmeans
def computKmeans(image, K, numInt):
    
    Z = image.reshape((-1,3))
    Z = np.float32(Z)    
    
    # Define criteria e K
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, numInt, 0.1)
    K = K
    
    # Aplica Kmeans
    _, labels, centroides = cv2.kmeans(Z, K, None, criteria, numInt, cv2.KMEANS_RANDOM_CENTERS)
    
    # Converte de volta a uint8 e monta a imagem
    centroides = np.uint8(centroides)
    res = centroides[labels.flatten()]
    imagemFinal = res.reshape((image.shape))
    
    return imagemFinal

def main():
    
    # Ler a imagem
    img = cv2.imread('mario.jpg')
    img2 = cv2.imread('mario8bits')

    # Chama a função
    img2 = computKmeans(img, 8, 8)
    newImg = computKmeans(img2, 256, 40)

    cv2.imshow('Original', img)
    cv2.imshow('8 bits', img2)
    cv2.imshow('8 bits to 256 colors', newImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()