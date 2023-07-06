from .database import mydb
import pandas as pd
import os
import pathlib
diretorio = pathlib.Path('database')
caminho_arquivo = diretorio / 'attributes.json'
attributes = pd.read_json(caminho_arquivo)