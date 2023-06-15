from database import mydb
from tools import criptografar
import datetime

class User:
    def __init__(self,id=None,name=None,email=None,password=None,datebirth=None):
        self._id=id
        self._name=name
        self._email=email
        if password is not None:
            self._password=criptografar(password)
        else:
            self._password=None
        self._datebirth = datebirth
        
    @property
    def id(self):
        if self._id is None:
            self._id=self.get_user()['id_user']
        return self._id
    
    @property
    def name(self):
        if self._name is None:
            self._name=self.get_user()['name']
        return self._name
    
    @property
    def email(self):
        if self._email is None:
            self._email=self.get_user()['email']
        return self._email
    
    @property
    def years(self):
        if self._datebirth is None:
            self._datebirth = self.get_user()['datebirth']
        if self._datebirth:
            today = datetime.date.today()
            datebirth_str = self._datebirth.strftime('%Y-%m-%d')
            dif = today - datetime.datetime.strptime(datebirth_str, '%Y-%m-%d').date()
            return dif.days // 365
        return None
            
    def delete(self):
        try:
            if self._id:
                mycursor = mydb.cursor()
                mycursor.execute('DELETE from user WHERE id_user=%s', (self._id,))
                mydb.commit()
                mydb.close()
                return True
            elif self._email:
                mycursor = mydb.cursor()
                mycursor.execute('DELETE from user WHERE email=%s', (self._email,))
                mydb.commit()
                mydb.close()
                return True
            return False
        except EOFError as e:
            print(e)
            return False   
    
    def create(self):
        try:
            if self._name and self._email and self._password and self._datebirth:
                mycursor = mydb.cursor()
                mycursor.execute('INSERT INTO user (name,email,password,datebirth) values(%s,%s,%s,%s)',(self._name,self._email,self._password,self._datebirth))
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
                query = f"UPDATE user SET {column} = %s WHERE id_user = %s"
                mycursor.execute(query, (value, self._id))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    def get_user(self):
        try:
            mycursor = mydb.cursor()
            result = {}
            if self._id:
                mycursor.execute("SELECT * FROM user WHERE id_user=%s", (self._id,))
                myresult = mycursor.fetchone()
            elif self._email:
                mycursor.execute("SELECT * FROM user WHERE email=%s", (self._email,))
                myresult = mycursor.fetchone()
            
            if myresult:
                column_names = [column[0] for column in mycursor.description]
                indexed_result = [(column_names[i], field) for i, field in enumerate(myresult)]
                for column_name, field in indexed_result:
                    result[column_name] = field
                return result
            return None
        except:
            return None
    
    def valid_user(self):
        try:
            mycursor = mydb.cursor()
            if self._email and self._password:
                mycursor.execute("SELECT * FROM user WHERE email=%s and password=%s",(self._email,self._password))
                myresult = mycursor.fetchone()  
                if myresult:
                    self._id=myresult[0]
                    self._name=myresult[1]
                    self._datebirth=myresult[4]
                    return True
            return False
        except EOFError as e:
            print(e)
            return False 