from data import mydb
import pymysql

class Pericia:
    def __init__(self,id_pericia=None,nome_pericia=None,status_uso=None):
        self._id_pericia= id_pericia if id_pericia is not None else []
        self._nome_pericia= nome_pericia if nome_pericia is not None else []
        self._status_uso= status_uso if status_uso is not None else []
        
    @property
    def nome_pericia(self):
        return self._nome_pericia
    
    @property
    def status_uso(self):
        return self._status_uso
    
    @property
    def pericias(self):
        if (type(self._id_pericia) is list and len(self._id_pericia)<=0) or (self._id_pericia is None):
            self.carregar_pericias()
        pericias=[]
        for id_pericia,nome_pericia,status_uso in zip(self._id_pericia,self._nome_pericia,self._status_uso):
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
        
    def carregar_pericia(self):
        try:
            mycursor = mydb.cursor()
            query = "SELECT nome_pericia, status_uso FROM pericia WHERE id_pericia=%s;"
            mycursor.execute(query,(self._id_pericia,))
            result = mycursor.fetchall() 
            if result:
                self._nome_pericia=result[0]
                self._status_uso=result[1]
                return True
            return False
        except Exception as e:
            print(e)
            return False
        
    def insert_pericia_banco(self):
        try:
            mycursor = mydb.cursor()
            query = "INSERT INTO pericia(nome_pericia,status_uso) VALUES(%s,%s);"
            mycursor.execute(query, (self._nome_pericia,self._status_uso,))
            self._id_pericia=mycursor.lastrowid
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_pericia_banco(self):
        try:
            mycursor = mydb.cursor()
            query = """DELETE from pericia
            WHERE id_pericia=%s;"""
            mycursor.execute(query, (self._id_pericia,))
            mydb.commit()
            return True
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_pericia_banco(self,chave,valor):
        try:
            possiveis_chave=['nome_pericia','status_uso']
            if chave in possiveis_chave:
                mycursor = mydb.cursor()
                query = f"UPDATE pericia SET {chave}=%s WHERE id_pericia=%s"
                mycursor.execute(query, (valor,self._id_pericia,))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False        