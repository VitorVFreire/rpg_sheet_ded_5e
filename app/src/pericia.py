from data import mydb
import pymysql

class Pericia:
    def __init__(self):
        self._id_pericia=[]
        self._nome_pericia=[]
        self._status_uso=[]
        
    @property
    def pericias(self):
        pericias=[]
        for id_pericia,nome_pericia,status_uso in self._id_pericia,self._nome_pericia,self._status_uso:
            pericias.append({'id_pericia':id_pericia,'nome_pericia':nome_pericia,'status_uso':status_uso})
        return pericias
    
    def carregar_pericias(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT id_pericia, nome_pericia, status_uso from pericia;"
            mycursor.execute(query)
            result = mycursor.fetchall() 
            if result:
                for row in result:
                    self._id_pericia.append(row[0])
                    self._nome_pericia.append(row[1])
                    self._status_uso.append(row[2])
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def insert_pericia_banco(self,nome_pericia,status_uso):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO pericia(nome_pericia,status_uso) VALUES(%s,%s);"
            mycursor.execute(query, (nome_pericia,status_uso))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_pericia_banco(self,id_pericia):
        try:
            mycursor = mydb.cursor()
            query = """DELETE from pericia
            WHERE id_pericia=%s;"""
            mycursor.execute(query, (id_pericia))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_pericia_banco(self,id_pericia,chave,valor):
        try:
            possiveis_chave=['nome_pericia','status_uso']
            if chave in possiveis_chave:
                mycursor = mydb.cursor()
                query = f"UPDATE pericia SET {chave}=%s"
                mycursor.execute(query, (valor))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False        