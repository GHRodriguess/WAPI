from PyQt5 import QtWidgets
import os
from backend.database import Database

class Adiciona_Contatos():
    def __init__(self, ui, janela, backend_contatos):
        self.ui = ui
        self.janela = janela
        self.planilha = None
        self.backend = backend_contatos
        self.database = Database(os.path.join(os.getenv("APPDATA"), "API WhatsApp", "database.db"))
        self.conecta_widgets()        
        
    def conecta_widgets(self):
        self.ui.botao_inserir_planilha.clicked.connect(lambda: self.inserir_planilha()) 
        self.ui.botao_cancelar.clicked.connect(lambda: self.janela.close())
        self.ui.botao_adicionar.clicked.connect(lambda: self.adicionar())
        self.ui.nome_contato.textChanged.connect(lambda: self.atualiza_status_botao_salvar())
        self.ui.numero_contato.textChanged.connect(lambda: self.atualiza_status_botao_salvar())
        
    def atualiza_status_botao_salvar(self):
        nome_contato = self.ui.nome_contato.text().strip()
        numero_contato = self.ui.numero_contato.text().strip()
        if nome_contato and numero_contato or self.planilha:
            self.ui.botao_adicionar.setEnabled(True)
        else:
            self.ui.botao_adicionar.setEnabled(False) 
    
    
    def inserir_planilha(self):
        self.planilha, _ = QtWidgets.QFileDialog.getOpenFileName(self.janela, "Selecionar Planilha", "", "Arquivos XLSX (*.xlsx)")
        self.atualiza_status_botao_salvar()
        
    def adicionar(self):
        nome_contato = self.ui.nome_contato.text().strip()
        numero_contato = self.ui.numero_contato.text().strip()
        if not (nome_contato and numero_contato):   
            print("Ler planilha tirar os dados contato")
            self.le_planilha()        
        else:
            contato_confianca = self.ui.contato_confianca.isChecked()
            if contato_confianca:
                self.verifica_contatos_confianca()
            self.database.inserir('contatos', ['nome', 'numero', 'contato_confianca'], [nome_contato, numero_contato,contato_confianca])
        self.janela.close()
        self.backend.atualiza_tabela()
        
    def le_planilha(self):
        print("Lendo planilha e extraindo os dados")
        
    def verifica_contatos_confianca(self):
        contatos_confianca = self.database.fetch_one('contatos', condition='contato_confianca = ?', params=(True,))
        if contatos_confianca:            
            self.database.atualizar('contatos', {'contato_confianca': False}, "id = ?", (contatos_confianca[0],))