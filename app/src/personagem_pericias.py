from data import get_connection, attributes
import pandas
import pymysql
import asyncio

from src import PersonagemAtributos

class PersonagemPericias(PersonagemAtributos):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._pericias=[] 
        
    async def exists_pericia_banco(self, id_pericia):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "SELECT EXISTS (SELECT id_pericia_personagem FROM pericia_personagem WHERE id_personagem = %s and id_pericia = %s)"
                        await mycursor.execute(query, (self._id_personagem, id_pericia,))
                        result = await mycursor.fetchone()
                        if result[0] == 1:
                            return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def adicionar_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = "INSERT INTO pericia_personagem(id_personagem,id_pericia) VALUES(%s,%s);"
                        await mycursor.execute(query, (self._id_personagem,id_pericia))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def delete_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """DELETE from pericia_personagem
                        WHERE id_pericia=%s;"""
                        await mycursor.execute(query, (id_pericia,))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    async def carregar_pericias_do_banco(self):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """SELECT pp.id_pericia, pc.nome_pericia, pc.status_uso,pp.id_pericia_personagem 
                        FROM pericia_personagem pp 
                        JOIN pericia pc ON pp.id_pericia = pc.id_pericia 
                        WHERE pp.id_personagem = %s;"""
                        await mycursor.execute(query, (self._id_personagem,))
                        result = await mycursor.fetchall() 
                        if result:
                            self._pericias.clear()
                            for row in result:
                                self._pericias.append({'id_pericia_personagem': row[3], 'id_pericia': row[0], 'nome_pericia': row[1], 'status_uso': row[2]})
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    async def update_pericias_banco(self,id_pericia,id_pericia_personagem):
        try:
            if self._id_personagem:
                async with await get_connection() as conn:
                    async with conn.cursor() as mycursor:
                        query = """UPDATE pericia_personagem
                        SET id_pericia=%s
                        WHERE id_pericia_personagem=%s;"""
                        await mycursor.execute(query, (id_pericia,id_pericia_personagem))
                        await conn.commit()
                        return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    async def get_pericias(self,chave,status_uso):
        if len(self._pericias) <= 0:
            await self.carregar_pericias_do_banco()
        if any(d.get('nome_pericia') == chave for d in self._pericias):
            return int(attributes.loc[self._atributos[status_uso]] + self.bonus_proficiencia)
        else:
            return int(attributes.loc[self._atributos[status_uso]]) if self._atributos[status_uso] is not None else ''

    @property
    def lista_nome_pericias(self):
        lista = [d.get('nome_pericia') for d in self._pericias]
        return lista

    @property
    def pericias(self):
        return self._pericias
        
    @property
    def acrobacia(self):
        if any(d.get('nome_pericia') == 'acrobacia' for d in self.pericias) and self.bonus_destreza is not None:
            return int(self.bonus_destreza + self.bonus_proficiencia)
        return int(self.bonus_destreza) if self.bonus_destreza is not None else ''

    @property
    def arcanismo(self):
        if any(d.get('nome_pericia') == 'arcanismo' for d in self.pericias) and self.bonus_inteligencia is not None:
            return int(self.bonus_inteligencia + self.bonus_proficiencia) 
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else ''

    @property
    def atletismo(self):
        if any(d.get('nome_pericia') == 'atletismo' for d in self.pericias) and self.bonus_forca is not None:
            return int (self.bonus_forca + self.bonus_proficiencia)
        return int(self.bonus_forca) if self.bonus_forca is not None else ''

    @property
    def atuacao(self):
        if any(d.get('nome_pericia') == 'atuacao' for d in self.pericias) and self.bonus_carisma is not None:
            return int(self.bonus_carisma + self.bonus_proficiencia)
        return int(self.bonus_carisma) if self.bonus_carisma is not None else ''

    @property
    def enganacao(self):
        if any(d.get('nome_pericia') == 'enganacao' for d in self.pericias) and self.bonus_carisma is not None:
            return int(self.bonus_carisma + self.bonus_proficiencia)
        return int(self.bonus_carisma) if self.bonus_carisma is not None else ''

    @property
    def furtividade(self):
        if any(d.get('nome_pericia') == 'furtividade' for d in self.pericias) and self.bonus_destreza is not None:
            return int(self.bonus_destreza + self.bonus_proficiencia)       
        return int(self.bonus_destreza) if self.bonus_destreza is not None else ''

    @property
    def historia(self):
        if any(d.get('nome_pericia') == 'historia' for d in self.pericias) and self.bonus_inteligencia is not None:
            return int(self.bonus_inteligencia + self.bonus_proficiencia)
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else ''

    @property
    def intimidacao(self):
        if any(d.get('nome_pericia') == 'intimidacao' for d in self.pericias) and self.bonus_carisma is not None:
            return int(self.bonus_carisma + self.bonus_proficiencia)
        return int(self.bonus_carisma) if self.bonus_carisma is not None else ''

    @property
    def intuicao(self):
        if any(d.get('nome_pericia') == 'intuicao' for d in self.pericias) and self.bonus_sabedoria is not None:
            return int(self.bonus_sabedoria + self.bonus_proficiencia)
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else ''

    @property
    def investigacao(self):
        if any(d.get('nome_pericia') == 'investigacao' for d in self.pericias) and self.bonus_inteligencia is not None:
            return int(self.bonus_inteligencia + self.bonus_proficiencia)
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else ''

    @property
    def lidar_com_animais(self):
        if any(d.get('nome_pericia') == 'lidar_com_animais' for d in self.pericias) and self.bonus_sabedoria is not None:
            return int(self.bonus_sabedoria + self.bonus_proficiencia)
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else ''

    @property
    def medicina(self):
        if any(d.get('nome_pericia') == 'medicina' for d in self.pericias) and self.bonus_sabedoria is not None:         
            return int(self.bonus_sabedoria + self.bonus_proficiencia)
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else ''

    @property
    def natureza(self):
        if any(d.get('nome_pericia') == 'natureza' for d in self.pericias) and self.bonus_inteligencia is not None:
            return int(self.bonus_inteligencia + self.bonus_proficiencia)
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else ''

    @property
    def percepcao(self):
        if any(d.get('nome_pericia') == 'percepcao' for d in self.pericias) and self.bonus_sabedoria is not None :         
            return int(self.bonus_sabedoria + self.bonus_proficiencia)
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else ''

    @property
    def persuasao(self):
        if any(d.get('nome_pericia') == 'persuasao' for d in self.pericias) and self.bonus_carisma is not None:
            return int(self.bonus_carisma + self.bonus_proficiencia)
        return int(self.bonus_carisma) if self.bonus_carisma is not None else ''

    @property
    def prestidigitacao(self):
        if any(d.get('nome_pericia') == 'prestidigitacao' for d in self.pericias) and self.bonus_destreza is not None:
            return int(self.bonus_destreza + self.bonus_proficiencia)       
        return int(self.bonus_destreza) if self.bonus_destreza is not None else ''

    @property
    def religiao(self):
        if any(d.get('nome_pericia') == 'religiao' for d in self.pericias) and self.bonus_inteligencia is not None:
            return int(self.bonus_inteligencia + self.bonus_proficiencia)
        return int(self.bonus_inteligencia) if self.bonus_inteligencia is not None else ''

    @property
    def sobrevivencia(self):
        if any(d.get('nome_pericia') == 'sobrevivencia' for d in self.pericias) and self.bonus_sabedoria is not None:
            return int(self.bonus_sabedoria + self.bonus_proficiencia)
        return int(self.bonus_sabedoria) if self.bonus_sabedoria is not None else ''