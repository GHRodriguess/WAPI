import sys
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QTimer

from frontend.py.tela_principal.tela_principal import Ui_Tela_Principal
from frontend.py.conexao.tela_conexao import Ui_Tela_Conexao
from frontend.py.contatos.tela_contatos import Ui_Tela_Contatos

from backend.gerenciamento_telas import Gerenciamento_Telas
from backend.whatsapp import WhatsApp
from backend.tela_principal.principal import Principal
from backend.conexao.conexao import Conexao
from backend.gerenciamento_tarefas import Tarefas

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.configura_diretorio_aplicacao()
        self.telas = Gerenciamento_Telas(self)
        self.api = WhatsApp()
        self.tarefas = Tarefas(self.api)
        self.setCentralWidget(QtWidgets.QWidget())  
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())  
        self.carrega_tela_principal()

    def closeEvent(self, event):        
        event.accept()        
        QTimer.singleShot(1, self.api.fecha_navegador)

    def configura_diretorio_aplicacao(self):
        diretorio = os.path.join(os.getenv('APPDATA'), 'API WhatsApp')
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)    

    def carrega_tela_principal(self):
        self.telas.carrega_telas(Ui_Tela_Principal, backend=Principal, api=self.api)
        self.ui = self.telas.ui
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        if self.api.conectado:
            self.tarefas.gerencia_tarefas_segundo_plano([
                ["pesquisa_contato", "Gabriel Henrique Rodrigues"],
                ["envia_mensagem", "Essa mensagem foi enviada por uma API do WhatsApp."],                
                ])
        
    def carrega_tela_conexao(self):
        self.telas.carrega_telas(Ui_Tela_Conexao, backend=Conexao,api=self.api)
        self.ui = self.telas.ui
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        
    def carrega_tela_contatos(self):
        self.telas.carrega_telas(Ui_Tela_Contatos)
        self.ui = self.telas.ui
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    
    sys.exit(app.exec())