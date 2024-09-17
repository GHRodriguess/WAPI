import sys
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QTimer, pyqtSignal
import threading

from frontend.py.tela_loading.tela_loading import Ui_Tela_Loading
from frontend.py.tela_principal.tela_principal import Ui_Tela_Principal
from frontend.py.tela_principal.adiciona_acao.adiciona_acao import Ui_Adiciona_Acao
from frontend.py.tela_principal.erros.erros import Ui_Tela_Erros
from frontend.py.conexao.tela_conexao import Ui_Tela_Conexao
from frontend.py.contatos.tela_contatos import Ui_Tela_Contatos
from frontend.py.contatos.adiciona_contatos.tela_adiciona_contatos import Ui_Adiciona_Contatos
from frontend.py.contatos.adiciona_grupos.tela_adiciona_grupos import Ui_Adiciona_Grupos

from backend.gerenciamento_telas import Gerenciamento_Telas
from backend.whatsapp import WhatsApp
from backend.tela_principal.principal import Principal
from backend.tela_principal.adiciona_acao.adiciona_acao import Adiciona_Acao
from backend.tela_principal.erros.erros import Erros
from backend.conexao.conexao import Conexao
from backend.contatos.contatos import Contatos
from backend.contatos.adiciona_contatos_grupos.adiciona_contatos_grupos import Adiciona_Contatos_Grupos
from backend.gerenciamento_tarefas import Tarefas


class App(QtWidgets.QMainWindow):
    api_ready = pyqtSignal()
    resultados_ready = pyqtSignal() 
    
    def __init__(self):
        super().__init__() 
        self.configura_diretorio_aplicacao()
        self.setCentralWidget(QtWidgets.QWidget())  
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout()) 
        self.telas = Gerenciamento_Telas(self)   
        self.api_ready.connect(self.api_pronta)    
        self.telas.carrega_telas(tela=Ui_Tela_Loading)  
        QTimer.singleShot(1000, self.inicia_api)  
        
    def inicia_api(self):  
        def roda_api():
            try:
                self.api = WhatsApp()
            except Exception as e:                
                os.system("taskkill /f /im chrome.exe")                
                roda_api()
            self.api_ready.emit()             
        self.api_thread = threading.Thread(target=roda_api)
        self.api_thread.start()
        
    def api_pronta(self):
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
            self.telas.carrega_telas(tela=Ui_Tela_Principal, backend=Principal, dimensoes=(800,600),tela_cheia=True,parametros=[self.api])
        else:            
            self.telas.carrega_telas(tela=Ui_Tela_Principal, backend=Principal, parametros=[self.api])
        
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_status_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        self.ui.botao_adiciona_item.clicked.connect(lambda: self.telas.carrega_telas(tela=Ui_Adiciona_Acao, segunda_tela=True, backend=Adiciona_Acao, parametros=["propria_janela", self.backend]))
        self.backend.verifica_conexao()        
        self.resultados_ready.connect(self.processa_resultados) 
        self.ui.botao_executar.clicked.connect(self.executa_mensagens)

    def executa_mensagens(self):  
        self.ui.botao_executar.setText("EXECUTANDO") 
        self.ui.botao_executar.setEnabled(False)
        self.thread_envia_mensagens = threading.Thread(target=self.run_envia_mensagens)
        self.thread_envia_mensagens.start()

    def run_envia_mensagens(self):        
        retornos = self.backend.envia_mensagens()        
        self.resultados = retornos    
        self.resultados_ready.emit()    

    def processa_resultados(self):         
        if self.resultados:
            if self.resultados is not None:                                                    
                    self.telas.carrega_telas(tela=Ui_Tela_Erros, segunda_tela=True, backend=Erros, parametros=["propria_janela", self.backend], tela_cheia=True)                        
        try:
            self.ui.botao_executar.setText("EXECUTAR") 
            self.ui.botao_executar.setEnabled(True)
        except:
            pass

    def carrega_tela_conexao(self):
        self.telas.carrega_telas(tela=Ui_Tela_Conexao, backend=Conexao,parametros=[self.api])
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)
        self.backend.verifica_conexao()
        
    def carrega_tela_contatos(self):
        self.telas.carrega_telas(tela=Ui_Tela_Contatos, backend=Contatos,parametros=[self.api])
        self.ui = self.telas.ui
        self.backend = self.telas.backend
        self.ui.botao_home.clicked.connect(self.carrega_tela_principal)
        self.ui.botao_contatos.clicked.connect(self.carrega_tela_contatos)        
        self.ui.botao_conexao.clicked.connect(self.carrega_tela_conexao)        
        self.ui.botao_adicionar_contato.clicked.connect(lambda: self.carrega_tela_adiciona_contatos_grupos('contato'))
        self.ui.botao_adicionar_grupo.clicked.connect(lambda: self.carrega_tela_adiciona_contatos_grupos('grupo'))        
        self.backend.verifica_conexao()
        self.backend.rodando()

    def carrega_tela_adiciona_contatos_grupos(self, tipo):
        try:
            self.telas.backend_2.fecha_janela()
        except:
            pass
        if tipo == "contato":
            self.telas.carrega_telas(tela=Ui_Adiciona_Contatos, segunda_tela=True, backend=Adiciona_Contatos_Grupos, parametros=["propria_janela", self.backend, tipo])
            self.telas.ui_2.botao_adicionar_grupo.clicked.connect(lambda: self.carrega_tela_adiciona_contatos_grupos('grupo'))
        elif tipo == 'grupo':
            self.telas.carrega_telas(tela=Ui_Adiciona_Grupos, segunda_tela=True, backend=Adiciona_Contatos_Grupos, parametros=["propria_janela", self.backend, tipo])
            self.telas.ui_2.botao_adicionar_contato.clicked.connect(lambda: self.carrega_tela_adiciona_contatos_grupos('contato'))
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())    
