from PyQt5 import QtWidgets

class Gerenciamento_Telas(QtWidgets.QWidget):
    def __init__(self, app):
        super().__init__()  
        self.app = app          
    
    def carrega_telas(self, tela: object, backend: object=None, dimensoes: tuple[int, int]=None, tela_cheia: bool=False, api: object=None):
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
            self.backend = backend(self.ui, api)           