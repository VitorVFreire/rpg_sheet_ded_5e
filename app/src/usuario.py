from data import get_connection
import datetime
import asyncio
import base64
from hashlib import sha256

class Usuario:
    def __init__(self,id=None,nome=None,email=None,senha=None,data_nascimento=None):
        self.__id = id
        self._nome = nome
        self._email = email
        self._senha = self.criptografar(senha)
        self.__tipo_usuario = None
        self._data_nascimento  =  data_nascimento
        self._personagens = []
        
    @property
    def tipo_usuario(self):
        return self.__tipo_usuario   
    
    def usuario_admin(self):
        return self.tipo_usuario == 'admin'   
    
    @property
    def personagens(self):
        return self._personagens
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,value):
        self.__id = value
    
    @property
    def nome(self): 
        return self._nome
    
    @nome.setter
    def nome(self,value):
        self._nome = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def idade(self):
        today = datetime.date.today()
        data_nascimento_str = self._data_nascimento.strftime('%Y-%m-%d')
        dif = today - datetime.datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        return dif.days // 365 if dif.days is not None else None
    
    @idade.setter
    def idade(self, value):
        self._data_nascimento = value
        
    def criptografar(self, valor):
        if valor is None:
            return None
        hash_senha = sha256(valor.encode())
        senha_digest = hash_senha.digest()
        return base64.b64encode(senha_digest).decode('utf-8')
            
    async def delete_usuario(self):
        try:
            if self.id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        await mycursor.execute('DELETE from usuario WHERE id_usuario=%s', (self.id,))
                        await conn.commit()
                        return True
            elif self._email:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        await mycursor.execute('DELETE from usuario WHERE email=%s', (self._email,))
                        await conn.commit()
                        return True
            return False
        except EOFError as e:
            print(e)
            return False   
    
    async def create_usuario(self):
        try:
            if self._nome and self._email and self._senha and self._data_nascimento:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        await mycursor.execute('INSERT INTO usuario (nome,email,senha,data_nascimento,tipo_usuario) values(%s,%s,%s,%s,%s)',(self._nome,self._email,self._senha,self._data_nascimento,'padrao'))
                        await conn.commit()
                        self.id = mycursor.lastrowid    
                        return True
        except EOFError as e:
                print(e)
                return False
        return False
    
    async def update_usuario(self, chave, valor):
        try:
            possiveis_chave=['nome','email','senha','data_nascimento','tipo_usuario']
            if self.id and chave in possiveis_chave:
                if chave == 'senha':
                    valor = self.criptografar(valor)
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"UPDATE usuario SET {chave} = %s WHERE id_usuario = %s"
                        await mycursor.execute(query, (valor, self.id))
                        await conn.commit()
                        return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    async def get_usuario(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    result = {}
                    if self.id:
                        await mycursor.execute("SELECT id_usuario, nome, email, senha, data_nascimento, tipo_usuario FROM usuario WHERE id_usuario=%s", (self.id,))
                        result = await mycursor.fetchone()
                    elif self._email:
                        await mycursor.execute("SELECT id_usuario, nome, email, senha, data_nascimento, tipo_usuario FROM usuario WHERE email=%s", (self._email,))
                        result = await mycursor.fetchone()
                    if result:
                        self.id = result[0]
                        self.nome = result[1]
                        self.email = result[2]
                        self.senha = result[3]
                        self.idade = result[4]
                        self.__tipo_usuario = result[5]
            return None
        except EOFError as e:
            print(e)
            return False
    
    async def valid_usuario(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if self._email and self._senha:
                        await mycursor.execute("SELECT * FROM usuario WHERE email=%s and senha=%s",(self._email,self._senha))
                        result = await mycursor.fetchone()  
                        if result:
                            self.id=result[0]
                            self._nome=result[1]
                            self.__tipo_usuario=result[4]
                            self._data_nascimento=result[5]
                            return True
            return False
        except EOFError as e:
            print(e)
            return False 
        
    async def carregar_personagens_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if self.id:
                        query="""SELECT pr.id_personagem,pr.nome_personagem,rc.nome_raca,rc.id_raca
                        FROM personagem pr,raca rc
                        WHERE pr.id_usuario = %s and pr.id_raca=rc.id_raca;"""
                        await mycursor.execute(query,(self.id,))
                        result = await mycursor.fetchall()  
                        if result:
                            for row in result:
                                self._personagens.append({'id_personagem':row[0],'nome_personagem':row[1],'nome_raca':row[2],'id_raca':row[3]})
                            return True
            return 'Sem Personagens no Banco', False
        except EOFError as e:
            print(e)
            return False 