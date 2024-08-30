import os
from backend.gerenciamento_tarefas import Tarefas

class Principal():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.tarefas = Tarefas(self.api)
        self.verifica_conexao()
        self.verifica_contatos()
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
    
    def atualiza_estado_botao(self):   
        if self.api.conectado and self.contatos_selecionados and self.ui.acoes.count() > 0:
            self.ui.botao_executar.setEnabled(True)
        else:
            self.ui.botao_executar.setEnabled(False)
    
    def conecta_botoes(self):        
        self.ui.botao_remove_item.clicked.connect(lambda: self.remove_item())
        self.ui.botao_executar.clicked.connect(lambda: self.envia_mensagens())
                
    def adiciona_itens(self, item):
        self.ui.acoes.addItem(item)
        self.atualiza_estado_botao()
    
    def remove_item(self):
        item = self.ui.acoes.currentItem()
        if item:
            self.ui.acoes.removeItemWidget(item)
            self.ui.acoes.takeItem(self.ui.acoes.row(item))
            del item        
            self.atualiza_estado_botao()
        
    def envia_mensagens(self):
        numeros = self.coleta_numeros()
        mensagens = self.coleta_mensagens()   
        tarefas = self.gera_tarefas(numeros, mensagens)
        self.tarefas.gerencia_tarefas_segundo_plano(tarefas)
        
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
                mensagem = texto.split("\n")[-1]
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
            
        