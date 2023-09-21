from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, abort
from flask_session import Session
import asyncio

from main import app
from src import Usuario, Pericia, Raca, Classe, Salvaguarda, Habilidade
from src import Personagem

@app.route('/')
def index():
    return render_template('index.html',titulo = 'home')
    
@app.route('/login')
def login():
    try:
        if session.get('id_usuario'):
            return render_template('index.html',titulo = 'home')
        return render_template('login.html',titulo = 'login')
    except EOFError as e:
        print(e)
        abort(404)

@app.post('/login')
async def cadastro_login():
    try:
        usuario = Usuario(email=request.form.get('email'), senha=request.form.get('senha'))
        if await usuario.valid_usuario():
            session['id_usuario'] = usuario.id
            return render_template('index.html', titulo = 'home', msg = 'Logado')
        return redirect(url_for('login'))
    except EOFError as e:
        print(e)
        abort(500)

@app.route('/logout')
def logout():
    try:
        session['id_usuario'] = None
        return render_template('index.html', titulo = 'home', msg = 'Logout')
    except EOFError as e:
        print(e)
        abort(404)

@app.route('/cadastro_usuario')
def criar_usuario():
    try:
        if session.get('id_usuario'):
            return render_template('index.html', titulo = 'home')
        return render_template('cadastro_usuario.html', titulo = 'cadastro de usuario')
    except EOFError as e:
        print(e)
        abort(404)

@app.post('/cadastro_usuario')
async def cadastro_usuario():
    try:
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        
        usuario = Usuario(nome = nome, email = email, senha = senha, data_nascimento = data_nascimento)
        
        if await usuario.create_usuario():
            session['id_usuario'] = usuario.id
            return render_template('index.html', titulo = 'home', msg = 'logado')
        return render_template('login.html', titulo = 'login', msg = 'Erro no Login')
    except EOFError as e:
        print(e)
        return jsonify({'result': False})
    
@app.delete('/delete/usuario')
async def delete_usuario():
    try:
        id_usuario = session.get('id_usuario')
        usuario = Usuario(id_usuario=id_usuario)
                
        await usuario.delete_usuario()
        
        return render_template('index.html', titulo = 'home', msg = 'Conta Encerrada!')
    except EOFError as e:
        print(e)
        return render_template('index.html', titulo = 'home', msg = 'Erro na Exclusão da conta!')

@app.route('/criar_personagem')
async def criar_personagem():
    try:
        racas = Raca()
        classes = Classe()
        
        return render_template('create_personagem.html', titulo = 'Criar Personagem', racas= await racas.racas, classes = await classes.classes)
    except EOFError as e:
        print(e)
        abort(404)
        
@app.route('/personagens')
async def personagens():
    try:
        id_usuario = session.get('id_usuario')
        
        if id_usuario is None:
            abort(403)
        
        usuario = Usuario(id=id_usuario)
        
        return render_template('personagens.html', titulo = 'Personagens', personagens = await usuario.personagens)
    except EOFError as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
    
@app.route('/personagem/<id_personagem>')
async def personagem(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        
        personagem = Personagem(id_usuario=id_usuario, id_personagem=id_personagem)

        await personagem.personagem_pertence_usuario()
        
        await personagem.carregar_personagem_banco()
        await personagem.carregar_classes_do_banco()
        
        return render_template(
            'ficha_personagem.html',
            titulo = await personagem.nome_personagem,
            raca = await personagem.raca,
            nome = await personagem.nome,
            classe = await personagem.classe,
            id_personagem = personagem.id_personagem,
            nome_personagem = await personagem.nome_personagem,
        )
    except EOFError as e:
        print(e)
        abort(403, 'Error: 403\nAcesso Negado')
    
@app.route('/personagem/adicionar_habilidade/<id_personagem>')
async def adicionar_habilidade_personagem(id_personagem):
    try:
        habilidades = Habilidade()
        
        await habilidades.carregar_habilidades()
        await habilidades.carregar_habilidades_personagem_do_banco(id_personagem)
        
        return render_template('adicionar_habilidade_personagem.html', habilidades = await habilidades.habilidades, id_personagem = id_personagem)
    except EOFError as e:
        print(e)
        abort(404)
        
@app.route('/room/<room>/<id_personagem>')
async def room(room, id_personagem):
    try:
        personagem = Personagem(id_usuario=session.get('id_usuario'), id_personagem=id_personagem)
        return render_template('room_game.html', titulo = 'Room', room = room, id_personagem = id_personagem, nome_personagem = await personagem.nome_personagem)
    except EOFError as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")