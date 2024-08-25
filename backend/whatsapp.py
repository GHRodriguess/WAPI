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

class WhatsApp:
    def __init__(self):
        self.navegador = self.incia_navegador()      
        self.conectado = False  
        self.qr_code_anterior = None
        self.wait = WebDriverWait(self.navegador, 10)    
        self.diretorio = os.path.join(os.getenv('APPDATA'), 'API WhatsApp')     

    def incia_navegador(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")        
        servico = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico, options=chrome_options)
        #navegador.maximize_window()
        navegador.get("https://web.whatsapp.com")
        return navegador

    def monitora_qrcode(self, ui):        
        import base64          
        if self.conectado:
            ui.qrcode.setText("VOCÊ JÁ SE CONECTOU")
            return 
        if self.qr_code_anterior:
            print("Tem qr code anterior")
            pixmap = QPixmap(os.path.join(self.diretorio, "imagem_qr_code.png"))
            ui.qrcode.setPixmap(pixmap)
            ui.qrcode.repaint()   
        canvas = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))       
        while True:
            try:
                canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
                qr_code_atual = self.coleta_qrcode()
                if qr_code_atual!= self.qr_code_anterior:
                    with open(os.path.join(self.diretorio, "imagem_qr_code.png"), "wb") as f:
                        f.write(base64.b64decode(qr_code_atual))
                    self.qr_code_anterior = qr_code_atual
                    print("QR Code alterado")
                    pixmap = QPixmap(os.path.join(self.diretorio, "imagem_qr_code.png"))
                    ui.qrcode.setPixmap(pixmap)
                    ui.qrcode.repaint()
                time.sleep(1)
            except Exception as e:            
                self.verifica_conexao(e)
                break
    
    def coleta_qrcode(self): 
        canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
        image_data = self.navegador.execute_script("""
                var canvas = arguments[0];
                return canvas.toDataURL('image/png').substring(22);  // Remover o prefixo 'data:image/png;base64,'
            """, canvas)

        return image_data
        
    def verifica_conexao(self, e):        
        elementos = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        elementos = self.navegador.find_elements(By.TAG_NAME, "h1")
        elementos = [(elemento.text).lower() for elemento in elementos]        
        if "chats" in elementos or "baixar o whatsapp para windows" in elementos or len(elementos) == 2:
            print("CONECTADO")
            self.conectado = True
        else:    
            print("Deu erro")
            
    def pesquisa_usuario(self, identificador):    
        elemento = self.wait.until(EC. presence_of_element_located((By.CLASS_NAME, 'selectable-text')))    
        pesquisa = elemento.text
        if pesquisa:
            elemento.send_keys(Keys.BACKSPACE * len(pesquisa))            
        elemento.send_keys(identificador, Keys.ENTER)

    def envia_mensagem(self, mensagem):
        elemento = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "selectable-text")))[-1]
        elemento.send_keys(mensagem, Keys.ENTER)     
        while True:
            try: 
                ultima_mensagem = [elemento.text for elemento in self.navegador.find_elements(By.CLASS_NAME, "_ao3e") if elemento.text][-1]
                if mensagem == ultima_mensagem:                    
                    break
            except Exception as e:                
                pass
    
    def __del__(self):
        if self.navegador:
            self.fecha_navegador()                  
    
    def fecha_navegador(self):
        self.navegador.quit()
    
if __name__ == "__main__":
    api = WhatsApp()    
    api.pesquisa_usuario("Gabriel henrique Rodrigues")    
    api.envia_mensagem("Essa mensagem foi enviada por uma API do WhatsApp.")