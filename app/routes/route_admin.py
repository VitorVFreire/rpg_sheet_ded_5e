from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session
import asyncio

from main import app
from src import User, Character, Classe, Race, Skill, SavingThrow, Spell, Equipment

@app.route('/admin')
async def admin():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('admin/admin_pag.html',titulo='ADMIN')
    return redirect(url_for('index'))

@app.route('/criar_classe')
async def new_class():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('admin/add_classe.html',titulo='Nova Classe')
    return redirect(url_for('index'))
    
@app.post('/criar_classe')
async def insert_class():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            classe = Classe(class_name=request.form.get('nome_classe'))
            return jsonify({'result': await classe.insert_class()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_raca')
async def new_race():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('admin/add_raca.html',titulo='Nova raca')
    return redirect(url_for('index'))
    
@app.post('/criar_raca')
async  def insert_race():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            race_name = request.form.get('nome_raca')
            
            race = Race(race_name=race_name)
            
            return jsonify({'result': await race.insert_race()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_pericia')
async def new_skill():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('admin/add_pericia.html',titulo='Nova pericia')
    return redirect(url_for('index'))
    
@app.post('/criar_pericia')
async def insert_skill():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            skill_name = request.form.get('nome_pericia')
            usage_status = request.form.get('status_uso',)
            
            skill = Skill(skill_name=skill_name,usage_status=usage_status)
            
            return jsonify({'result': await skill.insert_skill()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_salvaguarda')
async def new_saving_throw_name():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('admin/add_salvaguarda.html',titulo='Nova salvaguarda')
    return redirect(url_for('index'))
    
@app.post('/criar_salvaguarda')
async def insert_saving_throw_name():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            saving_throw_name = request.form.get('nome_salvaguarda')
            
            saving_throw_name = SavingThrow(saving_throw_name=saving_throw_name)
            
            return jsonify({'result': await saving_throw_name.insert_saving_throw()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/spell_register')
async def new_spell():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('index.html', id=session.get('user_id')), 200
    return redirect(url_for('index'))
    
@app.post('/spell_register')
async def insert_spell():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            spell_name = request.form.get('spell_name')
            attribute_use = request.form.get('attribute_use')
            side_dice = request.form.get('side_dice')
            description_spell = request.form.get('description_spell')
            type_damage_id = request.form.get('type_damage_id')
            amount_dice = request.form.get('amount_dice')
            spell_level = request.form.get('spell_level')
            add_per_level = request.form.get('add_per_level')
            
            spell = Spell(
                attribute_use=attribute_use,
                side_dice=side_dice,
                description_spell=description_spell,
                spell_name=spell_name,
                type_damage_id=type_damage_id,
                amount_dice=amount_dice,
                spell_level=spell_level,
                add_per_level=add_per_level
                )
            
            return jsonify({'result': await spell.insert_spell()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/equipment_register')
async def new_equipment():
    user = User(user_id=session.get('user_id'))
    
    if await user.valid_admin_user():
        return render_template('index.html', id=session.get('user_id')), 200
    return redirect(url_for('index'))
    
@app.post('/equipment_register')
async def insert_equipment():
    try:
        user = User(user_id=session.get('user_id'))
        
        if await user.valid_admin_user():
            kind_equipment_id = request.form.get("kind_equipment_id", default=None) 
            equipment_name = request.form.get('equipment_name', default=None)
            description_equipment = request.form.get('description_equipment', default=None)
            price = request.form.get('price', default=None)
            weight = request.form.get('weight', default=None)
            armor_class = request.form.get('armor_class', default=None)
            bonus = request.form.get('bonus', default=None)
            equipment_image = request.files.get('equipment_image', default=None)
            amount_dice = request.form.get('amount_dice', default=None)
            side_dice = request.form.get('side_dice', default=None)
            type_damage_id = request.form.get('type_damage_id', default=None)
            coin_id = request.form.get('coin_id', default=None)
            
            equipment = Equipment(
                kind_equipment_id=kind_equipment_id,
                equipment_name=equipment_name,
                description_equipment=description_equipment,
                price=price,
                weight=weight,
                armor_class=armor_class,
                amount_dice = amount_dice,
                side_dice = side_dice,
                bonus=bonus,
                equipment_image=equipment_image,
                type_damage_id = type_damage_id, 
                coin_id = coin_id
            )
            
            return jsonify({'result': await equipment.insert_equipment()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})