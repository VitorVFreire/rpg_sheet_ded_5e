from data import mydb
import pymysql

class Raca:
    def __init__(self,id_raca=None,nome_raca=None):
        self._id_raca = id_raca if id_raca is not None else []
        self._nome_raca = nome_raca if nome_raca is not None else []
        
    @property
    def racas(self):
        if (type(self._id_raca) is list and len(self._id_raca)<=0) or (self._id_raca is None):
            self.carregar_racas()
        racas = []
        for id_raca, nome_raca in zip(self._id_raca, self._nome_raca):
            racas.append({'id_raca': id_raca, 'nome_raca': nome_raca})
        return racas
    
    def carregar_racas(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT id_raca, nome_raca FROM raca;"
            mycursor.execute(query)
            result = mycursor.fetchall() 
            if result:
                for row in result:
                    self._id_raca.append(row[0])
                    self._nome_raca.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def insert_raca_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO raca (nome_raca) VALUES (%s);"
            mycursor.execute(query, (str(self._nome_raca),))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_raca_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "DELETE from raca WHERE id_raca=%s;"
            mycursor.execute(query, (self._id_raca))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_raca_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "UPDATE raca SET nome_raca=%s WHERE id_raca=%s"
            mycursor.execute(query, (self._nome_raca,self._id_raca))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False        