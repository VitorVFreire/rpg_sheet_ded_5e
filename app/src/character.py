from database import mydb
from src import User
print(attributes.loc[1]+attributes.loc[17])


class Character(User):
    def __init__(self, id_user):
        super().__init__(id=id_user)
        self._id = id_user
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
        
    @magia.setter
    def magia(self,value):
        self.magias.append(value)
        
    @property
    def magia(self,value=None):
        return self.magias[value]

#-----------------------------------------------GERAL-----------------------------------------------        
    @xp.setter
    def xp(self,value):
        self.xp=value
        
    @raca.setter
    def raca(self,value):
        self._raca=value
        
    @bonus_proficiencia.setter
    def bonus_proficiencia(self,value):
        self._bonus_proficiencia=value
        
    @deslocamento.setter
    def deslocamento(self,value):
        self._deslocamento=value
        
    @iniciativa.setter
    def iniciativa(self,value):
        self.iniciativa=value
    
    @vida.setter
    def vida(self,value):
        self.vida=value
    
    @inspiracao.setter
    def inspiracao(self,value):
        self.inspiracao=value
    
    @ca.setter
    def ca(self,value):
        self._ca=value
        
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
#-----------------------------------------------SALVAGUARDAS-----------------------------------------------
    @salvaguardas.setter
    def set_salvaguardas(self, value):
        self._salvaguardas = value
        
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
        self._pericias=value
        
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