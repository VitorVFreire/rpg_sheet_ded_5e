from data import mydb
import pymysql

class Classe:
    def __init__(self, id_classe=None, nome_classe=None):
        self._id_classe = [] if id_classe is None else id_classe
        self._nome_classe = nome_classe if nome_classe is not None else []

    @property
    def classes(self):
        if (type(self._id_classe) is list and len(self._id_classe)<=0) or (self._id_classe is None):
            self.carregar_classes()
        classes=[]
        for id_classe,nome_classe in zip(self._id_classe,self._nome_classe):
            classes.append({'id_classe':id_classe,'nome_classe':nome_classe})
        return classes
    
    def carregar_classes(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT id_classe, nome_classe FROM classe;"
            mycursor.execute(query)
            result = mycursor.fetchall() 
            if result:
                for row in result:
                    self._id_classe.append(row[0])
                    self._nome_classe.append(row[1])
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def insert_classe_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO classe (nome_classe) VALUES (%s);"
            mycursor.execute(query, (str(self._nome_classe),))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False

    def delete_classe_banco(self):
        try:
            mycursor = mydb.cursor()
            query = """DELETE from classe
            WHERE id_classe=%s;"""
            mycursor.execute(query, (self._id_classe))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_classe_banco(self,valor):
        try:
            mycursor = mydb.cursor()
            query = "UPDATE classe SET nome_classe=%s WHERE id_classe=%s"
            mycursor.execute(query, (valor,self._id_classe))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False 