import sqlite3

class Database:
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):        
        try:
            self.conn = sqlite3.connect(self.nome_banco)
            self.cursor = self.conn.cursor()            
        except sqlite3.Error as e:
            raise e

    def cria_tabela(self, nome_tabela:str, coluna:list[:str]):        
        coluna_com_tipos = ', '.join(coluna)
        query = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({coluna_com_tipos})"
        self.cursor.execute(query)
        self.conn.commit()        

    def inserir(self, nome_tabela:str, colunas:list[:str], valores:list[any]):       
        colunas = ', '.join(colunas)
        placeholders = ', '.join('?' * len(valores))
        query = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({placeholders})"
        self.cursor.execute(query, valores)
        self.conn.commit()       

    def atualizar(self, nome_tabela:str, updates:dict[:str, :any], condicao:str):        
        uptades = ', '.join([f"{col} = ?" for col in updates.keys()])
        query = f"UPDATE {nome_tabela} SET {uptades} WHERE {condicao}"
        self.cursor.execute(query, list(updates.values()))
        self.conn.commit()       

    def delete(self, nome_tabela:str, condition:str, params: tuple = ()):        
        query = f"DELETE FROM {nome_tabela} WHERE {condition}"
        self.cursor.execute(query, params)
        self.conn.commit()        

    def fetch_one(self, nome_tabela: str, colunas: list[str] = "*", condition: str = "1=1", params: tuple = ()) -> list:
        if isinstance(colunas, list):
            colunas = ', '.join(colunas)        
        query = f"SELECT {colunas} FROM {nome_tabela} WHERE {condition}"        
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()        
        return result
    
    def fetch_all(self, nome_tabela: str, colunas: list[str] = "*", condition: str = "1=1", params: tuple = ()) -> list:
        if isinstance(colunas, list):
            colunas = ', '.join(colunas)        
        query = f"SELECT {colunas} FROM {nome_tabela} WHERE {condition}"        
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()        
        return result

    def close(self):        
        if self.conn:
            self.conn.close()
            print(f"Conexão com o banco de dados {self.nome_banco} encerrada com sucesso.")

    def __enter__(self):       
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):        
        self.close()