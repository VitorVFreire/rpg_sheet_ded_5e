from data import get_connection
import pymysql
import asyncio

from src import Personagem

class PersonagemStatusBase(Personagem):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._alinhamento = None
        self._antecendente = None
        self._ca = None
        self._deslocamento = None
        self._faccao = None
        self._inspiracao = None
        self._iniciativa = None
        self._nivel = None
        self._vida = None
        self._vida_atual = None
        self._vida_temporaria = None
        self._xp = None
    
    def verifica_chave(self, chave):
        possibilidade_chave=['vida','xp','nivel','alinhamento','antecendente','faccao','inspiracao','ca','iniciativa','deslocamento','vida_atual','vida_temporaria']
        return chave in possibilidade_chave
        
    async def exists_status_base_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_status_base FROM status_base WHERE id_personagem = %s)"
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_status_base_banco(self,chave,valor):
        try:
            if self._id_personagem and self.verifica_chave(chave):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"INSERT INTO status_base(id_personagem,{chave}) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._id_personagem,valor,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_status_base_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from status_base
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self._id_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_status_base_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria
                        FROM status_base
                        WHERE id_personagem = %s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchone()
                        if result:
                            self.vida = result[0]
                            self.xp = result[1]
                            self.nivel = result[2]
                            self.alinhamento = result[3] 
                            self.antecendente = result[4] 
                            self.faccao = result[5]  
                            self.inspiracao = result[6]
                            self.ca = result[7]
                            self.iniciativa = result[8]
                            self.deslocamento = result[9]
                            self.vida_atual = result[10]
                            self.vida_temporaria = result[11]     
                            return True
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_status_base_banco(self,chave,valor):
        try:
            if self._id_personagem and self.verifica_chave(chave):
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE status_base
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
    
    @property
    def status_base(self):
        return {
            'nivel': self.nivel,
            'alinhamento': self.alinhamento,
            'faccao': self.faccao,
            'antecendente': self.antecendente,
            'xp': self.xp,
            'deslocamento': self.deslocamento,
            'iniciativa': self.iniciativa,
            'vida': self.vida,
            'vida_atual': self.vida_atual,
            'vida_temporaria': self.vida_temporaria,
            'inspiracao': self.inspiracao,
            'ca': self.ca
        }
    
    @property
    def nivel(self):
        return int(self._nivel) if self._nivel is not None else None 
    
    @nivel.setter
    def nivel(self,value):
        self._nivel=value
    
    @property
    def alinhamento(self):
        return self._alinhamento
    
    @alinhamento.setter
    def alinhamento(self,value):
        self._alinhamento=value
        
    @property
    def faccao(self):
        return self._faccao        
         
    @faccao.setter
    def faccao(self,value):
        self._faccao=value
        
    @property
    def antecendente(self):
        return self._antecendente        
         
    @antecendente.setter
    def antecendente(self,value):
        self._antecendente=value
    
    @property
    def xp(self):
        return self._xp
                
    @xp.setter
    def xp(self,value):
        self._xp=value
           
    @property
    def deslocamento(self):
        return self._deslocamento
    
    @deslocamento.setter
    def deslocamento(self,value):
        self._deslocamento=value
        
    @property
    def iniciativa(self):
        return self._iniciativa
    
    @iniciativa.setter
    def iniciativa(self,value):
        self._iniciativa=value
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self,value):
        self._vida=value
        
    @property
    def vida_atual(self):
        return self._vida_atual
    
    @vida_atual.setter
    def vida_atual(self,value):
        self._vida_atual=value
       
    @property
    def vida_temporaria(self):
        return self._vida_temporaria
    
    @vida_temporaria.setter
    def vida_temporaria(self,value):
        self._vida_temporaria=value
        
    @property
    def inspiracao(self):
        return self._inspiracao
    
    @inspiracao.setter
    def inspiracao(self,value):
        self._inspiracao=value
    
    @property
    def ca(self):
        return self._ca
    
    @ca.setter
    def ca(self,value):
        self._ca=value