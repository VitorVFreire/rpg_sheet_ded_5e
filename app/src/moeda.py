from data import get_connection
import pymysql
import asyncio

"""
1 da -> 100 pl
1 pl -> 100 po
1 po -> 10 pp
1 pe -> 5 pp
1 pp -> 10 pc
"""

class Moeda:
    fatores_de_conversao = {
        'da': {'da': 1, 'pl': 0.01, 'po': 0.0001, 'pe': 0.000002, 'pp': 0.000001, 'pc': 0.0000001},
        'pl': {'da': 100, 'pl': 1, 'po': 0.01, 'pe': 0.0002, 'pp': 0.0001, 'pc': 0.00001},
        'po': {'da': 10000, 'pl': 100, 'po': 1, 'pe': 0.02, 'pp': 0.01, 'pc': 0.001},
        'pe': {'da': 50000, 'pl': 500, 'po': 2, 'pe': 1, 'pp': 0.2, 'pc': 0.02},
        'pp': {'da': 100000, 'pl': 1000, 'po': 10, 'pe': 5, 'pp': 1, 'pc': 0.1},
        'pc': {'da': 1000000, 'pl': 10000, 'po': 100, 'pe': 50, 'pp': 10, 'pc': 1}
    }

    def __init__(self, diamante=None, platina=None, ouro=None, electrum=None, prata=None, cobre=None, origem=None, destino=None, valor=None):
        self.__moedas = {
            'da': diamante,
            'pl': platina,
            'po': ouro,
            'pe': electrum,
            'pp': prata,
            'pc': cobre
        }
        self.__origem = origem
        self.__destino = destino
        self.__valor = valor
        
    @property
    def origem(self):
        return self.__origem
    
    @origem.setter
    def origem(self, value):
        self.__origem = value
        
    @property
    def destino(self):
        return self.__destino
    
    @destino.setter
    def destino(self, value):
        self.__destino = value

    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, valor):
        self.__valor = valor
    
    @property
    def moedas(self):
        return self.__moedas
    
    @moedas.setter
    def moedas(self, diamante=None, platina=None, ouro=None, electrum=None, prata=None, cobre=None):
        self.__moedas = {
            'da': diamante,
            'pl': platina,
            'po': ouro,
            'pe': electrum,
            'pp': prata,
            'pc': cobre
        }
        
    def verifica_moeda(self, chave):
        possiveis_chave = ['da', 'po', 'pl', 'pp', 'pc', 'pe']
        return chave in possiveis_chave
            
    def converter_moedas(self):
        fator = self.fatores_de_conversao.get(self.origem, {}).get(self.destino)
        if fator is not None:
            self.__moedas[self.destino] += self.valor * fator
            self.__moedas[self.origem] -= self.valor
            return self.__moedas[self.destino], self.__moedas[self.origem]
        else:
            print("Conversão não suportada")