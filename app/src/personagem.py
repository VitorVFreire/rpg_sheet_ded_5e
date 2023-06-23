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
        self.caracteristicas = {
            'idade': None,
            'altura': None,
            'peso': None,
            'cor dos olhos': None,
            'cor da pele': None,
            'cor do cabelo': None
        }
        self.status = {
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
                query = "INSERT INTO magias_personagem(id_personagem,id_magia) VALUES(%s,%s);"
                mycursor.execute(query, (self._id_personagem,id_magia))
                mydb.commit()
                return True
            return False
        except EOFError as e:
            print(e)
            return False
        
    def carregar_magias_do_banco(self):
        try:
            if self._id:
                mycursor = mydb.cursor()
                query = "SELECT "
                mycursor.execute(query, (self._id,))
                result = mycursor.fetchall()
                self.magias = [row[0] for row in result]
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
#-----------------------------------------------STATUS-----------------------------------------------
    @set_forca.setter
    def set_forca(self,value):
        self.status['forca']=value
        
    @property
    def forca(self):
        if self.status['forca'] is None:
            return 0
        return self.status['forca']
    
    @property
    def bonus_forca(self):
        return attributes.loc[self.status['forca']]
        
    @set_destreza.setter
    def set_destreza(self,value):
        self.status['destreza']=value
        
    @property
    def destreza(self):
        if self.status['destreza'] is None:
            return 0
        return self.status['destreza']
    
    @property
    def bonus_destreza(self):
        return attributes.loc[self.status['destreza']]
        
    @set_constituicao.setter
    def set_constituicao(self,value):
        self.status['constituicao']=value
        
    @property
    def constituicao(self):
        if self.status['constituicao'] is None:
            return 0
        return self.status['constituicao']
    
    @property
    def bonus_constituicao(self):
        return attributes.loc[self.status['constituicao']]
        
    @set_inteligencia.setter
    def set_inteligencia(self,value):
        self.status['inteligencia']=value
        
    @property
    def inteligencia(self):
        if self.status['inteligencia'] is None:
            return 0
        return self.status['inteligencia']
    
    @property
    def bonus_inteligencia(self):
        return attributes.loc[self.status['inteligencia']]
        
    @set_sabedoria.setter
    def set_sabedoria(self,value):
        self.status['sabedoria']=value
        
    @property
    def sabedoria(self):
        if self.status['sabedoria'] is None:
            return 0
        return self.status['sabedoria']
    
    @property
    def bonus_sabedoria(self):
        return attributes.loc[self.status['sabedoria']]
        
    @set_carisma.setter
    def set_carisma(self,value):
        self.status['carisma']=value
    
    @property
    def carisma(self):
        if self.status['carisma'] is None:
            return 0
        return self.status['carisma']
    
    @property
    def bonus_carisma(self):
        return attributes.loc[self.status['carisma']]
#-----------------------------------------------CARACTERISTICAS----------------------------------------------- 
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
            return self.status['forca']+self._bonus_proficiencia
        return self.status['forca']
    
    @property
    def resistencia_destreza(self):
        if 'destreza' in self._salvaguardas:
            return self.status['destreza']+self._bonus_proficiencia
        return self.status['destreza']
    
    @property
    def resistencia_constituicao(self):
        if 'constituicao' in self._salvaguardas:
            return self.status['constituicao']+self._bonus_proficiencia
        return self.status['constituicao']
    
    @property
    def resistencia_inteligencia(self):
        if 'inteligencia' in self._salvaguardas:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def resistencia_sabedoria(self):
        if 'sabedoria' in self._salvaguardas:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']
    
    @property
    def resistencia_carisma(self):
        if 'carisma' in self._salvaguardas:
            return self.status['carisma']+self._bonus_proficiencia
        return self.status['carisma']
#-----------------------------------------------PERICIAS-----------------------------------------------
    @pericias.setter
    def set_pericias(self,value):
        self._pericias.append(value)
        
    @property
    def pericias(self):
        return self._pericias
        
    @property
    def acrobacia(self):
        if 'destreza' in self._pericias:
            return self.status['destreza']+self._bonus_proficiencia
        return self.status['destreza']
    
    @property
    def arcanismo(self):
        if 'inteligencia' in self._pericias:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def atletismo(self):
        if 'forca' in self._pericias:
            return self.status['forca']+self._bonus_proficiencia
        return self.status['forca']
    
    @property
    def atuacao(self):
        if 'carisma' in self._pericias:
            return self.status['carisma']+self._bonus_proficiencia
        return self.status['carisma']
    
    @property
    def enganacao(self):
        if 'carisma' in self._pericias:
            return self.status['carisma']+self._bonus_proficiencia
        return self.status['carisma']
    
    @property
    def furtividade(self):
        if 'destreza' in self._pericias:
            return self.status['destreza']+self._bonus_proficiencia
        return self.status['destreza']
    
    @property
    def historia(self):
        if 'inteligencia' in self._pericias:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def intimidacao(self):
        if 'carisma' in self._pericias:
            return self.status['carisma']+self._bonus_proficiencia
        return self.status['carisma']
    
    @property
    def intuicao(self):
        if 'sabedoria' in self._pericias:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']
    
    @property
    def investigacao(self):
        if 'inteligencia' in self._pericias:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def lidas_com_animais(self):
        if 'sabedoria' in self._pericias:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']
    
    @property
    def medicina(self):
        if 'sabedoria' in self._pericias:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']
    
    @property
    def natureza(self):
        if 'inteligencia' in self._pericias:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def percepcao(self):
        if 'sabedoria' in self._pericias:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']
    
    @property
    def persuasao(self):
        if 'carisma' in self._pericias:
            return self.status['carisma']+self._bonus_proficiencia
        return self.status['carisma']
    
    @property
    def prestidigitacao(self):
        if 'destreza' in self._pericias:
            return self.status['destreza']+self._bonus_proficiencia
        return self.status['destreza']
    
    @property
    def religiao(self):
        if 'inteligencia' in self._pericias:
            return self.status['inteligencia']+self._bonus_proficiencia
        return self.status['inteligencia']
    
    @property
    def sobrevivencia(self):
        if 'sabedoria' in self._pericias:
            return self.status['sabedoria']+self._bonus_proficiencia
        return self.status['sabedoria']