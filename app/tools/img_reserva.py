import pathlib 

def img_reserva():
    directory=pathlib.Path('static/img')
    arquivo = list(directory.glob('personagem.png'))
    return str(arquivo[0])