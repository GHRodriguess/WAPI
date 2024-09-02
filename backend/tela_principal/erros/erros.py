class Erros():
    def __init__(self, ui, janela, backend):
        self.ui = ui
        self.janela = janela
        self.backend = backend
        self.pega_erros()
        
    def pega_erros(self):
        erros = self.backend.le_erros()        
        if erros:                          
            for erro in erros:  
                e, numero = erro.split(",")
                self.ui.erros.addItem(f"Erro: {e}; Número: {numero}")
        else:
            print("sem erros")
