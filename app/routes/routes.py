from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session
import asyncio

from main import app
from src import Usuario, Pericia, Raca, Classe, Salvaguarda
from src import Personagem

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('login.html',titulo='login',msg='Erro no Login')

@app.post('/login')
async def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if await usuario.valid_usuario():
        session['id_usuario']=usuario.id
        return render_template('index.html',titulo='home',msg='Logado')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['id_usuario'] = None
    return render_template('index.html',titulo='home',msg='Logout')

@app.route('/cadastro_usuario')
def criar_usuario():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('cadastro_usuario.html',titulo='cadastro de usuario')

@app.route('/cadastro_usuario',methods=['POST'])
async def cadastro_usuario():
    try:
        email=request.form.get('email')
        senha=request.form.get('senha')
        nome=request.form.get('nome')
        data_nascimento=request.form.get('data_nascimento')
        
        usuario=Usuario(nome=nome,email=email,senha=senha,data_nascimento=data_nascimento)
        
        if await usuario.create_usuario():
            session['id_usuario'] = usuario.id
            return render_template('index.html',titulo='home',msg='logado')
        return render_template('login.html',titulo='login',msg='Erro no Login')
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/delete/usuario',methods=['POST'])
async def delete_usuario():
    try:
        id_usuario=session.get('id_usuario')
        usuario=Usuario(id_usuario=id_usuario)
                
        await usuario.delete_usuario(id_classe)
        
        return render_template('index.html',titulo='home',msg='Conta Encerrada!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão da conta!')

@app.route('/criar_personagem')
async def criar_personagem():
    racas = Raca()
    return render_template('create_personagem.html',titulo='Criar Personagem',racas= await racas.racas)
    
@app.route('/personagens')
async def personagens():
    usuario=Usuario(id=session.get('id_usuario'))
    return render_template('personagens.html',titulo='Personagens',personagens = await usuario.personagens)

@app.route('/personagem/<id_personagem>')
async def personagem(id_personagem):
    personagem = Personagem(id_usuario=session.get('id_usuario'), id_personagem=id_personagem)
    await personagem.personagem_pertence_usuario()
    await personagem.carregar_personagem_banco()
    return render_template(
        'ficha_personagem.html',
        titulo = await personagem.nome_personagem,
        raca = await personagem.raca,
        nome = await personagem.nome,
        id_personagem = personagem.id_personagem,
        nome_personagem = await personagem.nome_personagem
    )