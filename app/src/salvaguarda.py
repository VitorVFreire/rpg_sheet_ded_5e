from data import mydb
import pymysql

class Salvaguarda:
    def __init__(self,id_salvaguarda=None,nome_salvaguarda=None):
        self._id_salvaguarda = id_salvaguarda if id_salvaguarda is not None else []
        self._nome_salvaguarda = nome_salvaguarda if nome_salvaguarda is not None else []
        
    @property
    def nome_salvaguarda(self):
        return self._nome_salvaguarda
    
    @property
    def id_salvaguarda(self):
        return self._id_salvaguarda
    
    @property
    def salvaguardas(self):
        if (type(self._id_salvaguarda) is list and len(self._id_salvaguarda)<=0) or (self._id_salvaguarda is None):
            self.carregar_salvaguardas()
        salvaguardas = []
        for id_salvaguarda, nome_salvaguarda in zip(self._id_salvaguarda, self._nome_salvaguarda):
            salvaguardas.append({'id_salvaguarda': id_salvaguarda, 'nome_salvaguarda': nome_salvaguarda})
        return salvaguardas
    
    def carregar_salvaguardas(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT id_salvaguarda, nome_salvaguarda FROM salvaguarda;"
            mycursor.execute(query)
            result = mycursor.fetchall() 
            if result:
                for row in result:
                    self._id_salvaguarda.append(row[0])
                    self._nome_salvaguarda.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def carregar_salvaguarda(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT nome_salvaguarda FROM salvaguarda WHERE id_salvaguarda=%s;"
            mycursor.execute(query,(self._id_salvaguarda,))
            result = mycursor.fetchall() 
            if result:
                self._nome_salvaguarda=result[0]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def insert_salvaguarda_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO salvaguarda (nome_salvaguarda) VALUES (%s);"
            mycursor.execute(query, (str(self._nome_salvaguarda),))
            self._id_salvaguarda=mycursor.lastrowid 
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_salvaguarda_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "DELETE from salvaguarda WHERE id_salvaguarda=%s;"
            mycursor.execute(query, (self._id_salvaguarda,))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_salvaguarda_banco(self,valor):
        try:
            mycursor = mydb.cursor()
            query = "UPDATE salvaguarda SET nome_salvaguarda=%s WHERE id_salvaguarda=%s"
            mycursor.execute(query, (valor,self._id_salvaguarda))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False        