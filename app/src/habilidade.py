from data import get_connection
import pymysql
import asyncio

class Habilidade:
    def __init__(self, id_habilidade = None, nome_atributo = None, lados_dados = None, link_detalhes = None, nome_habilidade = None, tipo_dano = None, qtd_dados = None, nivel_habilidade = None, adicional_por_nivel = None):
        self._id_habilidade = id_habilidade or []
        self._nome_atributo = nome_atributo or []
        self._nome_habilidade = nome_habilidade or []
        self._nivel_habilidade = nivel_habilidade or []
        self._tipo_dano = tipo_dano or []
        self._qtd_dados = qtd_dados or []
        self._lados_dados = lados_dados or []
        self._adicional_por_nivel = adicional_por_nivel or [] 
        self._link_detalhes = link_detalhes or []
        self.__habilidades_personagem = []
        
    async def carregar_habilidades_personagem_do_banco(self, id_personagem):
        try:
            if id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT id_habilidade FROM habilidade_personagem WHERE id_personagem = %s;"""
                        await mycursor.execute(query, (id_personagem))
                        result = await mycursor.fetchall()
                        if result:
                            for row in result:
                                self.__habilidades_personagem.append(row[0])              
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    @property
    async def habilidades(self):
        if (type(self._id_habilidade) is list and len(self._id_habilidade)<=0) or (self._id_habilidade is None):
            await self.carregar_habilidades()
        habilidades = []
        for id_habilidade, nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes in zip(self._id_habilidade, self._nome_atributo, self._nome_habilidade, self._nivel_habilidade, self._tipo_dano, self._qtd_dados, self._lados_dados, self._adicional_por_nivel, self._link_detalhes):
            habilidades.append({
                'id_habilidade': id_habilidade, 
                'nome_atributo': nome_atributo, 
                'nome_habilidade': nome_habilidade, 
                'nivel_habilidade': nivel_habilidade, 
                'tipo_dano': tipo_dano, 
                'qtd_dados': qtd_dados, 
                'lados_dados': lados_dados, 
                'adicional_por_nivel': adicional_por_nivel, 
                'link_detalhes': link_detalhes,
                'personagem_possui': id_habilidade in self.__habilidades_personagem
            })
        return habilidades
    
    @property
    async def habilidade(self):
        if self._id_habilidade is None:
            await self.carregar_habilidade()
        habilidade = {
            'id_habilidade': self.id_habilidade, 
            'nome_atributo': self.nome_atributo, 
            'nome_habilidade': self.nome_habilidade, 
            'nivel_habilidade': self.nivel_habilidade, 
            'tipo_dano': self.tipo_dano, 
            'qtd_dados': self.qtd_dados, 
            'lados_dados': self.lados_dados, 
            'adicional_por_nivel': self.adicional_por_nivel, 
            'link_detalhes': self.link_detalhes
        }
        return habilidade
   
    async def carregar_habilidades(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_habilidade, nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes FROM habilidade;"
                    await mycursor.execute(query)
                    result = await mycursor.fetchall() 
                    if result:
                        for row in result:
                            self._id_habilidade.append(row[0])
                            self._nome_atributo.append(row[1])
                            self._nome_habilidade.append(row[2])
                            self._nivel_habilidade.append(row[3])
                            self._tipo_dano.append(row[4])
                            self._qtd_dados.append(row[5])
                            self._lados_dados.append(row[6])
                            self._adicional_por_nivel.append(row[7])
                            self._link_detalhes.append(row[8])
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    
    async def carregar_habilidade(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "SELECT id_habilidade, nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes FROM habilidade WHERE id_habilidade=%s;"
                    await mycursor.execute(query,(self._id_habilidade,))
                    result = await mycursor.fetchone() 
                    if result:
                        self._id_habilidade = result[0]
                        self._nome_atributo = result[1]
                        self._nome_habilidade = result[2]
                        self._nivel_habilidade = result[3]
                        self._tipo_dano = result[4]
                        self._qtd_dados = result[5]
                        self._lados_dados = result[6]
                        self._adicional_por_nivel = result[7]
                        self._link_detalhes = result[8]
                        return True
            return False
        except Exception as e:
            print(e)
            return False

    async def insert_habilidade_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = "INSERT INTO habilidade (nome_atributo, nome_habilidade, nivel_habilidade, tipo_dano, qtd_dados, lados_dados, adicional_por_nivel, link_detalhes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                    await mycursor.execute(query, (self.nome_atributo, self.nome_habilidade, self.nivel_habilidade, self.tipo_dano, self.qtd_dados, self.lados_dados, self.adicional_por_nivel, self.link_detalhes))
                    self.id_habilidaded_habilidade = mycursor.lastrowid   
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False

    async def delete_habilidade_banco(self):
        try:
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    query = """DELETE from habilidade
                    WHERE id_habilidade=%s;"""
                    await mycursor.execute(query, (self._id_habilidade,))
                    await conn.commit()
                    return True
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_habilidade_banco(self, chave, valor):
        try:
            possiveis_chave = ['id_habilidade', 'nome_atributo', 'nome_habilidade', 'nivel_habilidade', 'tipo_dano', 'qtd_dados', 'lados_dados', 'adicional_por_nivel', 'link_detalhes']
            async with await get_connection() as conn:
                async with conn.cursor() as mycursor:
                    if chave in possiveis_chave:
                        query = f"""UPDATE habilidade SET {chave}=%s WHERE id_habilidade=%s"""
                        await mycursor.execute(query, (valor, self._id_habilidade))
                        await conn.commit()
                        return True
        except pymysql.Error as e:
            print(e)
            return False 
        
    @property
    def nome_habilidade(self):
        return self._nome_habilidade
    
    @nome_habilidade.setter
    def nome_habilidade(self, value):
        self._nome_habilidade = value
        
    @property
    def nome_atributo(self):
        return self._nome_atributo
    
    @nome_atributo.setter
    def nome_atributo(self, value):
        self._nome_atributo = value
    
    @property
    def id_habilidade(self):
        return self._id_habilidade
    
    @id_habilidade.setter
    def id_habilidade(self, value):
        self._id_habilidade = value
        
    @property
    def tipo_dano(self):
        return self._tipo_dano
    
    @tipo_dano.setter
    def tipo_dano(self, value):
        self._tipo_dano = value
        
    @property
    def qtd_dados(self):
        return self._qtd_dados
    
    @qtd_dados.setter
    def qtd_dados(self, value):
        self._qtd_dados = value 
    
    @property
    def lados_dados(self):
        return self._lados_dados
    
    @lados_dados.setter
    def lados_dados(self, value):
        self._qtd_dados = value
        
    @property
    def adicional_por_nivel(self):
        return self._adicional_por_nivel
    
    @adicional_por_nivel.setter
    def adicional_por_nivel(self, value):
        self._qtd_dados = value
        
    @property
    def link_detalhes(self):
        return self._link_detalhes
    
    @link_detalhes.setter
    def link_detalhes(self, value):
        self._qtd_dados = value
        
    @property
    def nivel_habilidade(self):
        return self._nivel_habilidade
    
    @nivel_habilidade.setter
    def nivel_habilidade(self, value):
        self._nivel_habilidade = value