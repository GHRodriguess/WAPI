class Erros():
    def __init__(self, ui, janela, backend):
        self.ui = ui
        self.janela = janela
        self.backend = backend
        self.pega_erros()
        
    def pega_erros(self):
        if self.backend.erros:
            erros = self.backend.erros
            if erros is not None:
                for erro in erros:
                    if isinstance(erro, (list, tuple)) and len(erro) >= 2:
                        e = erro[0]
                        numero = erro[1]
                        self.ui.erros.addItem(f"Erro: {e}; Número: {numero}")
