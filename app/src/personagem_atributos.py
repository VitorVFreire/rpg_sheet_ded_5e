from data import get_connection, attributes
import pymysql
import asyncio

from src import Personagem

class PersonagemAtributos(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._atributos = {
            'forca': None,
            'destreza': None,
            'constituicao': None,
            'inteligencia': None,
            'sabedoria': None,
            'carisma': None
        }
        self._bonus_proficiencia = None
        
    def verifica_valor(self, valor, chave):
        valor = int(valor)
        possibilidade_chave=['forca','destreza','constituicao','inteligencia','sabedoria','carisma','bonus_proficiencia' ]
        condicao = 0 < valor <= 30 if chave != 'bonus_proficiencia' else valor > 0
        return condicao and chave in possibilidade_chave
        
    @property
    def atributos(self):
        return {
            'forca': self.forca,
            'bonus_forca': self.bonus_forca,
            'destreza': self.destreza,
            'bonus_destreza': self.bonus_destreza,
            'inteligencia': self.inteligencia,
            'bonus_inteligencia': self.bonus_inteligencia,
            'constituicao': self.constituicao,
            'bonus_constituicao': self.bonus_constituicao,
            'sabedoria': self.sabedoria,
            'bonus_sabedoria': self.bonus_sabedoria,
            'carisma': self.carisma,
            'bonus_carisma': self.bonus_carisma,
            'bonus_proficiencia': self.bonus_proficiencia_externa
        }
        
    async def exists_atributos_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_atributos FROM atributos WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_atributo_banco(self,chave,valor):
        try:
            if self._id_personagem and self.verifica_valor(chave=chave, valor=valor):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"INSERT INTO atributos(id_personagem,{chave}) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._id_personagem,valor,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_atributos_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from atributos
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def carregar_atributos_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia 
                        FROM atributos WHERE id_personagem = %s"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone() 
                        if result:
                            self.set_forca(result[0])
                            self.set_destreza(result[1])
                            self.set_constituicao(result[2])
                            self.set_inteligencia(result[3])
                            self.set_sabedoria(result[4])
                            self.set_carisma(result[5])
                            self._bonus_proficiencia = result[6]
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    
    async def update_atributos_banco(self, chave, valor):
        try:
            if self._id_personagem and self.verifica_valor(chave=chave, valor=valor):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE atributos
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        parametros=(valor,self._id_personagem)
                        await mycursor.execute(query, parametros)
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def get_bonus(self, chave):
        await self.carregar_atributos_do_banco()
        return getattr(self, f'bonus_{chave}')
        
    @property
    def bonus_proficiencia(self):
        return int(self._bonus_proficiencia) if self._bonus_proficiencia is not None else 0
    
    @property
    def bonus_proficiencia_externa(self):
        return int(self._bonus_proficiencia) if self._bonus_proficiencia is not None else 0
    
    @bonus_proficiencia.setter
    def bonus_proficiencia(self, value):
        self._bonus_proficiencia = value
    
    @property
    def forca(self):
        return int(self._atributos['forca']) if self._atributos['forca'] is not None else None
    
    @property
    def bonus_forca(self):
        return int(attributes.loc[self.forca]) if self.forca is not None else None
    
    def set_forca(self, value):
        self._atributos['forca'] = value 
        
    @property
    def destreza(self):
        return int(self._atributos['destreza']) if self._atributos['destreza'] is not None else None
    
    @property
    def bonus_destreza(self):
        return int(attributes.loc[self.destreza]) if self._atributos['destreza'] is not None else None
    
    def set_destreza(self,value):
        self._atributos['destreza'] = value
    
    @property
    def constituicao(self):
        return int(self._atributos['constituicao']) if self._atributos['constituicao'] is not None else None
    
    @property
    def bonus_constituicao(self):
        return int(attributes.loc[self.constituicao]) if self._atributos['constituicao'] is not None else None
           
    def set_constituicao(self,value):
        self._atributos['constituicao'] = value
    
    @property
    def inteligencia(self):
        return int(self._atributos['inteligencia']) if self._atributos['inteligencia'] is not None else None
    
    @property
    def bonus_inteligencia(self):
        return int(attributes.loc[self.inteligencia]) if self._atributos['inteligencia'] is not None else None
    
    def set_inteligencia(self,value):
        self._atributos['inteligencia'] = value
    
    @property
    def sabedoria(self):
        return int(self._atributos['sabedoria']) if self._atributos['sabedoria'] is not None else None
    
    @property
    def bonus_sabedoria(self):
        return int(attributes.loc[self.sabedoria]) if self._atributos['sabedoria'] is not None else None
     
    def set_sabedoria(self,value):
        self._atributos['sabedoria'] = value
    
    @property
    def carisma(self):
        return int(self._atributos['carisma']) if self._atributos['carisma'] is not None else None
    
    @property
    def bonus_carisma(self):
        return int(attributes.loc[self.carisma]) if self._atributos['carisma'] is not None else None
    
    def set_carisma(self,value):
        self._atributos['carisma'] = value