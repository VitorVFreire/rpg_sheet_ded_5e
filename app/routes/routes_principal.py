from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session

from main import app
from src import Usuario, Personagem, Pericia, Raca, Classe

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('login.html',titulo='login',msg='Erro no Login')

@app.post('/login')
def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if usuario.valid_usuario():
        session['id_usuario']=usuario.id
        return render_template('index.html',titulo='home',msg='Logado')
    return redirect(url_for('login'))

@app.route('/cadastro_usuario')
def criar_usuario():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('cadastro_usuario.html',titulo='cadastro de usuario')

@app.route('/logout')
def logout():
    session['id_usuario'] = None
    return render_template('index.html',titulo='home',msg='Logout')

@app.route('/criar_personagem')
def criar_personagem():
    racas=Raca()
    return render_template('create_personagem.html',titulo='Criar Personagem',racas=racas.racas)

@app.route('/personagens')
def personagens():
    usuario=Usuario(id=session.get('id_usuario'))
    return render_template('personagens.html',titulo='Personagens',personagens=usuario.personagens)

@app.route('/personagem/<id_personagem>')
def personagem(id_personagem):
    personagem=Personagem(id_usuario=session.get('id_usuario'),id_personagem=id_personagem)
    classe=Classe()
    personagem.carregar_atributos_do_banco()
    return render_template('ficha_personagem.html', titulo=personagem.nome_personagem, personagem=personagem,classes=classe.classes)
    
@app.route('/atributos/<id_personagem>',methods=['POST'])
def update_atributos(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        if personagem.exists_atributos_banco() and chave != 'bonus_proficiencia':
            return jsonify({'result': personagem.update_atributos_banco(chave=chave, valor=valor),
                'bonus': int(personagem.get_bonus(chave=chave))})
        elif personagem.exists_atributos_banco():
            return jsonify({'result': personagem.update_atributos_banco(chave=chave, valor=valor)})
        return jsonify({'result':personagem.adicionar_atributo_banco(chave=chave,valor=valor),
                        'bonus':int(personagem.get_bonus(chave=chave))})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})