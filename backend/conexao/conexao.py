import threading

class Conexao():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.verifica_conexao()
        self.gerencia_qrcode()
    
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
    
    def gerencia_qrcode(self):
        self.api_thread = threading.Thread(target=lambda: self.api.monitora_qrcode(self.ui, self))
        self.api_thread.daemon = True  
        self.api_thread.start()