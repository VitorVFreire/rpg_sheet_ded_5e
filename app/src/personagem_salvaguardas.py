from data import get_connection, attributes
from src import Usuario
import pymysql
import asyncio

from src import PersonagemAtributos

class PersonagemSalvaguardas(PersonagemAtributos):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._salvaguardas = []
    
    async def exists_salvaguarda_banco(self, id_salvaguarda):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_salvaguarda_personagem FROM salvaguarda_personagem WHERE id_personagem = %s and id_salvaguarda = %s)"
                        await mycursor.execute(query, (self._id_personagem, id_salvaguarda))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def adicionar_salvaguardas_banco(self,id_salvaguarda):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """
                            INSERT INTO `RPG`.`salvaguarda_personagem` 
                            (`id_personagem`, `id_salvaguarda`)
                            VALUES (%s, %s)
                        """
                        await mycursor.execute(query, (self._id_personagem,id_salvaguarda,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def delete_salvaguarda_banco(self,id_salvaguarda):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from salvaguarda_personagem
                        WHERE id_salvaguarda=%s;"""
                        await mycursor.execute(query, (id_salvaguarda,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def carregar_salvaguardas_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT sp.id_salvaguarda,sl.nome_salvaguarda,sp.id_salvaguarda_personagem FROM salvaguarda_personagem sp,salvaguarda sl WHERE sp.id_personagem = %s and sl.id_salvaguarda=sp.id_salvaguarda"
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._salvaguardas.clear()
                            for row in result:
                                self._salvaguardas.append({'id_salvaguarda_personagem':row[2],'id_salvaguarda':row[0],'nome_salvaguarda':row[1]})
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_salvaguardas_banco(self,nova_id_salvaguarda,antiga_id_salvaguarda):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE salvaguarda_personagem
                        SET id_salvaguarda=%s
                        WHERE id_salvaguarda=%s;"""
                        await mycursor.execute(query, (nova_id_salvaguarda,antiga_id_salvaguarda,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def get_salvaguardas(self,chave):
        await self.carregar_salvaguardas_do_banco()
        if any(d.get('nome_salvaguarda') == chave for d in self._salvaguardas):
            return attributes.loc[self._atributos[chave]]+ self.bonus_proficiencia
        else:
            return attributes.loc[self._atributos[chave]]
        
    @property
    def salvaguardas(self):
        return self._salvaguardas

    @salvaguardas.setter
    def salvaguardas(self, value):
        self._salvaguardas.append(value)
        
    @property
    def lista_nome_salvaguardas(self):
        lista = [d.get('nome_salvaguarda') for d in self._salvaguardas]
        return lista

    @property
    def resistencia_forca(self):
        if any(d.get('nome_salvaguarda') == 'forca' for d in self._salvaguardas):
            return self.bonus_forca + self._bonus_proficiencia
        return int(self.bonus_forca) if self.bonus_forca is not None else None
    
    @property
    def resistencia_destreza(self):
        if any(d.get('nome_salvaguarda') == 'destreza' for d in self._salvaguardas):
            return self.bonus_destreza + self._bonus_proficiencia
        return int(self.bonus_destreza) if self.bonus_destreza is not None else None
    
    @property
    def resistencia_constituicao(self):
        if any(d.get('nome_salvaguarda') == 'constituicao' for d in self._salvaguardas):
            return self.bonus_constituicao + self._bonus_proficiencia
        return int(self.bonus_constituicao) if self.bonus_constituicao is not None else None
    
    @property
    def resistencia_inteligencia(self):
        if any(d.get('nome_salvaguarda') == 'inteligencia' for d in self._salvaguardas):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else None
    
    @property
    def resistencia_sabedoria(self):
        if any(d.get('nome_salvaguarda') == 'sabedoria' for d in self._salvaguardas):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else None
    
    @property
    def resistencia_carisma(self):
        if any(d.get('nome_salvaguarda') == 'carisma' for d in self._salvaguardas):
            return self.bonus_carisma + self._bonus_proficiencia
        return int(self.bonus_carisma) if self.bonus_carisma is not None else None