from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PyQt5.QtGui import QPixmap
import os
from backend.database import Database


class WhatsApp:
    def __init__(self):
        self.diretorio = os.path.join(os.getenv("APPDATA"), "API WhatsApp")
        self.navegador = self.incia_navegador()
        self.database = Database(os.path.join(os.getenv("APPDATA"), "API WhatsApp", "database.db"))
        self.wait = WebDriverWait(self.navegador, 10)              
        try:
            self.verifica_conexao()
        except Exception as e:
            self.conectado = False
        self.qr_code_anterior = None

    def incia_navegador(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--user-data-dir={os.path.join(self.diretorio, 'dados_navegador')}")
        servico = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico, options=chrome_options)
        # navegador.maximize_window()
        navegador.get("https://web.whatsapp.com")
        return navegador
    
    def obtem_contato_confianca(self):
        contato_confianca = self.database.fetch_one('contatos', colunas=["numero"],condition='contato_confianca = ?', params=(True,))
        if isinstance(contato_confianca, tuple):
            contato_confianca = str(contato_confianca[0])        
        return contato_confianca if contato_confianca else None
            

    def monitora_qrcode(self, ui, conexao):
        import base64
        if self.qr_code_anterior:            
            pixmap = QPixmap(os.path.join(self.diretorio, "imagem_qr_code.png"))
            ui.qrcode.setPixmap(pixmap)
            ui.qrcode.repaint()
        canvas = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        while True:
            try:
                canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
                qr_code_atual = self.coleta_qrcode()
                if qr_code_atual != self.qr_code_anterior:
                    with open(os.path.join(self.diretorio, "imagem_qr_code.png"), "wb") as f:
                        f.write(base64.b64decode(qr_code_atual))
                    self.qr_code_anterior = qr_code_atual                    
                    pixmap = QPixmap(os.path.join(self.diretorio, "imagem_qr_code.png"))
                    ui.qrcode.setPixmap(pixmap)
                    ui.qrcode.repaint()
                time.sleep(1)
            except Exception as e:
                self.verifica_conexao(e)
                if self.conectado:
                    conexao.verifica_conexao()
                break

    def coleta_qrcode(self):
        canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
        image_data = self.navegador.execute_script("""
                var canvas = arguments[0];
                return canvas.toDataURL('image/png').substring(22);  // Remover o prefixo 'data:image/png;base64,'
            """,canvas,
        )

        return image_data
        
    def verifica_conexao(self, e=None, espera=True):  
        if espera:      
            elementos = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        elementos = self.navegador.find_elements(By.TAG_NAME, "h1")
        elementos = [(elemento.text).lower() for elemento in elementos]
        if "chats" in elementos or "baixar o whatsapp para windows" in elementos or len(elementos) == 2:
            self.conectado = True            
        else:    
            self.conectado = False
            
    def pesquisa_usuario(self, identificador): 
        elemento = self.wait.until(EC. presence_of_element_located((By.CLASS_NAME, 'selectable-text'))) 
        pesquisa = elemento.text        
        if pesquisa: 
            elemento.send_keys(Keys.CONTROL + "a")
            elemento.send_keys(Keys.BACKSPACE) 

        elemento = self.navegador.find_element(By.CLASS_NAME, "selectable-text")
        elemento.send_keys(identificador, Keys.ENTER)
        tem_contato = self.verifica_se_existe_contato(identificador)  
        if not tem_contato:
            self.contato_confianca = self.obtem_contato_confianca()              
            self.pesquisa_usuario(self.contato_confianca)            
            retorno = self.envia_mensagem(identificador, click=True)            
            return retorno, identificador if retorno else None, None
            
    def verifica_se_existe_contato(self, identificador):        
        try:
            resultados = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_ao3e")))            
            resultados = [resultado.text for resultado in resultados if resultado.text]            
            if "Procurando por conversas, contatos ou mensagens..." in resultados:
                return self.verifica_se_existe_contato(identificador) 
            
            if "Nenhuma conversa, contato ou mensagem encontrada" in resultados:                
                return False
            
            if not identificador in resultados:         
                return True
            
        except Exception as e:            
            return self.verifica_se_existe_contato(identificador) 
            
    def envia_mensagem(self, mensagem, click=False):        
        elemento = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "selectable-text")))[-1]
        elemento.send_keys(mensagem, Keys.ENTER)  
        while True:
            try: 
                contagem = 0
                elementos = self.navegador.find_elements(By.CLASS_NAME, "_ao3e") 
                ultima_mensagem = [elemento.text for elemento in elementos if elemento.text][-1]
                if mensagem == ultima_mensagem:    
                    if click:
                        elementos[-1].click()      
                        elemento_entrar_conversa = self.navegador.find_element(By.CLASS_NAME, "_aj-z")
                        if not "copiar" in elemento_entrar_conversa.text.lower():
                            elemento_entrar_conversa.click()  
                        else:
                            return "Número de telefone não encontrado."
                        time.sleep(1.5)        
                    break
                else:
                    contagem += 1
                    if contagem >= 50:
                        return "Mensagem não enviada."
                    
            except Exception as e:  
                pass

    def __del__(self):
        try:
            if self.navegador:
                self.fecha_navegador()
        except Exception as e:
            pass

    def fecha_navegador(self):
        self.navegador.quit()
        
if __name__ == "__main__":
    api = WhatsApp()
    api.pesquisa_usuario("Gabriel henrique Rodrigues")
    api.envia_mensagem("Essa mensagem foi enviada por uma API do WhatsApp.")
