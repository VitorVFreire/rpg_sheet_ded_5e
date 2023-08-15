from data import mydb, attributes
from src import Usuario
import pymysql

from src import Personagem

class PersonagemAtributos(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._atributos = {
            'forca': 0,
            'destreza': 0,
            'constituicao': 0,
            'inteligencia': 0,
            'sabedoria': 0,
            'carisma': 0
        }
        self._bonus_proficiencia = None
        
    def exists_atributos_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT EXISTS (SELECT id_atributos FROM atributos WHERE id_personagem = %s)"
                mycursor.execute(query, (self._id_personagem,))
                result = mycursor.fetchone()
                if result[0] == 1:
                    return True
                return False
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def adicionar_atributo_banco(self,chave,valor):
        try:
            possibilidade_chave=['forca','destreza','constituicao','inteligencia','sabedoria','carisma','bonus_proficiencia' ]
            if self._id_personagem and chave in possibilidade_chave:
                mycursor = mydb.cursor()
                query = f"INSERT INTO atributos(id_personagem,{chave}) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,valor,))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_atributos_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """DELETE from atributos
                WHERE id_personagem=%s;"""
                mycursor.execute(query, (self._id_personagem,))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_atributos_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia 
                FROM atributos WHERE id_personagem = %s"""
                mycursor.execute(query, (self._id_personagem,))
                result = mycursor.fetchone() 
                if result:
                    self.set_forca(result[0])
                    self.set_destreza(result[1])
                    self.set_constituicao(result[2])
                    self.set_inteligencia(result[3])
                    self.set_sabedoria(result[4])
                    self.set_carisma(result[5])
                    self._bonus_proficiencia = result[6]  # Update bonus_proficiencia directly
                    return True
                return False
            return False
        except pymysql.Error as e:
            print(e)
            return False

    
    def update_atributos_banco(self,chave,valor):
        try:
            possibilidade_chave=['forca','destreza','constituicao','inteligencia','sabedoria','carisma','bonus_proficiencia' ]
            if self._id_personagem and chave in possibilidade_chave:
                mycursor = mydb.cursor()
                query = f"""UPDATE atributos
                SET {chave}=%s
                WHERE id_personagem=%s;"""
                parametros=(valor,self._id_personagem)
                mycursor.execute(query, parametros)
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def get_bonus(self,chave):
        self.carregar_atributos_do_banco()
        if self._atributos[chave] is None:
            return 0
        return attributes.loc[self._atributos[chave]]
        
    @property
    def bonus_proficiencia(self):
        return self._bonus_proficiencia if self._bonus_proficiencia is not None else 0
    
    @bonus_proficiencia.setter
    def bonus_proficiencia(self,value):
        self._bonus_proficiencia=value
    
    @property
    def forca(self):
        return self._atributos['forca'] if self._atributos['forca'] is not None else 0
    
    @property
    def bonus_forca(self):
        if self.forca is None:
            return 0
        return attributes.loc[self.forca]
    
    def set_forca(self, value):
        self._atributos['forca'] = value
        
    @property
    def destreza(self):
        return self._atributos['destreza'] if self._atributos['destreza'] is not None else 0
    
    @property
    def bonus_destreza(self):
        if self.destreza is None:
            return 0
        return attributes.loc[self.destreza]
    
    def set_destreza(self,value):
        self._atributos['destreza']=value
    
    @property
    def constituicao(self):
        return self._atributos['constituicao'] if self._atributos['constituicao'] is not None else 0
    
    @property
    def bonus_constituicao(self):
        if self.constituicao is None:
            return 0
        return attributes.loc[self.constituicao]
           
    def set_constituicao(self,value):
        self._atributos['constituicao']=value
    
    @property
    def inteligencia(self):
        return self._atributos['inteligencia'] if self._atributos['inteligencia'] is not None else 0
    
    @property
    def bonus_inteligencia(self):
        if self.inteligencia is None:
            return 0
        return attributes.loc[self.inteligencia]
    
    def set_inteligencia(self,value):
        self._atributos['inteligencia']=value
    
    @property
    def sabedoria(self):
        return self._atributos['sabedoria'] if self._atributos['sabedoria'] is not None else 0
    
    @property
    def bonus_sabedoria(self):
        if self.sabedoria is None:
            return 0
        return attributes.loc[self.sabedoria]
     
    def set_sabedoria(self,value):
        self._atributos['sabedoria']=value
    
    @property
    def carisma(self):
        return self._atributos['carisma'] if self._atributos['carisma'] is not None else 0
    
    @property
    def bonus_carisma(self):
        if self.carisma is None:
            return 0
        return attributes.loc[self.carisma]
    
    def set_carisma(self,value):
        self._atributos['carisma']=value