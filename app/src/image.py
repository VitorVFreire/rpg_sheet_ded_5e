import time
import os
import pathlib
from flask import url_for

class Image:
    def __init__(self, parameters = None, name = None):
        self.directory = pathlib.Path('data/img')
        self.__parameter = parameters
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value
            
    @property
    def parameter(self):
        return self.__parameter
    
    @parameter.setter
    def parameter(self, value):
        self.__parameter = value
    
    def save_file(self, file):
        try:
            name_base = f'{self.parameter}{file.filename.replace(" ","")}'
            if self.name is not None:
                self.remove_file()
            time_now = int(time.time())
            name = f'{time_now}{name_base}'  
            route = f'{self.directory}/{name}'   
            file.save(route)
            return True, name
        except Exception as e:
            print(e)
            return False, None

    def remove_file(self):
        try:           
            arquivo = list(self.directory.glob(self.name))
            os.remove(arquivo[0])
            return True
        except Exception as e:
            print(e)
            return False
    
    @property
    def file(self):
        arquivo = list(self.directory.glob(self.name))
        return arquivo[0] if arquivo[0] is not None else self.img_default
    
    @property
    def img_default(self):
        self.directory = pathlib.Path('static/img')
        arquivo = list(self.directory.glob('personagem.png'))
        return str(arquivo[0])
    
    @property
    def url_img(self):
        return url_for('open_img', img=self.name if self.name is not None else self.img_default, _external=True)