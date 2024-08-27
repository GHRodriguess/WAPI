import threading

class Conexao():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api  
            
    def verifica_conexao(self):   
        try:
            self.api.verifica_conexao(espera=False)     
        except Exception as e: 
            print(e)
            pass
        if self.api.conectado:
            texto_conectado = "conectado"
            self.ui.qrcode.setText("VOCÊ JÁ SE CONECTOU")
        else:
            texto_conectado = "nao_conectado"
            self.gerencia_qrcode()
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