from database import mydb,attributes
from src import Usuario

class Personagem(Usuario):
    def __init__(self, id_usuario,id_personagem):
        super().__init__(id=id_usuario)
        self._id_personagem = id_personagem
        self.nome_personagem=None
        self.nivel = None
        self.classe = []
        self._salvaguardas = []
        self._pericias=[]
        self.truques = []
        self.magias = []
        self.armas=[]
        self.equipamentos=[]
        self.caracteristicas = {
            'idade': None,
            'altura': None,
            'peso': None,
            'cor dos olhos': None,
            'cor da pele': None,
            'cor do cabelo': None,
            'imagem_personagem':None
        }
        self.atributos = {
            'forca': None,
            'destreza': None,
            'contituicao': None,
            'inteligencia': None,
            'sabedoria': None,
            'carisma': None
        }
        self.xp = None
        self._raca = None
        self.inspiracao = None
        self._bonus_proficiencia = None
        self._ca = None
        self._deslocamento = None
        self.vida = None
        self.iniciativa = None
#-----------------------------------------------HABILIDADES----------------------------------------------- 
    @magia.setter
    def set_magia(self,value):
        self.magias.append(value)
        
    @property
    def magia(self,value):
        return self.magias[value]
    
    @property
    def magias(self):
        return self.magias
    
    def adicionar_magia_banco(self,id_magia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO magia_personagem(id_personagem,id_magia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_magia))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    def carregar_magias_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT mp.id_magia, mg.nome_magia, td.nome_tipo FROM magia_personagem mp 
                JOIN magia mg ON mp.id_magia = mg.id 
                JOIN tipo_dano td ON mg.id_tipo_dano = td.id_tipo_dano WHERE mp.id_personagem = %s"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchall()
                for row in result:
                    magia = {
                        'id_magia': row[0],
                        'nome_magia': row[1],
                        'tipo_dano': row[2]
                    }
                    self.set_magia(magia)                
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    @truque.setter
    def set_truque(self,value):
        self.truques.append(value)
        
    @property
    def truque(self,value):
        return self.truques[value]
    
    @property
    def truques(self):
        return self.truques
    
    def adicionar_truque_banco(self,id_truque):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO truque_personagem(id_personagem,id_magia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_truque))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
    
    def carregar_truques_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """SELECT tq.id_truque, tq.nome_truque, td.nome_tipo FROM truque_personagem tp 
                JOIN truque tq ON tp.id_truque = tq.id_truque 
                JOIN tipo_dano td ON tq.id_tipo_dano = td.id_tipo_dano WHERE tp.id_personagem = %s"""
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchall()
                for row in result:
                    truque = {
                        'id_truque': row[0],
                        'nome_truque': row[1],
                        'tipo_dano': row[2]
                    }
                self.set_truque(truque) 
                return True
            return False
        except Exception as e:
            print(e)
            return False
#-----------------------------------------------GERAL-----------------------------------------------   
    @nome_personagem.setter
    def set_nome_personagem(self,value):
        self.nome_personagem=value
        
    @property
    def nome_personagem(self):
        return self.nome_personagem
    
    @set_classe.setter
    def set_classe(self,value):
        self.classe.append(value)
    
    @property
    def classe(self):
        return self.classe
         
    @xp.setter
    def set_xp(self,value):
        self.xp=value
    
    @property
    def xp(self):
        return self.xp
        
    @raca.setter
    def set_raca(self,value):
        self._raca=value
        
    @property
    def raca(self):
        return self._raca
        
    @bonus_proficiencia.setter
    def set_bonus_proficiencia(self,value):
        self._bonus_proficiencia=value
        
    @property
    def bonus_proficiencia(self):
        return self._bonus_proficiencia
        
    @deslocamento.setter
    def set_deslocamento(self,value):
        self._deslocamento=value
        
    @property
    def deslocamento(self):
        return self._deslocamento
        
    @iniciativa.setter
    def set_iniciativa(self,value):
        self.iniciativa=value
        
    @property
    def iniciativa(self):
        return self.iniciativa
    
    @vida.setter
    def set_vida(self,value):
        self.vida=value
        
    @property
    def vida(self):
        return self.vida
    
    @inspiracao.setter
    def set_inspiracao(self,value):
        self.inspiracao=value
        
    @property
    def inspiracao(self):
        return self.inspiracao
    
    @ca.setter
    def set_ca(self,value):
        self._ca=value
    
    @property
    def ca(self):
        return self._ca        
#-----------------------------------------------ATRIBUTOS-----------------------------------------------
    def adicionar_atributos_banco(self,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO atributos(id_personagem,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
                mycursor.execute(query, (self._id_personagem,forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
    
    def carregar_atributos_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT * FROM atributos WHERE id_personagem = %s"
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone() 
                for row in result:
                    self.set_forca=row[2]
                    self.set_destreza=row[3]
                    self.set_constituicao=row[4]
                    self.set_inteligencia=row[5]
                    self.set_sabedoria=row[6]
                    self.set_carisma=row[7]
                    self.set_bonus_proficiencia=row[8]
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    @set_forca.setter
    def set_forca(self,value):
        self.atributos['forca']=value
        
    @property
    def forca(self):
        if self.atributos['forca'] is None:
            return 0
        return self.atributos['forca']
    
    @property
    def bonus_forca(self):
        return attributes.loc[self.atributos['forca']]
        
    @set_destreza.setter
    def set_destreza(self,value):
        self.atributos['destreza']=value
        
    @property
    def destreza(self):
        if self.atributos['destreza'] is None:
            return 0
        return self.atributos['destreza']
    
    @property
    def bonus_destreza(self):
        return attributes.loc[self.atributos['destreza']]
        
    @set_constituicao.setter
    def set_constituicao(self,value):
        self.atributos['constituicao']=value
        
    @property
    def constituicao(self):
        if self.atributos['constituicao'] is None:
            return 0
        return self.atributos['constituicao']
    
    @property
    def bonus_constituicao(self):
        return attributes.loc[self.atributos['constituicao']]
        
    @set_inteligencia.setter
    def set_inteligencia(self,value):
        self.atributos['inteligencia']=value
        
    @property
    def inteligencia(self):
        if self.atributos['inteligencia'] is None:
            return 0
        return self.atributos['inteligencia']
    
    @property
    def bonus_inteligencia(self):
        return attributes.loc[self.atributos['inteligencia']]
        
    @set_sabedoria.setter
    def set_sabedoria(self,value):
        self.atributos['sabedoria']=value
        
    @property
    def sabedoria(self):
        if self.atributos['sabedoria'] is None:
            return 0
        return self.atributos['sabedoria']
    
    @property
    def bonus_sabedoria(self):
        return attributes.loc[self.atributos['sabedoria']]
        
    @set_carisma.setter
    def set_carisma(self,value):
        self.atributos['carisma']=value
    
    @property
    def carisma(self):
        if self.atributos['carisma'] is None:
            return 0
        return self.atributos['carisma']
    
    @property
    def bonus_carisma(self):
        return attributes.loc[self.atributos['carisma']]
#-----------------------------------------------CARACTERISTICAS----------------------------------------------- 
    def adicionar_caracteristicas_banco(self,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = """INSERT INTO caracteristicas_personagem
                (id_personagem,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
                mycursor.execute(query, (self._id_personagem,idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
    
    def carregar_caracteristicas_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT * FROM caracteristicas_personagem WHERE id_personagem = %s"
                mycursor.execute(query, (self._id_personagem))
                result = mycursor.fetchone() 
                for row in result:
                    self.set_idade=row[2]
                    self.set_cor_olhos=row[3]
                    self.set_cor_pele=row[4]
                    self.set_cor_cabelo=row[5]
                    self.set_peso=row[6]
                    self.set_altura=row[7]
                    self.set_imagem_personagem=row[8]
                return True
            return False
        except Exception as e:
            print(e)
            return False
    
    @set_idade.setter
    def set_idade(self,value):
        self.caracteristicas['idade']=value
    
    @property
    def idade(self):
        self.caracteristicas['idade']
    
    @set_altura.setter
    def set_altura(self,value):
        self.caracteristicas['altura']=value
        
    @property
    def altura(self):
        return self.caracteristicas['altura']
    
    @set_peso.setter
    def set_peso(self,value):
        self.caracteristicas['peso']=value
    
    @property
    def peso(self):
        return self.caracteristicas['peso']
    
    @set_cor_olhos.settet
    def set_cor_olhos(self,value):
        self.caracteristicas['cor dos olhos']=value
        
    @property
    def cor_olhos(self):
        return self.caracteristicas['cor dos olhos']
    
    @set_cor_pele.setter
    def set_cor_pele(self,value):
        self.caracteristicas['cor da pele']=value
    
    @property
    def cor_pele(self):
        return self.caracteristicas['cor da pele']
    
    @set_cor_cabelo.setter
    def set_cor_cabelo(self,value):
        self.caracteristicas['cor do cabelo']=value
    
    @property
    def cor_cabelo(self):
        return self.caracteristicas['cor do cabelo']  
    
    @set_imagem_personagem.setter
    def set_imagem_personagem(self,value):
        self.caracteristicas['imagem_personagem']=value
        
    @property
    def imagem_personagem(self):
        return self.caracteristicas['imagem_personagem']
#-----------------------------------------------SALVAGUARDAS-----------------------------------------------
    @salvaguardas.setter
    def set_salvaguardas(self, value):
        self._salvaguardas.append(value)
        
    @property
    def savalguardas(self):
        return self._salvaguardas
    
    @property
    def resistencia_forca(self):
        if 'forca' in self._salvaguardas:
            return self.atributos['forca']+self._bonus_proficiencia
        return self.atributos['forca']
    
    @property
    def resistencia_destreza(self):
        if 'destreza' in self._salvaguardas:
            return self.atributos['destreza']+self._bonus_proficiencia
        return self.atributos['destreza']
    
    @property
    def resistencia_constituicao(self):
        if 'constituicao' in self._salvaguardas:
            return self.atributos['constituicao']+self._bonus_proficiencia
        return self.atributos['constituicao']
    
    @property
    def resistencia_inteligencia(self):
        if 'inteligencia' in self._salvaguardas:
            return self.atributos['inteligencia']+self._bonus_proficiencia
        return self.atributos['inteligencia']
    
    @property
    def resistencia_sabedoria(self):
        if 'sabedoria' in self._salvaguardas:
            return self.atributos['sabedoria']+self._bonus_proficiencia
        return self.atributos['sabedoria']
    
    @property
    def resistencia_carisma(self):
        if 'carisma' in self._salvaguardas:
            return self.atributos['carisma']+self._bonus_proficiencia
        return self.atributos['carisma']
#-----------------------------------------------PERICIAS-----------------------------------------------
    def adicionar_pericias_banco(self,id_pericia):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "INSERT INTO pericia_personagem(id_personagem,id_pericia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_pericia))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
    
    def carregar_pericias_do_banco(self):
        try:
            if self._id_personagem:
                mycursor = mydb.cursor()
                query = "SELECT pp.id_pericia, pc.nome_pericia, pc.status_uso FROM pericia_personagem pp JOIN pericia pc ON pp.id_pericia = pc.id_pericia WHERE pp.id_personagem = %s;"
                mycursor.execute(query, (self._id_personagem,))
                result = mycursor.fetchall() 
                for row in result:
                    self.set_pericias({'id_pericia': row[0], 'nome_pericia': row[1], 'status_uso': row[2]})
                return True
            return False
        except Exception as e:
            print(e)
            return False

    @property
    def pericias(self):
        return self._pericias

    @pericias.setter
    def pericias(self, value):
        self._pericias.append(value)
        
    @property
    def acrobacia(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self.atributos['destreza'] + self._bonus_proficiencia
        return self.atributos['destreza']

    @property
    def arcanismo(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self.atributos['inteligencia'] + self._bonus_proficiencia
        return self.atributos['inteligencia']

    @property
    def atletismo(self):
        if any(d.get('nome_pericia') == 'forca' for d in self._pericias):
            return self.atributos['forca'] + self._bonus_proficiencia
        return self.atributos['forca']

    @property
    def atuacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self.atributos['carisma'] + self._bonus_proficiencia
        return self.atributos['carisma']

    @property
    def enganacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self.atributos['carisma'] + self._bonus_proficiencia
        return self.atributos['carisma']

    @property
    def furtividade(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self.atributos['destreza'] + self._bonus_proficiencia
        return self.atributos['destreza']

    @property
    def historia(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self.atributos['inteligencia'] + self._bonus_proficiencia
        return self.atributos['inteligencia']

    @property
    def intimidacao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self.atributos['carisma'] + self._bonus_proficiencia
        return self.atributos['carisma']

    @property
    def intuicao(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self.atributos['sabedoria'] + self._bonus_proficiencia
        return self.atributos['sabedoria']

    @property
    def investigacao(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self.atributos['inteligencia'] + self._bonus_proficiencia
        return self.atributos['inteligencia']

    @property
    def lidar_com_animais(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self.atributos['sabedoria'] + self._bonus_proficiencia
        return self.atributos['sabedoria']

    @property
    def medicina(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self.atributos['sabedoria'] + self._bonus_proficiencia
        return self.atributos['sabedoria']

    @property
    def natureza(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self.atributos['inteligencia'] + self._bonus_proficiencia
        return self.atributos['inteligencia']

    @property
    def percepcao(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self.atributos['sabedoria'] + self._bonus_proficiencia
        return self.atributos['sabedoria']

    @property
    def persuasao(self):
        if any(d.get('nome_pericia') == 'carisma' for d in self._pericias):
            return self.atributos['carisma'] + self._bonus_proficiencia
        return self.atributos['carisma']

    @property
    def prestidigitacao(self):
        if any(d.get('nome_pericia') == 'destreza' for d in self._pericias):
            return self.atributos['destreza'] + self._bonus_proficiencia
        return self.atributos['destreza']

    @property
    def religiao(self):
        if any(d.get('nome_pericia') == 'inteligencia' for d in self._pericias):
            return self.atributos['inteligencia'] + self._bonus_proficiencia
        return self.atributos['inteligencia']

    @property
    def sobrevivencia(self):
        if any(d.get('nome_pericia') == 'sabedoria' for d in self._pericias):
            return self.atributos['sabedoria'] + self._bonus_proficiencia
        return self.atributos['sabedoria']