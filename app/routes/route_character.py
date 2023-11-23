from flask import request, redirect, session, jsonify, url_for
from flask_session import Session
import asyncio

from main import app
from src import User, Skill, Race, Classe, SavingThrow, Spell, Room, Image, Equipment
from src import Character, CharacterAttribute, CharacterCharacteristics, CharacterSpell
from src import CharacterSkills, CharacterSavingThrowTest, CharacterStatusBase, CharacterEquipment

@app.get('/characters')
async def get_characters():
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id)

        if await character.load_characters():
            return jsonify(character.characters), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/character/<character_id>')
async def get_character(character_id):
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id, character_id=character_id)

        if await character.character_belongs_user() and await character.load_character():
            return jsonify(character.character), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.post('/character')
async def post_character():
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id)

        race_id = request.form.get('race_id')
        class_id = request.form.get('class_id')
        character_name = request.form.get('character_name')
        
        if await character.insert_character(race_id=race_id, character_name=character_name) and await character.insert_character_class(class_id=class_id):
            return redirect(url_for('characters'))
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        return 404

@app.put('/character/<character_id>')
async def put_character(character_id):
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        value = request.form.get('value')

        return jsonify({'result': await character.update_character(key=key, value=value)}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/character/<character_id>')
async def delete_character(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterCharacteristics(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        return jsonify({'result': await character.delete_character()}), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/characteristics/<character_id>')
async def get_character_characteristics(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterCharacteristics(character_id=character_id, user_id=user_id)

        await character.character_belongs_user()
        
        if await character.load_characteristics():
            return jsonify(character.characteristic), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.put('/characteristics/<character_id>')
async def put_character_characteristics(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterCharacteristics(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        value = request.form.get('value')

        if request.files:
            file_upload = request.files.get('character_image')
            return jsonify({'result': await character.save_character_image(file=file_upload), 'url': character.url_img}), 200
        if await character.exists_characteristics():
            return jsonify({'result': await character.update_characteristics(key=key, value=value)}), 200
        else:
            return jsonify({'result': await character.insert_characteristics(key=key, value=value)}), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/attributes/<character_id>')
async def get_character_attribute(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterAttribute(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_attributes():
            await character.load_attributes()
        return jsonify(character.attributes)
    except Exception as e:
        print(e)
        return 404

@app.put('/attributes/<character_id>')
async def put_character_attribute(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterAttribute(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        value = request.form.get('value')

        if await character.exists_attributes() and key != 'bonus_proficiencia':
            update_result = await character.update_attributes(key=key, value=value)
            update_value_bonus = await character.get_bonus(key=key)
            return jsonify({'result': update_result,
                            'data': {
                                f'{key}_bonus': update_value_bonus,
                                f'{key}_resistance': update_value_bonus
                            }
                            }), 200
        elif await character.exists_attributes():
            return jsonify({'result': await character.update_attributes(key=key, value=value)}), 200

        addition_result = await character.insert_attribute(key=key, value=value)
        addition_value_bonus = await character.get_bonus(key=key)
        return jsonify({'result': addition_result,
                        'data': {
                            f'{key}_bonus': addition_value_bonus,
                            f'{key}_resistance': addition_value_bonus
                        }
                        }), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/saving_throws/<character_id>')
async def get_character_saving_throw(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSavingThrowTest(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_attributes():
            await character.load_attributes()
            await character.load_saving_throws()

        return jsonify(character.saving_throws), 200
    except Exception as e:
        print(e)
        return 404

@app.post('/saving_throws/<character_id>')
async def post_character_saving_throw(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSavingThrowTest(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        
        key_saving = key.replace('_resistance', '')

        saving_throw = SavingThrow(saving_throw_name=key_saving)
        
        if await saving_throw.load_saving_throw_by_name() and await character.load_attributes():
            return jsonify({'result': await character.insert_saving_throws(saving_throw_id=saving_throw.saving_throw_id),
                'data': {
                    key: await character.get_saving_throws(key)
                }
            }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.delete('/saving_throws/<character_id>')
async def delete_character_saving_throw(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSavingThrowTest(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        
        key_saving = key.replace('_resistance', '')
        
        saving_throw = SavingThrow(saving_throw_name=key_saving)

        if await saving_throw.load_saving_throw_by_name() and await character.load_attributes():
            if await character.exists_saving_throw(saving_throw_id=saving_throw.saving_throw_id):
                return jsonify({'result': await character.delete_saving_throw(saving_throw_id=saving_throw.saving_throw_id),
                    'data': {
                        key: await character.get_saving_throws(key)
                    }
                }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/status_base/<character_id>')
async def get_character_status_base(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterStatusBase(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.load_status_base():
            return jsonify(character.status_base), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.put('/status_base/<character_id>')
async def put_character_status_base(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterStatusBase(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')
        value = request.form.get('value')

        if await character.exists_status_base():
            return jsonify({'result': await character.update_status_base(key=key, value=value)}), 200
        else:
            return jsonify({'result': await character.insert_status_base(key=key, value=value)}), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/pericias/<character_id>')
async def get_character_skills(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_attributes():
            await character.load_attributes()
            await character.load_skills()
        return jsonify(character.skill)
    except Exception as e:
        print(e)
        return 404

@app.post('/pericias/<character_id>')
async def post_character_skill(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')

        skill = Skill(skill_name=key)

        if await skill.load_skill_by_name() and await character.load_attributes():
            return jsonify({'result': await character.insert_skill(id_skill=skill.id_skill),
                'data': {
                    key: await character.get_skills(key=key)
                }
            }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.delete('/pericias/<character_id>')
async def delete_character_skill(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')

        skill = Skill(skill_name=key)

        if await skill.load_skill_by_name() and await character.load_attributes():
            if await character.exists_skill(id_pericia=skill.id_skill):
                return jsonify({'result': await character.delete_skills(id_skill=skill.id_skill),
                    'data': {
                    key: await character.get_skills(key=key)
                    }
                }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/spell/<character_id>')
async def get_character_spells(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSpell(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_spell() and await character.load_spells():
            return jsonify({'result': True,
                'data': character.spells
            }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.post('/spell/<character_id>')
async def post_character_spell(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSpell(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()
        
        spell_id = request.form.get('id_habilidade')
        
        return jsonify({'result': await character.insert_spell(spell_id=spell_id)}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/spell/<character_id>')
async def delete_character_spell(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSpell(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()
        
        spell_id = request.form.get('id_habilidade')
        
        if await character.exists_specific_spell(spell_id=spell_id):
            return jsonify({'result': await character.delete_spell(character_id_spell=spell_id)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return jsonify({'result': False}), 500

@app.get('/equipamentos/<character_id>')
async def get_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterEquipment(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_equipment() and await character.load_equipments():
            return jsonify(character.list_equipments), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.post('/equipamentos/<character_id>')
async def post_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        id_equipment = request.form.get('id_equipamento')
        amount = request.form.get('qtd')
        character = CharacterEquipment(amount=amount, id_equipment=id_equipment, user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        return jsonify({'result': await character.insert_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.put('/equipamentos/<character_id>')
async def put_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        id_equipment = request.form.get('id_equipamento')
        amount = request.form.get('qtd')
        character = CharacterEquipment(amount=amount, id_equipment=id_equipment, user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        return jsonify({'result': await character.update_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/equipamentos/<character_id>')
async def delete_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        id_equipment = request.form.get('id_equipamento')
        character = CharacterEquipment(id_equipment=id_equipment, user_id=user_id, character_id=character_id)

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
        id_usuario = session.get('user_id')
        id_equipamento = request.form.get('id_equipamento')
        personagem = PersonagemEquipamento(id_equipamento=id_equipamento,id_usuario=id_usuario, id_personagem=id_personagem)
        equipamento = Equipamento(id_equipamento=id_equipamento)
        
        await personagem.personagem_pertence_usuario()
        await equipamento.carregar_equipamento()
        personagem.value = equipamento.preco
        #personagem.
        await personagem.gasto_moeda()
                    
        return jsonify({'result': await personagem.adicionar_equipamento_banco()}), 200
    except Exception as e:
        print(e)
        return 404"""
