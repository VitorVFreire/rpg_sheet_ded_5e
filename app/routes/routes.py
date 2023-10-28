from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, abort, make_response, send_file
from flask_session import Session
import asyncio

from main import app
from src import Skill, Race, Classe, SavingThrow, Spell, Equipment
from src import Character, User, Room, Image

@app.route('/')
def index():
    return render_template('index.html',titulo = 'home'), 200
    
@app.route('/login')
def login():
    try:
        if session.get('id_usuario'):
            return redirect(url_for('index'))
        return render_template('login.html',titulo = 'login'), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/login')
async def cadastro_login():
    try:
        usuario = User(email=request.form.get('email'), password=request.form.get('senha'))
        if await usuario.valid_user():
            session['id_usuario'] = usuario.id_user
            #return render_template('index.html', titulo = 'home', msg = 'Logado'), 200
            return redirect(url_for('index'))
        return redirect(url_for('login')), 406
    except Exception as e:
        print(e)
        abort(500)

@app.route('/logout')
def logout():
    try:
        session['id_usuario'] = None
        session.clear()
        return render_template('index.html', titulo = 'home', msg = 'Logout'), 200
    except Exception as e:
        print(e)
        abort(404)

@app.route('/cadastro_usuario')
def criar_usuario():
    try:
        if session.get('id_usuario'):
            return redirect(url_for('index'))
        return render_template('cadastro_usuario.html', titulo = 'cadastro de usuario'), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/cadastro_usuario')
async def cadastro_usuario():
    try:
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        
        usuario = User(name = nome, email = email, password = senha, birth_date = data_nascimento)
        
        if await usuario.insert_user():
            session['id_usuario'] = usuario.id_user
            return render_template('index.html', titulo = 'home', msg = 'logado'), 200
        return render_template('login.html', titulo = 'login', msg = 'Erro no Login')
    except Exception as e:
        print(e)
        return jsonify({'result': False})
    
@app.delete('/delete/usuario')
async def delete_usuario():
    try:
        id_usuario = session.get('id_usuario')
        usuario = User(id=id_usuario)
                
        await usuario.delete_user()
        
        return jsonify({'message': 'Conta Encerrada com sucesso!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 200

@app.route('/criar_personagem')
async def criar_personagem():
    try:
        if session.get('id_usuario') is None:
            abort(403)
        
        racas = Race()
        classes = Classe()
        
        return render_template('create_personagem.html', titulo = 'Criar Personagem', racas= await racas.races, classes = await classes.classes), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/personagens')
async def personagens():
    try:
        id_usuario = session.get('id_usuario')
        
        if id_usuario is None:
            abort(403)
        
        usuario = User(id=id_usuario)
        
        await usuario.load_characters()
        
        return render_template('personagens.html', titulo = 'Personagens', personagens = usuario.characters), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
    
@app.route('/personagem/<id_personagem>')
async def personagem(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Character(id_user=id_usuario, id_character=id_personagem)

        await personagem.character_belongs_user()
        
        await personagem.load_user()
        await personagem.load_character()
        await personagem.load_character_classes()
                
        return render_template(
            'ficha_personagem.html',
            titulo = personagem.character_name,
            raca = personagem.race,
            nome = personagem.name,
            classe = personagem.classe,
            id_personagem = personagem.id_character,
            nome_personagem = personagem.character_name,
        ), 200
    except Exception as e:
        print(e)
        abort(403, 'Error: 403\nAcesso Negado')
                 
@app.route('/personagem/adicionar_habilidade/<id_personagem>')
async def adicionar_habilidade_personagem(id_personagem):
    try:
        habilidades = Spell()
        
        await habilidades.load_spells()
        await habilidades.load_character_spells(id_personagem)
        
        return render_template('adicionar_habilidade_personagem.html', habilidades = await habilidades.spells, id_personagem = id_personagem), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/personagem/adicionar_equipamento/<id_personagem>')
async def adicionar_equipamento_personagem(id_personagem):
    try:
        equipamentos = Equipment()
        
        await equipamentos.load_equipments()
        await equipamentos.load_character_equipments(id_personagem=id_personagem)
        return render_template('adicionar_equipamento_personagem.html', equipamentos = equipamentos.equipments, id_personagem = id_personagem), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/openimg/<img>')
def open_img(img): 
    try:  
        return send_file(Image(name=img).file)   
    except Exception as e:
        print(e)
        return send_file(Image().img_default) 
