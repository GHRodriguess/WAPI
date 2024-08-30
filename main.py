import sys
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QTimer
import threading

from frontend.py.tela_principal.tela_principal import Ui_Tela_Principal
from frontend.py.tela_principal.adiciona_acao.adiciona_acao import Ui_Adiciona_Acao
from frontend.py.conexao.tela_conexao import Ui_Tela_Conexao
from frontend.py.contatos.tela_contatos import Ui_Tela_Contatos
from frontend.py.contatos.adiciona_contatos.tela_adiciona_contatos import Ui_Adiciona_Contatos

from backend.gerenciamento_telas import Gerenciamento_Telas
from backend.whatsapp import WhatsApp
from backend.tela_principal.principal import Principal
from backend.tela_principal.adiciona_acao.adiciona_acao import Adiciona_Acao
from backend.conexao.conexao import Conexao
from backend.contatos.contatos import Contatos
from backend.contatos.adiciona_contatos.adiciona_contatos import Adiciona_Contatos
from backend.gerenciamento_tarefas import Tarefas


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.configura_diretorio_aplicacao()
        self.setCentralWidget(QtWidgets.QWidget())  
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())    
        self.api = WhatsApp()  
        self.telas = Gerenciamento_Telas(self)
        self.tarefas = Tarefas(self.api)
        self.carrega_tela_principal(primeira_vez=True)

    def closeEvent(self, event):  
        event.accept()        
        QTimer.singleShot(1, self.fecha_navegador)
        

    def configura_diretorio_aplicacao(self):
        diretorio = os.path.join(os.getenv('APPDATA'), 'API WhatsApp')
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def fecha_navegador(self):
        if hasattr(self, 'api') and self.api:
            self.api.fecha_navegador()
    
    def carrega_tela_principal(self, primeira_vez=False):
        if primeira_vez:
            self.telas.carrega_telas(tela=Ui_Tela_Principal, backend=Principal, dimensoes=(800,600),parametros=self.api)
        else:            
            self.telas.carrega_telas(tela=Ui_Tela_Principal, backend=Principal, parametros=self.api)
        
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_status_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        self.ui.botao_adiciona_item.clicked.connect(lambda: self.telas.carrega_telas(tela=Ui_Adiciona_Acao, segunda_tela=True, backend=Adiciona_Acao, parametros=["propria_janela", self.backend]))
        self.backend.verifica_conexao()
        #if self.api.conectado:            
        #    if not self.tarefas.rodando:
        #        numeros = ["+55 42 99846-0016", "+55 44 3031-3571", "+55 44 98448-6131"]
        #        mensagens = ["Essa mensagem foi enviada por uma API do WhatsApp.", "Botei agora para você não se assustar"]
        #        tarefas = []
        #        for numero in numeros:
        #            tarefa_atual = [
        #                ["pesquisa_contato", numero],                    
        #                ]       
        #            for mensagem in mensagens:
        #                tarefa_atual.append(["envia_mensagem", mensagem])
        #            tarefas.extend(tarefa_atual)
        #           
        #        self.tarefas.gerencia_tarefas_segundo_plano(tarefas)
            
    def carrega_tela_conexao(self):
        self.telas.carrega_telas(tela=Ui_Tela_Conexao, backend=Conexao,parametros=self.api)
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        self.backend.verifica_conexao()
        
    def carrega_tela_contatos(self):
        self.telas.carrega_telas(tela=Ui_Tela_Contatos, backend=Contatos,parametros=self.api)
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)        
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)        
        self.ui.botao_adicionar_contato.clicked.connect(lambda: self.telas.carrega_telas(tela=Ui_Adiciona_Contatos, segunda_tela=True, backend=Adiciona_Contatos, parametros=["propria_janela", self.backend]))
        self.backend.verifica_conexao()
        self.backend.rodando()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
