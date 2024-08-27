import threading

class Tarefas():
    def __init__(self, api):
        self.api = api
    
    def gerencia_tarefas_segundo_plano(self, tarefas:list):
        self.tarefas_thread = threading.Thread(target=lambda: self.realiza_tarefas(tarefas))
        self.tarefas_thread.daemon = True  
        self.tarefas_thread.start()
    
    def realiza_tarefas(self, tarefas:list):         
        dicionario_acoes = {
            'pesquisa_contato': self.api.pesquisa_usuario,
            'envia_mensagem': self.api.envia_mensagem,
            
        }   
        for tarefa in tarefas:            
            acao = dicionario_acoes[tarefa[0]]
            parametros = tarefa[1:]            
            acao(*parametros)               
