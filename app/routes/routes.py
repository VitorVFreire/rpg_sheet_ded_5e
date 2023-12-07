from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify, abort, make_response, send_file
from flask_session import Session
import asyncio

from main import app
from src import Skill, Race, Classe, SavingThrow, Spell, Equipment
from src import Character, User, Room, Image, KindEquipment, TypeDamage, Coin

@app.route('/')
def index():
    return render_template('index.html', id=session.get('user_id')), 200
    
@app.route('/login')
def login():
    try:
        if session.get('user_id'):
            return redirect(url_for('index'))
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/login')
async def login_registration():
    try:
        user = User(email=request.form.get('email'), password=request.form.get('password'))
        if await user.user_validate():
            session['user_id'] = user.user_id
            return redirect(url_for('index'))
        return redirect(url_for('login')), 406
    except Exception as e:
        print(e)
        abort(500)

@app.route('/logout')
def logout():
    try:
        session['user_id'] = None
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/user_registration')
def render_user_registration():
    try:
        if session.get('user_id'):
            return redirect(url_for('index'))
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)

@app.post('/user_registration')
async def user_registration():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user_name = request.form.get('user_name')
        birth_date = request.form.get('birth_date')
        
        user = User(user_name = user_name, email = email, password = password, birth_date = birth_date)
        
        if await user.insert_user():
            session['user_id'] = user.user_id
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return jsonify({'result': False})
    
@app.delete('/delete/user')
async def delete_user():
    try:
        user_id = session.get('user_id')
        user = User(user_id=user_id)
                
        await user.delete_user()
        
        return jsonify({'message': 'Conta Encerrada com sucesso!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 200

@app.route('/create_character')
async def render_create_character():
    try:
        if session.get('user_id') is None:
            abort(403)
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/classes')
async def get_classes():
    try:
        if session.get('user_id') is None:
            abort(403)
        
        classes = Classe()
        
        return jsonify({'result':True, 'data': await classes.classes})
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/races')
async def get_races():
    try:
        if session.get('user_id') is None:
            abort(403)
        
        races = Race()
        
        return jsonify({'result':True, 'data': await races.races})
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/types_damage')
async def get_type_damage():
    try:
        if session.get('user_id') is None:
            abort(403)
        
        type_damage = TypeDamage()
                
        return jsonify({'result':True, 'data': await type_damage.types_damage})
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/kind_equipments')
async def get_kind_equipment():
    try:
        if session.get('user_id') is None:
            abort(403)
        
        kind_equipment = KindEquipment()
        
        return jsonify({'result':True, 'data': await kind_equipment.kind_equipments})
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/coins')
async def get_coin():
    try:
        if session.get('user_id') is None:
            abort(403)
        
        coin = Coin()
        
        return jsonify({'result':True, 'data': await coin.coins})
    except Exception as e:
        print(e)
        abort(404)
            
@app.route('/characters_page')
async def characters():
    try:
        user_id = session.get('user_id')
        
        if user_id is None:
            abort(403)
        
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
    
@app.route('/character_page/<character_id>')
async def character(character_id):
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()
        
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(403, 'Error: 403\nAcesso Negado')
                 
@app.route('/add_spell/<character_id>')
async def render_character_spell(character_id):
    try:
        character = Character()
        
        #await character.character_belongs_user()
                
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/get_spell/<character_id>')
async def get_character_spells(character_id):
    try:
        spell = Spell()
        
        if await spell.load_spells():
            await spell.load_character_spells(character_id=character_id)
            return jsonify({'result': True, 'data': await spell.spells})
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        abort(404)
        
@app.route('/add_equipment/<character_id>')
async def render_character_equipment(character_id):
    try:
        character = Character()
        
        await character.character_belongs_user()
        
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)

@app.route('/get_equipment/<character_id>')
async def get_character_equipments(character_id):
    try:
        equipments = Equipment()
        
        if await equipments.load_equipments():
            await equipments.load_character_equipments(character_id=character_id)
            return jsonify({'result': True, 'data': equipments.equipments})
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/user')
async def get_name_user():
    try:
        user_id = session.get('user_id')
        
        if user_id is None:
            abort(403)                
        
        user = User(user_id=user_id)
        
        await user.load_user()

        return jsonify({'result': True, 'data': {'user_name': user.user_name}})        
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/openimg/<img>')
def open_img(img): 
    try:  
        img = Image(name=img)
        if img.file is None:
            img.directory('static/img')
        return send_file(img.file)   
    except Exception as e:
        print(e)
        return send_file(Image().img_default) 
