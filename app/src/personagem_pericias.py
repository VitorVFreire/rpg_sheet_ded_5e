from data import get_connection
from src import Usuario
import pandas
import pymysql

from src import PersonagemAtributos

class PersonagemPericias(PersonagemAtributos):
    def __init__(self, id_usuario=None,id_personagem=None):
        super().__init__(id_usuario=id_usuario, id_personagem=id_personagem)
        self._pericias=[] 
        
    def exists_pericia_banco(self, id_pericia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT EXISTS (SELECT id_pericia_personagem FROM pericia_personagem WHERE id_personagem = %s and id_pericia = %s)"
                mycursor.execute(query, (self._id_personagem, id_pericia,))
                result = mycursor.fetchone()
                if result[0] == 1:
                    return True
                return False
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def adicionar_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO pericia_personagem(id_personagem,id_pericia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_pericia))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def delete_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """DELETE from pericia_personagem
                WHERE id_pericia=%s;"""
                mycursor.execute(query, (id_pericia,))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False
    
    def carregar_pericias_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT pp.id_pericia, pc.nome_pericia, pc.status_uso,pp.id_pericia_personagem 
                FROM pericia_personagem pp 
                JOIN pericia pc ON pp.id_pericia = pc.id_pericia 
                WHERE pp.id_personagem = %s;"""
                mycursor.execute(query, (self._id_personagem,))
                result = mycursor.fetchall() 
                if result:
                    self._pericias.clear()
                    for row in result:
                        self._pericias.append({'id_pericia_personagem': row[3], 'id_pericia': row[0], 'nome_pericia': row[1], 'status_uso': row[2]})
                    return True
                return False
            return False
        except pymysql.Error as e:
            print(e)
            return False
        
    def update_pericias_banco(self,id_pericia,id_pericia_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """UPDATE pericia_personagem
                SET id_pericia=%s
                WHERE id_pericia_personagem=%s;"""
                mycursor.execute(query, (id_pericia,id_pericia_personagem))
                mydb.commit()
                return True
            return False
        except pymysql.Error as e:
            print(e)
            return False

    def get_pericias(self,chave,status_uso):
        if len(self._pericias) <=0:
            self.carregar_pericias_do_banco()
        if any(d.get('nome_pericia') == chave for d in self._pericias):
            return attributes.loc[self._atributos[status_uso]]+ self.bonus_proficiencia
        else:
            return attributes.loc[self._atributos[status_uso]]

    @property
    def lista_nome_pericias(self):
        lista = [d.get('nome_pericia') for d in self._pericias]
        return lista

    @property
    def pericias(self):
        return self._pericias

    @pericias.setter
    def set_pericias(self, value):
        self._pericias.append(value)
        
    @property
    def acrobacia(self):
        if any(d.get('nome_pericia') == 'acrobacia' for d in self._pericias):
            return self.bonus_destreza + self._bonus_proficiencia
        return self.bonus_destreza

    @property
    def arcanismo(self):
        if any(d.get('nome_pericia') == 'arcanismo' for d in self._pericias):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return self.bonus_inteligencia

    @property
    def atletismo(self):
        if any(d.get('nome_pericia') == 'atletismo' for d in self._pericias):
            return self.bonus_forca + self._bonus_proficiencia
        return self.bonus_forca

    @property
    def atuacao(self):
        if any(d.get('nome_pericia') == 'atuacao' for d in self._pericias):
            return self.bonus_carisma + self._bonus_proficiencia
        return self.bonus_carisma

    @property
    def enganacao(self):
        if any(d.get('nome_pericia') == 'enganacao' for d in self._pericias):
            return self.bonus_carisma + self._bonus_proficiencia
        return self.bonus_carisma

    @property
    def furtividade(self):
        if any(d.get('nome_pericia') == 'furtividade' for d in self._pericias):
            return self.bonus_destreza + self._bonus_proficiencia
        return self.bonus_destreza

    @property
    def historia(self):
        if any(d.get('nome_pericia') == 'historia' for d in self._pericias):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return self.bonus_inteligencia

    @property
    def intimidacao(self):
        if any(d.get('nome_pericia') == 'intimidacao' for d in self._pericias):
            return self.bonus_carisma + self._bonus_proficiencia
        return self.bonus_carisma

    @property
    def intuicao(self):
        if any(d.get('nome_pericia') == 'intuicao' for d in self._pericias):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return self.bonus_sabedoria

    @property
    def investigacao(self):
        if any(d.get('nome_pericia') == 'investigacao' for d in self._pericias):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return self.bonus_inteligencia

    @property
    def lidar_com_animais(self):
        if any(d.get('nome_pericia') == 'lidar_com_animais' for d in self._pericias):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return self.bonus_sabedoria

    @property
    def medicina(self):
        if any(d.get('nome_pericia') == 'medicina' for d in self._pericias):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return self.bonus_sabedoria

    @property
    def natureza(self):
        if any(d.get('nome_pericia') == 'natureza' for d in self._pericias):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return self.bonus_inteligencia

    @property
    def percepcao(self):
        if any(d.get('nome_pericia') == 'percepcao' for d in self._pericias):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return self.bonus_sabedoria

    @property
    def persuasao(self):
        if any(d.get('nome_pericia') == 'persuasao' for d in self._pericias):
            return self.bonus_carisma + self._bonus_proficiencia
        return self.bonus_carisma

    @property
    def prestidigitacao(self):
        if any(d.get('nome_pericia') == 'prestidigitacao' for d in self._pericias):
            return self.bonus_destreza + self._bonus_proficiencia
        return self.bonus_destreza

    @property
    def religiao(self):
        if any(d.get('nome_pericia') == 'religiao' for d in self._pericias):
            return self.bonus_inteligencia + self._bonus_proficiencia
        return self.bonus_inteligencia

    @property
    def sobrevivencia(self):
        if any(d.get('nome_pericia') == 'sobrevivencia' for d in self._pericias):
            return self.bonus_sabedoria + self._bonus_proficiencia
        return self.bonus_sabedoria