from PyQt5 import QtWidgets
import os
import pandas as pd
import re
from backend.database import Database

class Adiciona_Contatos_Grupos():
    def __init__(self, ui, janela, backend_contatos, tipo):
        self.ui = ui
        self.janela = janela
        self.planilha_dir = None
        self.backend = backend_contatos
        self.tipo = tipo       
        self.database = Database(os.path.join(os.getenv("APPDATA"), "API WhatsApp", "database.db"))
        self.conecta_widgets()        
        
    def conecta_widgets(self):
        self.ui.botao_inserir_planilha.clicked.connect(lambda: self.inserir_planilha()) 
        self.ui.botao_cancelar.clicked.connect(lambda: self.janela.close())
        self.ui.botao_adicionar.clicked.connect(lambda: self.adicionar())
        self.ui.nome.textChanged.connect(lambda: self.atualiza_status_botao_salvar())
        if self.tipo == "contato":
            self.ui.numero_contato.textChanged.connect(lambda: self.atualiza_status_botao_salvar())            
        
    def atualiza_status_botao_salvar(self):
        if self.tipo == "contato":
            nome_contato = self.ui.nome.text().strip()        
            numero_contato = self.ui.numero_contato.text().strip()
            if (nome_contato and numero_contato) or (self.planilha_dir and nome_contato and numero_contato):
                self.ui.botao_adicionar.setEnabled(True)
            else:
                self.ui.botao_adicionar.setEnabled(False) 
        elif self.tipo == "grupo":
            nome_grupo = self.ui.nome.text().strip() 
            if nome_grupo or (self.planilha_dir and nome_grupo): 
                self.ui.botao_adicionar.setEnabled(True)
            else:
                self.ui.botao_adicionar.setEnabled(False) 
    
    
    def inserir_planilha(self):
        self.planilha_dir, _ = QtWidgets.QFileDialog.getOpenFileName(self.janela, "Selecionar Planilha", os.path.join(os.path.expanduser("~"), "Desktop"), "Arquivos XLSX (*.xlsx)")
        self.atualiza_status_botao_salvar()
        
    def adicionar(self):
        if self.tipo == "contato":
            nome_contato = self.ui.nome.text().strip()
            numero_contato = self.ui.numero_contato.text().strip()
            if self.planilha_dir:
                try:
                    self.le_planilha()    
                except Exception as e:
                    print(e)
                    self.fecha_janela()               
            else:
                contato_confianca = self.ui.contato_confianca.isChecked()
                if contato_confianca:
                    self.verifica_contatos_confianca()
                self.database.inserir('contatos', ['nome', 'numero', 'tipo', 'contato_confianca'], [nome_contato, numero_contato, 'Contato', contato_confianca])
        elif self.tipo == "grupo":
            nome_grupo = self.ui.nome.text().strip()
            contato_confianca = False
            if self.planilha_dir:
                try:
                    self.le_planilha()
                except Exception as e:
                    print(e)
                    self.fecha_janela()
            else:
                self.database.inserir('contatos', ['nome', 'tipo', 'contato_confianca'], [nome_grupo, 'Grupo', contato_confianca])
        self.fecha_janela()
        self.backend.atualiza_tabela()
        
    def le_planilha(self):
        planilha = pd.read_excel(self.planilha_dir)   
        if self.tipo == "contato":     
            coluna_nome_contato = self.ui.nome.text().strip()
            coluna_numero_contato = self.ui.numero_contato.text().strip()
            dados_contatos = self.coleta_numeros_planilha(planilha, coluna_nome_contato, col_num=coluna_numero_contato)           
        elif self.tipo == "grupo":
            coluna_nome_contato = self.ui.nome.text().strip()
            dados_contatos = self.coleta_numeros_planilha(planilha, coluna_nome_contato)
            
        for dado in dados_contatos:
            nome_contato = dado[0]
            numero_contato = dado[1]
            contato_confianca = False
            self.database.inserir('contatos', ['nome', 'numero', 'tipo', 'contato_confianca'], [nome_contato, numero_contato, self.tipo.capitalize(),contato_confianca])
            
        self.fecha_janela()
        self.backend.atualiza_tabela()  
            
    def coleta_numeros_planilha(self, planilha, col_nom:str, col_num:str=None):
        dados_contatos = []
        planilha.columns = map(str.lower, planilha.columns)        
        col_nom = col_nom.lower()
        if col_num:
            col_num = col_num.lower()
            for index, row in planilha.iterrows():
                e_numero, numero = self.verifica_numero(row[col_num])
                if e_numero:
                    dados_contatos.append([row[col_nom], numero])
        else:
            for index, row in planilha.iterrows():
                dados_contatos.append([row[col_nom], None])
                
        return dados_contatos
    
    def verifica_numero(self, numero):
        if pd.isna(numero):
            return False, None
        if re.search(r'[a-zA-Z]', numero):
            numero = re.sub(r'\D', '', numero)
            if not numero:
                return False, None
            else:
                return True, numero   
        else: 
            return True, numero
            
    def verifica_contatos_confianca(self):
        contatos_confianca = self.database.fetch_one('contatos', condition='contato_confianca = ?', params=(True,))
        if contatos_confianca:            
            self.database.atualizar('contatos', {'contato_confianca': False}, "id = ?", (contatos_confianca[0],))
            
    def fecha_janela(self):
        self.janela.close()