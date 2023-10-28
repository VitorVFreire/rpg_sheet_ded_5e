from flask import request, redirect, session, jsonify
from flask_session import Session
import asyncio

from main import app
from src import User, Skill, Race, Classe, SavingThrow, Spell, Room, Image, Equipment
from src import Character, CharacterAttribute, CharacterCharacteristics, CharacterSpell
from src import CharacterSkills, CharacterSavingThrow, CharacterStatusBase, CharacterEquipment

@app.post('/personagem')
async def post_character():
    try:
        id_user = session.get('id_usuario')
        character = Character(id_user=id_user)
        
        id_race = request.form.get('id_raca')
        id_class = request.form.get('id_classe')
        character_name = request.form.get('nome_personagem')
        
        return jsonify({'result': (
            await character.insert_character(id_race=id_race,character_name=character_name) 
            and 
            await character.insert_character_class(id_class=id_class)
            ), 
            'id_personagem': character.id_character}), 200     
    except Exception as e:
        print(e)
        return 404

@app.put('/personagem/<id_character>')
async def put_character(id_character):
    try:
        id_user = session.get('id_usuario')
        character = Character(id_user=id_user,id_character=id_character)
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')
        value = request.form.get('valor')
                
        return jsonify({'result': await character.update_character(chave=key,valor=value)}), 200
    except Exception as e:
        print(e)
        return 404
    
@app.delete('/personagem/<id_character>')
async def delete_character(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterCharacteristics(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
                
        return jsonify({'result': (await character.delete_characteristics() and await character.delete_character())}), 200
    except Exception as e:
        print(e)
        return 404
    
@app.get('/caracteristicas/<id_character>')
async def get_character_characteristics(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterCharacteristics(id_character=id_character,id_user=id_user)
            
        await character.character_belongs_user()
        
        if await character.load_characteristics():
            return jsonify(character.characteristic), 200
        return jsonify({'result': False}), 404            
    except Exception as e:
        print(e)
        return 404 

@app.put('/caracteristicas/<id_character>')
async def put_character_characteristics(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterCharacteristics(id_user=id_user, id_character=id_character)
            
        await character.character_belongs_user()
        
        key = request.form.get('chave')
        value = request.form.get('valor')

        if request.files:
            file_upload = request.files.get('img_personagem')
            return jsonify({'result': await character.save_character_image(file=file_upload), 'img_personagem': character.url_img}), 200 

        if await character.exists_characteristics():
            return jsonify({'result': await character.update_characteristics(chave=key,valor=value)}), 200
        else:               
            return jsonify({'result': await character.insert_characteristics(key=key,value=value)}), 200
    except Exception as e:
        print(e)
        return 404  

@app.get('/atributos/<id_character>')
async def get_character_attribute(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterAttribute(id_user=id_user, id_character=id_character)   
        
        await character.character_belongs_user()
        
        if await character.exists_attributes():
            await character.load_attributes()
        
        return jsonify(character.attributes)              
    except Exception as e:
        print(e)
        return 404
    
@app.put('/atributos/<id_character>')
async def put_character_attribute(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterAttribute(id_user=id_user, id_character=id_character)   
                
        await character.character_belongs_user()
        
        key = request.form.get('chave')
        value = request.form.get('valor')

        if await character.exists_attributes() and key != 'bonus_proficiencia':
            update_result = await character.update_attributes(key=key, value=value)
            update_value_bonus = await character.get_bonus(key=key)
            return jsonify({'result': update_result,
                'bonus': update_value_bonus,
                'resistencia': update_value_bonus}), 200
        elif await character.exists_attributes():
            return jsonify({'result': await character.update_attributes(key=key, value=value)}), 200
            
        addition_result = await character.insert_attribute(key=key,value=value)
        addition_value_bonus = await character.get_bonus(key=key)
        return jsonify({'result': addition_result,
                        'bonus': addition_value_bonus,
                        'resistencia': addition_value_bonus}), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/salvaguardas/<id_character>')
async def get_character_saving_throw(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSavingThrow(id_user=id_user, id_character=id_character)  
        
        await character.character_belongs_user()
        
        if await character.exists_attributes():
            await character.load_attributes()
            await character.load_saving_throws()
        
        return jsonify(character.saving_throws)        
    except Exception as e:
        print(e)
        return 404

@app.post('/salvaguardas/<id_character>')
async def post_character_saving_throw(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSavingThrow(id_user=id_user, id_character=id_character)  
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')
            
        saving_throw = SavingThrow(saving_throw_name=key)
            
        if await saving_throw.load_saving_throw_by_name() and await character.load_attributes():
            return jsonify({'result': await character.insert_saving_throws(id_saving_throw=saving_throw.id_saving_throw),
                            'resistencia': await character.get_saving_throws(key)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404  
    
@app.delete('/salvaguardas/<id_character>')
async def delete_character_saving_throw(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSavingThrow(id_user=id_user, id_character=id_character)  
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')
        saving_throw = SavingThrow(saving_throw_name=key)
            
        if await saving_throw.load_saving_throw_by_name() and await character.load_attributes():
            if await character.exists_saving_throw(id_saving_throw=saving_throw.id_saving_throw):
                return jsonify({'result': await character.delete_saving_throw(id_saving_throw=saving_throw.id_saving_throw),
                                'resistencia': await character.get_saving_throws(key)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/status_base/<id_character>')
async def get_character_status_base(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterStatusBase(id_user=id_user, id_character=id_character)          

        await character.character_belongs_user()
        
        if await character.load_status_base():
            return jsonify(character.status_base), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
   
@app.put('/status_base/<id_character>')
async def put_character_status_base(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterStatusBase(id_user=id_user, id_character=id_character)          
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')
        value = request.form.get('valor')
            
        if await character.exists_status_base():
            return jsonify({'result': await character.update_status_base(key=key, value=value)}), 200
        else:
            return jsonify({'result': await character.insert_status_base(key=key,value=value)}),200
    except Exception as e:
        print(e)
        return 404

@app.get('/pericias/<id_character>')
async def get_character_skills(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSkills(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
        
        if await character.exists_attributes():
            await character.load_attributes()
            await character.load_skills()
        return jsonify(character.skill)
    except Exception as e:
        print(e)
        return 404

@app.post('/pericias/<id_character>')
async def post_character_skill(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSkills(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')

        skill = Skill(skill_name=key)
            
        if await skill.load_skill_by_name() and await character.load_attributes():
            return jsonify({'result': await character.insert_skill(id_pericia=skill.id_skill),
                            'pericia': await character.get_skills(chave=key)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.delete('/pericias/<id_character>')
async def delete_character_skill(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSkills(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
        
        key = request.form.get('chave')

        skill = Skill(skill_name=key)
            
        if await skill.load_skill_by_name() and await character.load_attributes():
            if await character.exists_skill(id_pericia=skill.id_skill):
                 return jsonify({'result': await character.delete_skills(id_pericia=skill.id_skill),
                                'pericia': await character.get_skills(chave=key)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/habilidades/<id_character>')
async def get_character_spells(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSpell(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
                
        if await character.exists_spell() and await character.load_spells():
            return jsonify(character.spells), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
@app.post('/habilidades/<id_character>')
async def post_character_spell(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSpell(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
        
        id_spell = request.form.get('id_habilidade')
            
        return jsonify({'result': await character.insert_spell(id_spell=id_spell)}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/habilidades/<id_character>')
async def delete_character_spell(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterSpell(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
        
        id_spell = request.form.get('id_habilidade')
            
        if await character.exists_specific_spell(id_spell=id_spell):
            return jsonify({'result': await character.delete_spell(id_character_spell=id_spell)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
@app.get('/equipamentos/<id_character>')
async def get_character_equipment(id_character):
    try:
        id_user = session.get('id_usuario')
        character = CharacterEquipment(id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
                
        if await character.exists_equipment() and await character.load_equipments():
            return jsonify(character.list_equipments), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
@app.post('/equipamentos/<id_character>')
async def post_character_equipment(id_character):
    try:
        id_user = session.get('id_usuario')
        id_equipment = request.form.get('id_equipamento')
        amount = request.form.get('qtd')
        character = CharacterEquipment(amount=amount,id_equipment=id_equipment,id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
                    
        return jsonify({'result': await character.insert_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.put('/equipamentos/<id_character>')
async def put_character_equipment(id_character):
    try:
        id_user = session.get('id_usuario')
        id_equipment = request.form.get('id_equipamento')
        amount = request.form.get('qtd')
        character = CharacterEquipment(amount=amount,id_equipment=id_equipment,id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
                    
        return jsonify({'result': await character.update_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/equipamentos/<id_character>')
async def delete_character_equipment(id_character):
    try:
        id_user = session.get('id_usuario')
        id_equipment = request.form.get('id_equipamento')
        character = CharacterEquipment(id_equipment=id_equipment,id_user=id_user, id_character=id_character)
        
        await character.character_belongs_user()
            
        if await character.exists_specific_equipment():
            return jsonify({'result': await character.delete_equipment()}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
"""@app.post('/compra_equipamentos/<id_personagem>')
async def compra_equipamentos_personagem_post(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        id_equipamento = request.form.get('id_equipamento')
        personagem = PersonagemEquipamento(id_equipamento=id_equipamento,id_usuario=id_usuario, id_personagem=id_personagem)
        equipamento = Equipamento(id_equipamento=id_equipamento)
        
        await personagem.personagem_pertence_usuario()
        await equipamento.carregar_equipamento()
        personagem.valor = equipamento.preco
        #personagem.
        await personagem.gasto_moeda()
                    
        return jsonify({'result': await personagem.adicionar_equipamento_banco()}), 200
    except Exception as e:
        print(e)
        return 404"""