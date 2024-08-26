import threading
import os

from backend.database import Database

class Contatos():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.verifica_conexao()
        self.database = Database(os.path.join(os.getenv("APPDATA"), "API WhatsApp", "database.db"))
        self.database.cria_tabela('contatos', ["id INTEGER PRIMARY KEY AUTOINCREMENT", "nome_numero TEXT NOT NULL"])
        
        
    def verifica_conexao(self):
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
    

