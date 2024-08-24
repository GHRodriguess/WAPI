class Principal():
    def __init__(self, ui, api):
        self.ui = ui
        self.api = api
        self.verifica_conexao()
    
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