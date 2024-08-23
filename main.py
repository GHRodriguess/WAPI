from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WhatsApp:
    def __init__(self):
        self.navegador = self.incia_navegador()
        self.monitora_qrcode()   

    def incia_navegador(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        servico = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico, options=chrome_options)
        #navegador.maximize_window()
        navegador.get("https://web.whatsapp.com")
        return navegador

    def monitora_qrcode(self):
        import base64
        wait = WebDriverWait(self.navegador, 10)
        canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        qr_code_anterior = None
        while True:
            try:
                canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
                qr_code_atual = self.coleta_qrcode()
                if qr_code_atual!= qr_code_anterior:
                    with open("imagem_qr_code.png", "wb") as f:
                        f.write(base64.b64decode(qr_code_atual))
                    qr_code_anterior = qr_code_atual
                    print("QR CODE ALTERADO")
                time.sleep(1)
            except Exception as e:            
                self.verifica_conexao(e)
                break
    
    def coleta_qrcode(self):        
        wait = WebDriverWait(self.navegador, 10)
        canvas = self.navegador.find_element(By.TAG_NAME, "canvas")
        image_data = self.navegador.execute_script("""
                var canvas = arguments[0];
                return canvas.toDataURL('image/png').substring(22);  // Remover o prefixo 'data:image/png;base64,'
            """, canvas)

        return image_data
        
    def verifica_conexao(self, e:KeyError):
        wait = WebDriverWait(self.navegador, 10)
        elementos = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        elementos = self.navegador.find_elements(By.TAG_NAME, "h1")
        elementos = [(elemento.text).lower() for elemento in elementos]
        if "chats" in elementos:
            print("CONECTADO")
        else:
            print(e)
            
    def pesquisa_usuario(self, identificador):    
        elemento = self.navegador.find_element(By.CLASS_NAME, 'selectable-text')    
        pesquisa = elemento.text
        if pesquisa:
            elemento.send_keys(Keys.BACKSPACE * len(pesquisa))
            
        elemento.send_keys(identificador, Keys.ENTER)

    def envia_mensagem(self, mensagem):
        elemento = self.navegador.find_elements(By.CLASS_NAME, "selectable-text")[-1]
        elemento.send_keys(mensagem, Keys.ENTER)
            
if __name__ == "__main__":
    api = WhatsApp()
    api.pesquisa_usuario("Meu amor")
    api.envia_mensagem("Mensagem de teste")