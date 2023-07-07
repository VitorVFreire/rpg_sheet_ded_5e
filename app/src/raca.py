from data import mydb
import pymysql

class Raca:
    def __init__(self):
        self._id_raca = []
        self._nome_raca = []
        self.carregar_racas()
        
    @property
    def racas(self):
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
        
    def insert_raca_banco(self,nome_raca):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO raca(nome_raca) VALUES(%s);"
            mycursor.execute(query, (nome_raca))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_raca_banco(self,id_raca):
        try:
            mycursor = mydb.cursor()
            query = "DELETE from raca WHERE id_raca=%s;"
            mycursor.execute(query, (id_raca))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_raca_banco(self,id_raca,nome_raca):
        try:
            mycursor = mydb.cursor()
            query = "UPDATE raca SET nome_raca=%s WHERE id_raca=%s"
            mycursor.execute(query, (nome_raca,id_raca))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False        