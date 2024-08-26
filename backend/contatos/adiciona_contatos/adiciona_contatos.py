from PyQt5 import QtWidgets

class Adiciona_Contatos():
    def __init__(self, ui, janela):
        self.ui = ui
        self.janela = janela
        self.conecta_widgets()        
        
    def conecta_widgets(self):
        self.ui.botao_inserir_planilha.clicked.connect(lambda: self.inserir_planilha()) 
        self.ui.botao_cancelar.clicked.connect(lambda: self.janela.close())
        self.ui.botao_adicionar.clicked.connect(lambda: self.adicionar())
        self.ui.dados_contato.textChanged.connect(lambda: self.atualiza_status_botao_salvar())
        
    def atualiza_status_botao_salvar(self):
        dados_contato = self.ui.dados_contato.text()
        if dados_contato:
            self.ui.botao_adicionar.setEnabled(True)
        else:
            self.ui.botao_adicionar.setEnabled(False) 
    
    
    def inserir_planilha(self):
        arquivo, _ = QtWidgets.QFileDialog.getOpenFileName(self.janela, "Selecionar Planilha", "", "Arquivos XLSX (*.xlsx)")
        print(arquivo)
        
    def adicionar(self):
        print("Adicionar")