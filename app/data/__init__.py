from .database import mydb
import pandas as pd
import os
import pathlib
diretorio = pathlib.Path('database')
caminho_arquivo = diretorio / 'attributes.json'
if caminho_arquivo.is_file():
    attributes = pd.read_json(caminho_arquivo)
else:
    attributes=False