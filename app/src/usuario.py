from tools import criptografar
from data import mydb
import datetime

class Usuario:
    def __init__(self,id=None,nome=None,email=None,senha=None,data_nascimento=None):
        self._id=id
        self._nome=nome
        self._email=email
        self._senha=criptografar(senha)
        self.__tipo_usuario=None
        self._data_nascimento = data_nascimento
        self._personagens=[]
        
    @property
    def tipo_usuario(self):
        if self.__tipo_usuario is None:
            self.__tipo_usuario=self.get_usuario()['tipo_usuario']
        return self.__tipo_usuario   
    
    def usuario_admin(self):
        if self.__tipo_usuario is None:
            self.__tipo_usuario=self.get_usuario()['tipo_usuario']
        return self.__tipo_usuario=='admin'   
    
    @property
    def personagens(self):
        if len(self._personagens)<=0:
            self.carregar_personagens_banco()
        return self._personagens
    
    @property
    def id(self):
        if self._id is None:
            self._id=self.get_usuario()['id_usuario']
        return self._id
    
    @property
    def nome(self):
        if self._nome is None:
            self._nome=self.get_usuario()['nome']
        return self._nome
    
    @property
    def email(self):
        if self._email is None:
            self._email=self.get_usuario()['email']
        return self._email
    
    @property
    def years(self):
        if self._data_nascimento is None:
            self._data_nascimento = self.get_usuario()['data_nascimento']
        if self._data_nascimento:
            today = datetime.date.today()
            data_nascimento_str = self._data_nascimento.strftime('%Y-%m-%d')
            dif = today - datetime.datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            return dif.days // 365
        return None
            
    def delete_usuario(self):
        try:
            if self._id:
                mycursor = mydb.cursor()
                mycursor.execute('DELETE from usuario WHERE id_usuario=%s', (self._id,))
                mydb.commit()
                mydb.close()
                return True
            elif self._email:
                mycursor = mydb.cursor()
                mycursor.execute('DELETE from usuario WHERE email=%s', (self._email,))
                mydb.commit()
                mydb.close()
                return True
            return False
        except EOFError as e:
            print(e)
            return False   
    
    def create_usuario(self):
        try:
            if self._nome and self._email and self._senha and self._data_nascimento:
                mycursor = mydb.cursor()
                mycursor.execute('INSERT INTO usuario (nome,email,senha,data_nascimento,tipo_usuario) values(%s,%s,%s,%s,%s)',(self._nome,self._email,self._senha,self._data_nascimento,'padrão'))
                mydb.commit()
                self._id=mycursor.lastrowid    
                return True
        except EOFError as e:
                print(e)
                return False
        return False
    
    def update_usuario(self, chave, valor):
        try:
            possiveis_chave=['nome','email','senha','data_nascimento','tipo_usuario']
            if self._id and chave in possiveis_chave:
                if chave=='senha':
                    valor=criptografar(valor)
                mycursor = mydb.cursor()
                query = f"UPDATE usuario SET {chave} = %s WHERE id_usuario = %s"
                mycursor.execute(query, (valor, self._id))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    def get_usuario(self):
        try:
            mycursor = mydb.cursor()
            result = {}
            if self._id:
                mycursor.execute("SELECT * FROM usuario WHERE id_usuario=%s", (self._id,))
                result = mycursor.fetchone()
            elif self._email:
                mycursor.execute("SELECT * FROM usuario WHERE email=%s", (self._email,))
                result = mycursor.fetchone()
            if result:
                column_nomes = [column[0] for column in mycursor.description]
                usuario={}
                for chave, valor in zip(column_nomes,result):
                    usuario[chave] = valor
                return usuario
            return None
        except:
            return None
    
    def valid_usuario(self):
        try:
            mycursor = mydb.cursor()
            if self._email and self._senha:
                mycursor.execute("SELECT * FROM usuario WHERE email=%s and senha=%s",(self._email,self._senha))
                result = mycursor.fetchone()  
                if result:
                    self._id=result[0]
                    self._nome=result[1]
                    self._data_nascimento=result[4]
                    return True
            return False
        except EOFError as e:
            print(e)
            return False 
        
    def carregar_personagens_banco(self):
        try:
            mycursor = mydb.cursor()
            if self._id:
                query="""SELECT pr.id_personagem,pr.nome_personagem,rc.nome_raca,rc.id_raca
                FROM personagem pr,raca rc
                WHERE pr.id_usuario = %s and pr.id_raca=rc.id_raca;"""
                mycursor.execute(query,(self._id,))
                result = mycursor.fetchall()  
                if result:
                    for row in result:
                        self._personagens.append({'id_personagem':row[0],'nome_personagem':row[1],'nome_raca':row[2],'id_raca':row[3]})
                    return True
            return 'Sem Personagens no Banco', False
        except EOFError as e:
            print(e)
            return False 