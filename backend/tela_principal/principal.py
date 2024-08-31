import os
import threading
from backend.gerenciamento_tarefas import Tarefas

class Principal():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.tarefas = Tarefas(self.api)
        self.arquivo_acoes = os.path.join(os.getenv("APPDATA"), "API WhatsApp", "acoes.txt")
        self.verifica_conexao()
        self.verifica_contatos()
        self.verifica_acoes_existentes()
        self.atualiza_estado_botao()
        self.conecta_botoes()
    
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
    
    def verifica_contatos(self):
        arquivos_marcados = os.path.join(os.getenv("APPDATA"), "API WhatsApp", "marcados.txt")
        if os.path.isfile(arquivos_marcados):
            with open(arquivos_marcados, 'r') as f:
                self.contatos_selecionados = f.read().splitlines()
        try:
            if self.contatos_selecionados:
                texto_contato = "contatos_selecionados"
            else:
                texto_contato = "sem_contatos_selecionados"
        except Exception as e:
            texto_contato = "sem_contatos_selecionados"
        self.ui.botao_status_contatos.setStyleSheet(f"""
QPushButton{{
	icon: url(:/icons/{texto_contato}.svg);
	background-color: transparent;
}}

QPushButton:hover{{
	icon: url(:/icons/{texto_contato}_hover.svg);
}}
""")
    
    def verifica_acoes_existentes(self):
        if os.path.isfile(self.arquivo_acoes):           
            with open(self.arquivo_acoes, 'r') as arquivo:                
                for linha in arquivo.readlines():  
                    if linha:  
                        if "\n" in linha:
                            linha = linha.replace("\n", "")                        
                        self.adiciona_itens(linha) 
    
    def atualiza_estado_botao(self):  
        self.salva_acoes() 
        if self.api.conectado and self.contatos_selecionados and self.ui.acoes.count() > 0:
            self.ui.botao_executar.setEnabled(True)
        else:
            self.ui.botao_executar.setEnabled(False)
    
    def conecta_botoes(self):        
        self.ui.botao_remove_item.clicked.connect(lambda: self.remove_item())        
                
    def adiciona_itens(self, item):
        mensagem = f"""Mensagem
{item}"""
        self.ui.acoes.addItem(mensagem)
        self.atualiza_estado_botao()        
        
        
    def salva_acoes(self):
        mensagens = self.coleta_mensagens()        
        with open(self.arquivo_acoes, "w") as arquivo:  
            for i, mensagem in enumerate(mensagens):
                if i != 0:
                    arquivo.write(f"\n{mensagem}")
                else:
                    arquivo.write(f"{mensagem}")
    
    def remove_item(self):
        item = self.ui.acoes.currentItem()
        if item:
            self.ui.acoes.removeItemWidget(item)
            self.ui.acoes.takeItem(self.ui.acoes.row(item))
            del item        
            self.atualiza_estado_botao()
        
    def envia_mensagens(self):
        if not self.tarefas.rodando:
            self.tarefas_event = threading.Event()
            numeros = self.coleta_numeros()
            mensagens = self.coleta_mensagens()   
            tarefas = self.gera_tarefas(numeros, mensagens)
            self.erros = self.tarefas.gerencia_tarefas_segundo_plano(tarefas)
            self.tarefas_event.set()
            
            return self.erros if self.erros else None
        
    def coleta_numeros(self):
        numeros = []    
        for item in self.contatos_selecionados:            
            nome, numero = item.split(",")
            numero = numero.strip()  
            numeros.append(numero)
        return numeros    
        
    def coleta_mensagens(self):
        mensagens = []        
        for i in range(self.ui.acoes.count()):
            item = self.ui.acoes.item(i)
            if item:                
                texto = item.text()  
                mensagem = texto.split("\n")[1]
                mensagens.append(mensagem)
        return mensagens    
    
    def gera_tarefas(self, numeros, mensagens):
        tarefas = []
        for numero in numeros:
            tarefa_atual = [
                ["pesquisa_contato", numero],
            ]
            for mensagem in mensagens:
                tarefa_atual.append(["envia_mensagem", mensagem])
            tarefas.extend(tarefa_atual)
                
        return tarefas
            
        