import threading
import os
from backend.database import Database
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QModelIndex, QSortFilterProxyModel, QTimer, QRegularExpression
import os
import ast
import time
from tkinter import filedialog


from backend.database import Database

class Contatos():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.model = None
        self.arquivo_marcados = os.path.join(os.getenv("APPDATA"), "API WhatsApp", "marcados.txt")
        self.database = Database(os.path.join(os.getenv("APPDATA"), "API WhatsApp", "database.db"))
        self.database.cria_tabela('contatos', ["id INTEGER PRIMARY KEY AUTOINCREMENT", "nome TEXT NOT NULL", "numero TEXT NOT NULL","contato_confianca BOOLEAN NOT NULL"])
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.atualiza_estado_botao)
        self.atualiza_tabela()  

    def conecta_botoes(self):
        self.ui.selecionar_tudo.clicked.connect(lambda: self.seleciona_tudo('selecionar'))
        self.ui.limpar_tudo.clicked.connect(lambda: self.seleciona_tudo('limpar'))     
        self.ui.botao_remover_contato.clicked.connect(lambda: self.remove_contato())      
    
    def remove_contato(self):
        self.verificar_marcados()        
        for marcado in self.marcados:            
            self.database.delete("contatos", "nome = ?", (marcado[0],))
        self.atualiza_tabela()
    
    def verifica_conexao(self):   
        try:
            self.api.verifica_conexao(espera=False)     
        except Exception as e: 
            print(e)
            pass
        if self.api.conectado:
            texto_conectado = "conectado"            
        else:
            texto_conectado = "nao_conectado"            
        self.ui.botao_conexao.setStyleSheet(f"""
QPushButton{{
    icon: url(:/icons/{texto_conectado}.svg);
    background-color: transparent;
}}

QPushButton::hover{{
    icon: url(:/icons/{texto_conectado}_hover.svg);
    background-color: transparent;
}}""")
    

    def atualiza_tabela(self):
        if self.model:
            self.model.clear()
        self.model = QStandardItemModel()
        resultados = self.database.fetch_all("contatos", ["nome", "numero","contato_confianca"])
        if resultados:            
            self.model.setColumnCount(len(resultados[0]) + 1)
            headers = ["", "NOME", "NÚMERO", "CONTATO DE CONFIANÇA"]
            for col, header in enumerate(headers):
                self.model.setHeaderData(col, Qt.Horizontal, header)        
            
            for linha, texto in enumerate(resultados):
                self.ui.checkbox_item = QStandardItem()
                self.ui.checkbox_item.setCheckable(True)
                texto = list(texto) 
                marcado = self.verifica_salvo_em_marcados(texto)
                if marcado: 
                    self.ui.checkbox_item.setCheckState(Qt.Checked)   
                else:
                    self.ui.checkbox_item.setCheckState(Qt.Unchecked)               
                if texto[2] == 1:
                    texto[2] = "Contato de Confiança"
                else:
                    texto[2] = ""                      
                texto = [QStandardItem(str(item)) for item in texto]
                texto.insert(0, self.ui.checkbox_item)
                
                self.model.appendRow(texto)
                
            self.ui.tabela.setModel(self.model)  
            self.model.itemChanged.connect(lambda: self.timer.start(100))
        self.rodando()
    
    def rodando(self):
        self.conecta_botoes() 
        self.busca = QSortFilterProxyModel()
        self.busca.setSourceModel(self.model)
        self.busca.setFilterKeyColumn(1)
        self.busca.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self.ui.procura.textChanged.connect(lambda: self.filtra_planilha(self.ui.procura.text()))
        
    def filtra_planilha(self, busca):        
        reg_exp = QRegularExpression(busca)
        self.busca.setFilterRegularExpression(reg_exp)
        self.ui.tabela.setModel(self.busca)
        
    def verificar_marcados(self):
        self.marcados = []
        self.nao_encontrados = []

        for linha in range(self.model.rowCount()):
            item = self.model.item(linha, 0)
            if item.isCheckable() and item.checkState() == Qt.Checked:
                dados_linha = [self.model.item(linha, col).text() for col in range(1, self.model.columnCount())]
                self.marcados.append(dados_linha)
                
    def atualiza_estado_botao(self):
        self.verificar_marcados()
        if self.marcados:
            self.ui.botao_remover_contato.setEnabled(True)
        else:
            self.ui.botao_remover_contato.setEnabled(False)
        self.salva_marcados()
        
    def salva_marcados(self):
        with open(self.arquivo_marcados, "w") as arquivo:
            for marcado in self.marcados: 
                texto = f"{marcado[0]}, {marcado[1]}\n"
                arquivo.write(texto)
                
    def verifica_salvo_em_marcados(self, texto):        
        if os.path.isfile(self.arquivo_marcados):       
            marcados = []     
            with open(self.arquivo_marcados, "r") as arquivo:                
                for linha in arquivo.readlines():
                    nome, numero = linha.split(",")
                    marcados.append(nome)
                    marcados.append(numero)

            nome = texto[0] 
            if nome in marcados:                
                return True
            else:
                return False
        else:
            return False

    def seleciona_tudo(self, acao:str):        
        for linha_busca in range(self.busca.rowCount()):
            index_busca = self.busca.index(linha_busca, 0)
            index_procura = self.busca.mapToSource(index_busca)
            item = self.model.item(index_procura.row(), 0)
            if item.isCheckable():                
                if acao == "selecionar":
                    item.setCheckState(Qt.Checked)
                elif acao == "limpar":
                    item.setCheckState(Qt.Unchecked)