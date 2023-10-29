from data import get_connection
import datetime
import asyncio
import base64
from hashlib import sha256

class User:
    def __init__(self,id_user=None,name=None,email=None,password=None,birth_date=None):
        self.__id_user = id_user
        self._name = name
        self._email = email
        self.__password = self.encrypt(password)
        self.__user_type = None
        self._birth_date  =  birth_date
        self._characters = []
        
    @property
    def user_type(self):
        return self.__user_type   
    
    async def valid_admin_user(self):
        await self.load_user()
        return self.user_type == 'admin'   
    
    @property
    def characters(self):
        return self._characters
    
    @property
    def id_user(self):
        return self.__id_user
    
    @id_user.setter
    def id_user(self,value):
        self.__id_user = value
    
    @property
    def name(self): 
        return self._name
    
    @name.setter
    def name(self,value):
        self._name = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def age(self):
        today = datetime.date.today()
        data_nascimento_str = self._birth_date.strftime('%Y-%m-%d')
        dif = today - datetime.datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        return dif.days // 365 if dif.days is not None else None
    
    @age.setter
    def age(self, value):
        self._birth_date = value
        
    def encrypt(self, valor):
        if valor is None:
            return None
        hash_senha = sha256(valor.encode())
        senha_digest = hash_senha.digest()
        return base64.b64encode(senha_digest).decode('utf-8')
            
    async def delete_user(self):
        try:
            if self.id_user:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        await mycursor.execute('DELETE from usuario WHERE id_usuario=%s', (self.id_user,))
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
    
    async def insert_user(self):
        try:
            if self._name and self._email and self.__password and self._birth_date:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        await mycursor.execute('INSERT INTO usuario (nome,email,senha,data_nascimento,tipo_usuario) values(%s,%s,%s,%s,%s)',(self._name,self._email,self.__password,self._birth_date,'padrao'))
                        await conn.commit()
                        self.id_user = mycursor.lastrowid    
                        return True
        except EOFError as e:
                print(e)
                return False
        return False
    
    async def update_user(self, chave, valor):
        try:
            possiveis_chave=['nome','email','senha','data_nascimento','tipo_usuario']
            if self.id_user and chave in possiveis_chave:
                if chave == 'senha':
                    valor = self.encrypt(valor)
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"UPDATE usuario SET {chave} = %s WHERE id_usuario = %s"
                        await mycursor.execute(query, (valor, self.id_user))
                        await conn.commit()
                        return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    async def load_user(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    result = {}
                    if self.id_user:
                        await mycursor.execute("SELECT id_usuario, nome, email, senha, data_nascimento, tipo_usuario FROM usuario WHERE id_usuario=%s", (self.id_user,))
                        result = await mycursor.fetchone()
                    elif self._email:
                        await mycursor.execute("SELECT id_usuario, nome, email, senha, data_nascimento, tipo_usuario FROM usuario WHERE email=%s", (self._email,))
                        result = await mycursor.fetchone()
                    if result:
                        self.id_user = result[0]
                        self.name = result[1]
                        self.email = result[2]
                        self.senha = result[3]
                        self.age = result[4]
                        self.__user_type = result[5]
            return None
        except EOFError as e:
            print(e)
            return False
    
    async def valid_user(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if self._email and self.__password:
                        await mycursor.execute("SELECT * FROM usuario WHERE email=%s and senha=%s",(self._email,self.__password))
                        result = await mycursor.fetchone()  
                        if result:
                            self.id_user=result[0]
                            self._name=result[1]
                            self.__user_type=result[4]
                            self._birth_date=result[5]
                            return True
            return False
        except EOFError as e:
            print(e)
            return False 
        
    async def load_characters(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if self.id_user:
                        query="""SELECT pr.id_personagem,pr.nome_personagem,rc.nome_raca,rc.id_raca
                        FROM personagem pr,raca rc
                        WHERE pr.id_usuario = %s and pr.id_raca=rc.id_raca;"""
                        await mycursor.execute(query,(self.id_user,))
                        result = await mycursor.fetchall()  
                        if result:
                            for row in result:
                                self._characters.append({'id_personagem':row[0],'nome_personagem':row[1],'nome_raca':row[2],'id_raca':row[3]})
                            return True
            return 'Sem Personagens no Banco', False
        except EOFError as e:
            print(e)
            return False 