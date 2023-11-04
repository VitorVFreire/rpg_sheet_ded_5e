from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, abort, make_response, send_file
from flask_session import Session
import asyncio

from main import app
from src import Skill, Race, Classe, SavingThrow, Spell, Equipment
from src import Character, User, Room, Image

@app.route('/')
def index():
    return render_template('index.html', id=session.get('id_user')), 200
    
@app.route('/login')
def login():
    try:
        if session.get('id_user'):
            return redirect(url_for('index'))
        return render_template('index.html', id=session.get('id_user')), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/login')
async def login_registration():
    try:
        user = User(email=request.form.get('email'), password=request.form.get('senha'))
        if await user.valid_user():
            session['id_user'] = user.id_user
            #return render_template('index.html', titulo = 'home', msg = 'Logado'), 200
            return redirect(url_for('index'))
        return redirect(url_for('login')), 406
    except Exception as e:
        print(e)
        abort(500)

@app.route('/logout')
def logout():
    try:
        session['id_user'] = None
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/cadastro_usuario')
def render_user_registration():
    try:
        if session.get('id_user'):
            return redirect(url_for('index'))
        return render_template('cadastro_usuario.html', titulo = 'cadastro de usuario'), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/cadastro_usuario')
async def user_registration():
    try:
        email = request.form.get('email')
        password = request.form.get('senha')
        name = request.form.get('nome')
        birth_date = request.form.get('data_nascimento')
        
        user = User(name = name, email = email, password = password, birth_date = birth_date)
        
        if await user.insert_user():
            session['id_usuario'] = user.id_user
            return render_template('index.html', titulo = 'home', msg = 'logado'), 200
        return render_template('login.html', titulo = 'login', msg = 'Erro no Login')
    except Exception as e:
        print(e)
        return jsonify({'result': False})
    
@app.delete('/delete/usuario')
async def delete_user():
    try:
        id_user = session.get('id_user')
        user = User(id_user=id_user)
                
        await user.delete_user()
        
        return jsonify({'message': 'Conta Encerrada com sucesso!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 200

@app.route('/criar_personagem')
async def render_create_character():
    try:
        if session.get('id_user') is None:
            abort(403)
        
        races = Race()
        classes = Classe()
        
        return render_template('create_personagem.html', titulo = 'Criar Personagem', racas= await races.races, classes = await classes.classes), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/personagens')
async def characters():
    try:
        id_user = session.get('id_user')
        
        if id_user is None:
            abort(403)
        
        return render_template('index.html', id=session.get('id_user')), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
    
@app.route('/personagem/<id_character>')
async def character(id_character):
    try:
        id_user = session.get('id_user')
        character = Character(id_user=id_user, id_character=id_character)

        await character.character_belongs_user()
        
        await character.load_user()
        await character.load_character()
        await character.load_character_classes()
                
        '''return render_template(
            'ficha_personagem.html',
            titulo = character.character_name,
            raca = character.race,
            nome = character.name,
            classe = character.classe,
            id_personagem = character.id_character,
            nome_personagem = character.character_name,
        ), 200'''
        return render_template('index.html', id=session.get('id_user')), 200
    except Exception as e:
        print(e)
        abort(403, 'Error: 403\nAcesso Negado')
                 
@app.route('/personagem/adicionar_habilidade/<id_character>')
async def render_character_spell(id_character):
    try:
        spell = Spell()
        
        await spell.load_spells()
        await spell.load_character_spells(id_character)
                
        return render_template('adicionar_habilidade_personagem.html', habilidades = await spell.spells, id_personagem = id_character), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/personagem/adicionar_equipamento/<id_character>')
async def render_character_equipment(id_character):
    try:
        equipments = Equipment()
        
        await equipments.load_equipments()
        await equipments.load_character_equipments(id_character=id_character)
        return render_template('adicionar_equipamento_personagem.html', equipamentos = equipments.equipments, id_personagem = id_character), 200
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
