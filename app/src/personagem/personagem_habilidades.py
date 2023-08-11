from data import mydb, attributes
from src import Usuario
import pymysql

from src import Personagem

class Personagem_Habilidades(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id=id_usuario, id_personagem=id_personagem)
        self._feitico = []
        
    def adicionar_feitico_banco(self,id_feitico):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO feitico_personagem(id_personagem,id_feitico) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_feitico))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_feitico_banco(self,id_feitico_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """DELETE from feitico_personagem
                WHERE id_feitico_personagem=%s;"""
                mycursor.execute(query, (id_feitico_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def carregar_feitico_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT fp.id_feitico, ft.nome_feitico, ft.tipo_feitico, td.nome_tipo,fp.id_feitico_personagem
                FROM feitico_personagem fp
                JOIN feitico ft ON fp.id_feitico = ft.id_feitico
                JOIN tipo_dano td ON ft.id_tipo_dano = td.id_tipo_dano
                WHERE fp.id_personagem = %s;"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchall()
                if result:
                    for row in result:
                        feitico = {
                            'id_feitico_personagem':row[4],
                            'id_feitico': row[0],
                            'nome_feitico': row[1],
                            'tipo_feitico': row[2],
                            'tipo_dano':row[3]
                        }
                        self.feitico(feitico)               
                    return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_feitico_banco(self,novo_feitico,id_feitico_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE feitico_personagem
                SET id_feitico=%s
                WHERE id_feitico_personagem=%s;"""
                mycursor.execute(query, (novo_feitico,id_feitico_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    def feitico(self,value):
        return self._feitico[value]
    
    @property
    def feiticos(self):
        return self._feitico  
    
    @feitico.setter
    def feitico(self,value):
        self._feitico.append(value)