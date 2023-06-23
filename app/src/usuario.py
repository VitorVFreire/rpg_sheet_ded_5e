from database import mydb
from tools import criptografar
import datetime

class Usuario:
    def __init__(self,id=None,nome=None,email=None,senha=None,data_nascimento=None):
        self._id=id
        self._nome=nome
        self._email=email
        self._senha=criptografar(senha)
        self.personagens=[]
        self._data_nascimento = data_nascimento
        
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
            
    def delete(self):
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
    
    def create(self):
        try:
            if self._nome and self._email and self._senha and self._data_nascimento:
                mycursor = mydb.cursor()
                mycursor.execute('INSERT INTO usuario (nome,email,senha,data_nascimento) values(%s,%s,%s,%s)',(self._nome,self._email,self._senha,self._data_nascimento))
                mydb.commit()
                self._id=mycursor.lastrowid    
                return True
        except EOFError as e:
                print(e)
                return False
        return False
    
    def update(self, column, value):
        try:
            if self._id:
                mycursor = mydb.cursor()
                query = f"UPDATE usuario SET {column} = %s WHERE id_usuario = %s"
                mycursor.execute(query, (value, self._id))
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
                myresult = mycursor.fetchone()
            elif self._email:
                mycursor.execute("SELECT * FROM usuario WHERE email=%s", (self._email,))
                myresult = mycursor.fetchone()
            
            if myresult:
                column_nomes = [column[0] for column in mycursor.description]
                indexed_result = [(column_nomes[i], field) for i, field in enumerate(myresult)]
                for column_nome, field in indexed_result:
                    result[column_nome] = field
                return result
            return None
        except:
            return None
    
    def valid_usuario(self):
        try:
            mycursor = mydb.cursor()
            if self._email and self._senha:
                mycursor.execute("SELECT * FROM usuario WHERE email=%s and senha=%s",(self._email,self._senha))
                myresult = mycursor.fetchone()  
                if myresult:
                    self._id=myresult[0]
                    self._nome=myresult[1]
                    self._data_nascimento=myresult[4]
                    return True
            return False
        except EOFError as e:
            print(e)
            return False 
        
    def carregar_personagens_banco(self):
        try:
            mycursor = mydb.cursor()
            if self._email and self._senha:
                mycursor.execute("SELECT id_personagem,nome_personagem FROM personagem ps WHERE id_usuario=%s and ",(self._id))
                myresult = mycursor.fetchall()  
                if myresult:
                    for row in result:
                        self.personagens.append({'id_personagem':row[0],'nome_personagem':row[1]})
                    return True
            return False
        except EOFError as e:
            print(e)
            return False 