# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog 
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np


class GrabCutGUI(tk.Frame):
    def __init__(self, master = None):
        # Construtor da classe Frame
        tk.Frame.__init__(self, master)
        
        # Inicializar a interface gráfica
        self.iniciaUI()
    
    def iniciaUI(self):
        # Preparando a janela
        self.master.title("Janela da Imagem Segmentada")
        self.pack()
        
        # Computa as ações do mouse
        self.computaAcoesDoMouse()
        
        # Carregando imagem do disco
        self.imagem = self.carregaImagem()

        # Cria o Canvas
        self.canvas = tk.Canvas(self.master, height = self.imagem.height(),width = self.imagem.width(), cursor = 'cross')
        self.canvas.create_image(0, 0, image = self.imagem, anchor = tk.NW)
        self.canvas.image = self.imagem
        self.canvas.pack()
        
    def computaAcoesDoMouse(self):
        self.startX = None
        self.startY = None
        self.rect   = None
        self.rectangleReady = None
        
        self.master.bind('<ButtonPress-1>', self.callbackBotaoPrecionado)
        self.master.bind('<B1-Motion>', self.callbackBotaoPrecionadoEmMovimento)
        self.master.bind('<ButtonRelease-1>', self.callbackBotaoSolto)
        
    def callbackBotaoSolto(self, event):
        if self.rectangleReady:
            # Cria uma nova janela
            windowGrabcut = tk.Toplevel(self.master)
            windowGrabcut.wm_title('Segmentação')
            windowGrabcut.minsize(width = self.imagem.width(), height = self.imagem.height())
            
            # Cria um canvas para essa nova janela
            canvasGrabcut = tk.Canvas(windowGrabcut, width = self.imagem.width(), height = self.imagem.height())
            canvasGrabcut.pack()
            
            # Aplicar grabcut na imagem
            mask = np.zeros(self.imagemOpenCV.shape[:2], np.uint8)
            rectGcut = (int(self.startX), int(self.startY), int(event.x - self.startX), int(event.y - self.startY))
            fundoModel = np.zeros((1, 65), np.float64)
            objModel = np.zeros((1, 65), np.float64)
            
            # Cria uma copia da imagem 
            imagemNova = self.imagemOpenCV.copy()
            
            # Invocar grabcut
            cv2.grabCut(self.imagemOpenCV, mask, rectGcut, fundoModel, objModel, 5, cv2.GC_INIT_WITH_RECT)
            
            # Prepara a imagem final
            maskFinal = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            imgFinal = self.imagemOpenCV * maskFinal[:,:,np.newaxis]
            
            # Subitrair da imagem copiada a imagem com Grabcut.(Como o resultado temos o fundo da imagem)
            imagemNova = imagemNova - imgFinal
            
            # Aplicar o filtro na imagem de fundo
            imagemNova = cv2.blur(imagemNova, (10,10))
            
            # Adicionar a imagem do grabcut no fundo borrado
            imgFinal = cv2.add(imgFinal, imagemNova)
            
            # Converter de opencv para Tkinter
            imgFinal = cv2.cvtColor(imgFinal, cv2.COLOR_BGR2RGB)
            imgFinal = Image.fromarray(imgFinal)
            imgFinal = ImageTk.PhotoImage(imgFinal)
            
            # Inserir a imagem no canvas
            canvasGrabcut.create_image(0, 0, image = imgFinal, anchor = tk.NW)
            canvasGrabcut.image = imgFinal
            
            
    def callbackBotaoPrecionadoEmMovimento(self, event):
        currentX = self.canvas.canvasx(event.x)
        currentY = self.canvas.canvasy(event.y)
        
        # Atualiza o retângulo
        self.canvas.coords(self.rect, self.startX, self.startY, currentX, currentY)
        
        # Verifica se existe um retângulo
        self.rectangleReady = True
        
    def callbackBotaoPrecionado(self, event):
        self.startX = self.canvas.canvasx(event.x)
        self.startY = self.canvas.canvasy(event.y)
        
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline = 'red')
        
    def carregaImagem(self):
        caminhoDaImagem = filedialog.askopenfilename()
              
        self.imagemOpenCV = cv2.imread(caminhoDaImagem)
     
        # Converte BGR to RGB
        image = cv2.cvtColor(self.imagemOpenCV, cv2.COLOR_BGR2RGB)

        
        # Convert de OpenCV para PIL
        image = Image.fromarray(image)
             
        # Converte de PIL para PhotoImage
        image = ImageTk.PhotoImage(image)
             
        return image
             
        
def main():
    
    # Inicializar a Tkinter
    root = tk.Tk()
    
    # Cria a aplicação
    appcut = GrabCutGUI(root)
    
    # Cria o loop do programa
    appcut.mainloop()    

if __name__ == '__main__':
    main()