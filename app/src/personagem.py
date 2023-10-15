from data import get_connection
from src import Usuario, Moeda
import pymysql
import asyncio
from flask import abort

class Personagem(Usuario, Moeda):
    def __init__(self, id_usuario=None, id_personagem=None, valor=None):
        super().__init__(id=id_usuario)
        Moeda().__init__(self, valor=valor)
        self._id_personagem = id_personagem
        self._nome_personagem = None
        self._classe = []
        self._raca = None
    
    @property
    def id_personagem(self):
        return self._id_personagem 
    
    @property
    def classe(self):
        return self._classe[0]['nome_classe'] if len(self._classe) > 0 else ''
    
    @property
    def classes(self):
        return self._classe

    @classe.setter
    def classe(self, value):
        self._classe.append(value)
        
    @property
    def nome_personagem(self):
        return self._nome_personagem
        
    @nome_personagem.setter
    def nome_personagem(self,value):
        self._nome_personagem=value 
        
    @property
    def raca(self):
        return self._raca
    
    @raca.setter
    def raca(self,value):
        self._raca=value   
        
    async def personagem_pertence_usuario(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_personagem FROM personagem WHERE id_personagem = %s and id_usuario = %s)"
                        await mycursor.execute(query, (self.id_personagem, self.id))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            abort(403, "Acesso Negado")
        except pymysql.Error as e:
            print(e)
            return False      

    async def adicionar_classe_banco(self,id_classe):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """
                            INSERT INTO `RPG`.`classe_personagem` 
                            (`id_personagem`, `id_classe`)
                            VALUES (%s, %s)
                        """
                        await mycursor.execute(query, (self.id_personagem,id_classe))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_classe_banco(self,id_classe_personagem):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from classe_personagem
                        WHERE id_classe_personagem=%s;"""
                        await mycursor.execute(query, (id_classe_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_personagem_banco(self,id_raca,nome_personagem):
        try:
            if self.id:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """INSERT INTO personagem
                        (id_usuario,id_raca,nome_personagem) 
                        VALUES(%s,%s,%s);"""
                        await mycursor.execute(query, (self.id,id_raca,nome_personagem))
                        self._id_personagem = mycursor.lastrowid  
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def delete_personagem_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from personagem
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (self.id_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_classe_banco(self,id_classe,id_classe_personagem):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE classe_personagem
                        SET id_classe=%s
                        WHERE id_classe_personagem=%s"""
                        await mycursor.execute(query, (id_classe,id_classe_personagem,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_classes_do_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT cp.id_classe, cl.nome_classe,cp.id_classe_personagem
                        FROM classe_personagem cp, classe cl
                        WHERE cp.id_personagem = %s and cp.id_classe=cl.id_classe;"""
                        await mycursor.execute(query, (self.id_personagem,))
                        result = await mycursor.fetchall()
                        if result:
                            self._classe.clear()
                            for row in result:
                                self._classe.append({'id_classe_personagem': row[2], 'id_classe': row[0], 'nome_classe': row[1]})
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def carregar_personagem_banco(self):
        try:
            if self.id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT pr.nome_personagem,rc.nome_raca
                        FROM personagem pr,raca rc
                        WHERE pr.id_personagem = %s and pr.id_raca=rc.id_raca;"""
                        await mycursor.execute(query, (self.id_personagem,))
                        result = await mycursor.fetchone()
                        if result:
                            self.nome_personagem=result[0]
                            self.raca=result[1]
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_personagem_banco(self,chave,valor):
        try:
            possibilidades_chave=['id_raca','nome_personagem']
            if self.id_personagem and chave in possibilidades_chave:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = f"""UPDATE personagem
                        SET {chave}=%s
                        WHERE id_personagem=%s;"""
                        await mycursor.execute(query, (valor,self.id_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
     
    async def exists_moeda_banco(self, moeda):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_moedas_personagem FROM moeda WHERE id_personagem = %s AND moeda = %s)"
                        await mycursor.execute(query, (self._id_personagem, moeda,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False    
        
    async def banco_moeda_personagem(self, moeda):
        try:
            if self._id_personagem and self.verifica_moeda(moeda):
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            if await self.exists_moeda_banco(moeda):
                                query = f"UPDATE moedas_personagem SET qtd=%s WHERE id_personagem=%s AND moeda=%s;"
                                parametros = (self.valor, self.id_personagem, moeda,)
                            else:
                                query = f"INSERT INTO moedas_personagem(id_personagem,moeda,qtd) VALUES(%s,%s,%s);"
                                parametros = (self._id_personagem, moeda, self.valor)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def gasto_moeda(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                        async with conn.cursor() as mycursor:
                            deposito, saque = self.converter_moedas()
                            if self.exists_moeda_banco(self.destino):
                                query = "UPDATE moedas_personagem SET qtd=%s WHERE moeda=%s AND id_personagem=%s;"
                            else:
                                query = "INSERT INTO moedas_personagem (qtd_moeda, moeda, id_personagem) VALUES(%s,%s,%s);"                            
                            query += "UPDATE moedas_personagem SET qtd=%s WHERE id_personagem=%s AND moeda=%s;"
                            parametros = (deposito, self.destino, self.id_personagem, saque, self.id_personagem, self.origem,)
                            await mycursor.execute(query, parametros)
                            await conn.commit()
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False