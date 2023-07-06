from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session

from main import app
from src import Usuario, Personagem, Pericia, Raca

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('login.html',titulo='login',msg='Erro no Login')

@app.route('/logout')
def logout():
    session['id_usuario'] = None
    return render_template('index.html',titulo='home',msg='Logout')

@app.post('/login')
def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if usuario.valid_usuario():
        session['id_usuario']=usuario.id
        return render_template('index.html',titulo='home',msg='Logado')
    return redirect(url_for('login'))

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
    return f"Acessado ficha {personagem.nome_personagem} de {personagem.nome} id:{personagem.id}"