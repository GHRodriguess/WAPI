class Adiciona_Acao():
    def __init__(self, ui, janela, backend):
        self.ui = ui
        self.janela = janela
        self.backend = backend
        self.conecta_widgets()
        
    def conecta_widgets(self):
        self.ui.mensagem.textChanged.connect(lambda: self.atualiza_estado_botao())
        self.ui.botao_cancelar.clicked.connect(lambda: self.janela.close())
        self.ui.botao_adicionar.clicked.connect(lambda: self.adicionar())
        
    def adicionar(self):
        mensagem = self.ui.mensagem.text()
        self.backend.adiciona_itens(f"""Mensagem
{mensagem}""")
        self.janela.close()
        
        
    def atualiza_estado_botao(self):
        if self.ui.mensagem.text():
            self.ui.botao_adicionar.setEnabled(True)
        else:
            self.ui.botao_adicionar.setEnabled(False)