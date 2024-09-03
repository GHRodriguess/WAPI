from PyQt5 import QtWidgets, QtCore
import sys

class Gerenciamento_Telas(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()  
        self.app = app          
    
    def carrega_telas(self, tela: object=None, segunda_tela: bool=False, backend: object=None, dimensoes: tuple[int, int]=None, tela_cheia: bool=False, parametros: object=None):
        if not segunda_tela:
            if dimensoes is None:            
                largura = self.app.width()
                altura = self.app.height()               
            else: 
                largura = dimensoes[0]
                altura = dimensoes[1]            
            self.ui = tela()
            self.ui.setupUi(self.app)        
            self.app.resize(largura, altura)            
            if tela_cheia:
                self.app.showMaximized()                
            if backend:
                if parametros:
                    if 'propria_janela' in parametros:
                        index = parametros.index('propria_janela')
                        parametros[index] = self.app                        
                    self.backend = backend(self.ui, *parametros)
                else:
                    self.backend = backend(self.ui)                             
        else:
            self.app2 = QtWidgets.QWidget()
            if dimensoes is None:
                largura = self.app2.width()
                altura = self.app2.height()
            else:
                largura = dimensoes[0]
                altura = dimensoes[1]                
            self.ui_2 = tela()
            self.ui_2.setupUi(self.app2)
            self.app2.resize(largura, altura)
            self.app2.show()            
            self.app2.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            if tela_cheia:
                self.app2.showMaximized()                
            if backend:
                if parametros:
                    if 'propria_janela' in parametros: 
                        index = parametros.index('propria_janela')    
                        parametros[index] = self.app2                   
                    self.backend_2 = backend(self.ui_2, *parametros) 
                else:
                    self.backend_2 = backend(self.ui_2)
