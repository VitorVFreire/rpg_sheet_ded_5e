from flask import request, redirect, session, jsonify, url_for
from flask_session import Session
import asyncio

from main import app
from src import User, Skill, Race, Classe, SavingThrow, Spell, Room, Image, Equipment
from src import Character, CharacterAttribute, CharacterCharacteristics, CharacterSpell, CharacterCoin
from src import CharacterSkills, CharacterSavingThrow, CharacterStatusBase, CharacterEquipment

@app.get('/characters')
async def get_characters():
    try:
        user_id = session.get('user_id')
        character = Character(user_id=user_id)

        if await character.load_characters():
            return jsonify({'result': True,'data': character.characters}), 200
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
            return jsonify({'result': True,'data': character.character}), 200
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
            return jsonify({'result': True, 'data': character.characteristic}), 200
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

        if await character.exists_attributes() is False:
            return jsonify({'result': True, 'data': None}), 200
        elif await character.load_attributes():
            return jsonify({'result': True,'data': character.attributes})
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        return 404

@app.put('/attributes/<character_id>')
async def put_character_attribute(character_id):
    try:        
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)
        
        await character.character_belongs_user()

        key = request.form.get('key')
        value = request.form.get('value', default=0, type=int)

        result = {
            'result': False,
            'data': {}
        }
        
        if await character.exists_attributes():
            result['result'] = await character.update_attributes(key=key, value=value)
        else:
            result['result'] = await character.insert_attribute(key=key, value=value)
        
        if key != 'proficiency_bonus':
            await character.load_skills_attributes(usage_status=key)
            getattr(character, f'set_{key}')(value)
            
            result['data'] = {
                f'{key}_bonus': await character.get_bonus(key=key),
                f'{key}_resistance': await character.get_saving_throws(key=f'{key}_resistance'),                
            }
        else:
            await character.load_attribute_skills_saving_throw()
            
            for saving_throw in character.saving_throw_name_list:
                saving_throw_value = getattr(character, saving_throw)
                result['data'][saving_throw] = saving_throw_value
                        
        for skill in character.skills:
            skill_value = getattr(character, skill['skill_name'])
            result['data'][skill['skill_name']] = skill_value
            
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/saving_throws/<character_id>')
async def get_character_saving_throw(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSavingThrow(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_attributes() is False:
            return jsonify({'result': True, 'data': None}), 200
        elif await character.load_attributes() and await character.load_saving_throws():
            return jsonify({'result': True,'data': character.saving_throws}), 200
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        return 404

@app.post('/saving_throws/<character_id>')
async def post_character_saving_throw(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSavingThrow(user_id=user_id, character_id=character_id)

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
        character = CharacterSavingThrow(user_id=user_id, character_id=character_id)

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
        if await character.exists_status_base() is False:
            return jsonify({'result': True, 'data': None}), 200
        elif await character.load_status_base():
            return jsonify({'result': True,'data': character.status_base}), 200
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

@app.get('/skills/<character_id>')
async def get_character_skills(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_attributes():
            await character.load_attributes()
            await character.load_skills()
            return jsonify({'result': True, 'data': character.skill})
        return jsonify({'result': False})
    except Exception as e:
        print(e)
        return 404

@app.post('/skills/<character_id>')
async def post_character_skill(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')

        skill = Skill(skill_name=key)

        if await skill.load_skill_by_name() and await character.load_attributes():
            return jsonify({'result': await character.insert_skill(skill_id=skill.skill_id),
                'data': {
                    key: await character.get_skills(key=key)
                }
            }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.delete('/skills/<character_id>')
async def delete_character_skill(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSkills(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        key = request.form.get('key')

        skill = Skill(skill_name=key)

        if await skill.load_skill_by_name() and await character.exists_skill(skill_id=skill.skill_id):
            if await character.load_attributes():
                return jsonify({'result': await character.delete_skills(skill_id=skill.skill_id),
                    'data': {
                    key: await character.get_skills(key=key)
                    }
                }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/spell/<character_id>')
async def get_character_spell(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterSpell(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_spell() is False:
            return jsonify({'result': True,
                'data': None
            }), 200
        elif await character.load_spells():
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
                
        spell_id = request.form.get('key')
        
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
        
        spell_id = request.form.get('key')

        if await character.exists_specific_spell(spell_id=spell_id):
            return jsonify({'result': await character.delete_spell(character_id_spell=spell_id)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return jsonify({'result': False}), 500

@app.get('/equipments/<character_id>')
async def get_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterEquipment(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_equipment() is False:
            return jsonify({'result': True, 'data': None}), 200, 200
        elif await character.load_equipments():
            return jsonify({'result': True, 'data': character.list_equipments}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.post('/equipments/<character_id>')
async def post_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        equipment_id = request.form.get('key')
        amount = request.form.get('amount', default=1)
        character = CharacterEquipment(amount=amount, equipment_id = equipment_id, user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        return jsonify({'result': await character.insert_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.put('/equipments/<character_id>')
async def put_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        equipment_id = request.form.get('key')
        amount = request.form.get('value')
        
        print(request.form)
        
        character = CharacterEquipment(amount=amount, equipment_id=equipment_id, user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        return jsonify({'result': await character.update_equipment()}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/equipments/<character_id>')
async def delete_character_equipment(character_id):
    try:
        user_id = session.get('user_id')
        equipment_id = request.form.get('key')
        character = CharacterEquipment(equipment_id=equipment_id, user_id=user_id, character_id=character_id)

        await character.character_belongs_user()

        if await character.exists_specific_equipment():
            return jsonify({'result': await character.delete_equipment()}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/coins/<character_id>')
async def get_character_coin(character_id):
    try:
        user_id = session.get('user_id')
        character = CharacterCoin(user_id=user_id, character_id=character_id)

        await character.character_belongs_user()
        
        if await character.load_character_coins():
            return jsonify({'result': True, 'data': character.coins}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.put('/coins/<character_id>')
async def put_character_coin(character_id):
    try:
        user_id = session.get('user_id')
        coin_id = request.form.get('key')
        amount_coin = request.form.get('value')
                
        character = CharacterCoin(user_id=user_id, character_id=character_id, coin_id=coin_id, amount_coin=amount_coin)

        await character.character_belongs_user()

        if await character.character_has_this_coin():
            return jsonify({'result': await character.update_character_coin()}), 200
        return jsonify({'result': await character.insert_character_coin()}), 200
    except Exception as e:
        print(e)
        return 404