import threading
import time

class Tarefas():
    def __init__(self, api):
        self.api = api
        self.somente_contato = True
        self.rodando = False
    
    def gerencia_tarefas_segundo_plano(self, tarefas: list):
        self.retornos_event = threading.Event() 
        def executar_tarefas():
            self.retornos = self.realiza_tarefas(tarefas)
            self.retornos_event.set()             

        self.retornos = None
        self.tarefas_thread = threading.Thread(target=executar_tarefas)
        self.tarefas_thread.daemon = True  
        self.tarefas_thread.start()
        return self.obter_retornos()        
        
    def obter_retornos(self):
        self.retornos_event.wait() 
        return self.retornos if self.retornos else None

    def realiza_tarefas(self, tarefas:list):   
        retornos = []
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

            resultado = acao(*parametros)            
            if resultado is not None:
                retorno, identificador = resultado
            else:
                retorno, identificador = None, None  
            if retorno:                     
                if "Número de telefone não encontrado." in retorno:                           
                    self.somente_contato = True  
                    retornos_atual = [retorno, identificador] 
                    retornos.extend(retornos_atual)           
                elif retorno:                
                    retornos_atual = [retorno, identificador] 
                    retornos.extend(retornos_atual)                 
        self.rodando = False        
        return retornos if retornos else None, None