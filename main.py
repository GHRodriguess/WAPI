import sys
from PyQt5 import QtWidgets, QtGui
import os
import traceback
import datetime

from frontend.py.tela_principal.tela_principal import Ui_Tela_Principal
from frontend.py.conexao.tela_conexao import Ui_Tela_Conexao

from backend.gerenciamento_telas import Gerenciamento_Telas
from backend.whatsapp import WhatsApp
from backend.tela_principal.principal import Principal
from backend.conexao.conexao import Conexao


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.configura_diretorio_aplicacao()
        self.telas = Gerenciamento_Telas(self)
        self.api = WhatsApp()
        self.setCentralWidget(QtWidgets.QWidget())  
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())  
        self.carrega_tela_principal()

    def configura_diretorio_aplicacao(self):
        diretorio = os.path.join(os.getenv('APPDATA'), 'API WhatsApp')
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)    

    def carrega_tela_principal(self):
        self.telas.carrega_telas(Ui_Tela_Principal, backend=Principal, api=self.api)
        self.ui = self.telas.ui
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        #self.ui.botao_contatos.clicked.connect(print("Tela Contatos"))
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        
    def carrega_tela_conexao(self):
        self.telas.carrega_telas(Ui_Tela_Conexao, backend=Conexao,api=self.api)
        self.ui = self.telas.ui
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        #self.ui.botao_contatos.clicked.connect(print("Tela Contatos"))
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())