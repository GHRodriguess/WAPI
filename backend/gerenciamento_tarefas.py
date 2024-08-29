import threading
import time

class Tarefas():
    def __init__(self, api):
        self.api = api
        self.somente_contato = True
        self.rodando = False
    
    def gerencia_tarefas_segundo_plano(self, tarefas:list):
        self.tarefas_thread = threading.Thread(target=lambda: self.realiza_tarefas(tarefas))
        self.tarefas_thread.daemon = True  
        self.tarefas_thread.start()
    
    def realiza_tarefas(self, tarefas:list):   
        self.rodando = True      
        dicionario_acoes = {
            'pesquisa_contato': self.api.pesquisa_usuario,
            'envia_mensagem': self.api.envia_mensagem,
            
        }   
        for tarefa in tarefas:    
            if self.somente_contato:
                if tarefa[0] != "pesquisa_contato":
                    continue     
                else:
                    self.somente_contato = False              
            acao = dicionario_acoes[tarefa[0]]
            parametros = tarefa[1:]   

            retorno = acao(*parametros)    
            if retorno == "Número de telefone não encontrado.":
                print(retorno, "Parando a execução...")                
                self.somente_contato = True               
            elif retorno:
                print(retorno)  
        self.rodando = False