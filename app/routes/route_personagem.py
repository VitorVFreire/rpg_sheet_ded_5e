from flask import request, redirect, session, jsonify, send_from_directory, send_file
from flask_session import Session
import asyncio
import pathlib 

from main import app
from tools import img_reserva
from src import Usuario, Pericia, Raca, Classe, Salvaguarda, Habilidade, Room
from src import Personagem, PersonagemAtributos, PersonagemCaracteristicas, PersonagemHabilidades
from src import PersonagemPericias, PersonagemSalvaguardas, PersonagemStatusBase

@app.post('/insert_personagem')
async def insert_personagem():
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario)
        
        id_raca = request.form.get('id_raca')
        id_classe = request.form.get('id_classe')
        nome_personagem = request.form.get('nome_personagem')
        
        return jsonify({'result': (
            await personagem.adicionar_personagem_banco(id_raca=id_raca,nome_personagem=nome_personagem) 
            and 
            await personagem.adicionar_classe_banco(id_classe=id_classe)
            ), 
            'id_personagem': personagem.id_personagem}), 200     
    except Exception as e:
        print(e)
        return 404
    
@app.delete('/personagem/<id_personagem>')
async def deletepersonagem(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                
        return jsonify({'result': await personagem.delete_personagem_banco()}), 200
    except Exception as e:
        print(e)
        return 404
    
@app.get('/caracteristicas/<id_personagem>')
async def caracteristicas_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemCaracteristicas(id_usuario=id_usuario, id_personagem=id_personagem)
            
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_caracteristicas_do_banco():
            return jsonify({
                'idade': personagem.idade,
                'altura': personagem.altura,
                'peso': personagem.peso,
                'cor_dos_olhos': personagem.cor_olhos,
                'cor_da_pele': personagem.cor_pele,
                'cor_do_cabelo': personagem.cor_cabelo,
                'imagem_personagem': personagem.url_img
            }), 200
        return jsonify({'result': False}), 404            
    except Exception as e:
        print(e)
        return 404 

@app.put('/caracteristicas/<id_personagem>')
async def caracteristicas_personagem_put(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemCaracteristicas(id_usuario=id_usuario, id_personagem=id_personagem)
            
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')

        if request.files:
            file_upload = request.files.get('img_personagem')
            return jsonify({'result': await personagem.save_file(file=file_upload), 'img_personagem': personagem.url_img}), 200 

        if await personagem.exists_caracteristicas_banco():
            return jsonify({'result': await personagem.update_caracteristicas_banco(chave=chave,valor=valor)}), 200
        else:               
            return jsonify({'result': await personagem.adicionar_caracteristicas_banco(chave=chave,valor=valor)}), 200
    except Exception as e:
        print(e)
        return 404  
    
@app.get('/openimg/<img>')
def open_img(img): 
    try:  
        directory=pathlib.Path('data/img')
        arquivo = list(directory.glob(img))
        file = arquivo[0] if arquivo[0] is not None else img_reserva()
        return send_file(file)   
    except Exception as e:
        print(e)
        return send_file(img_reserva()) 

@app.get('/atributos/<id_personagem>')
async def atributos_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemAtributos(id_usuario=id_usuario, id_personagem=id_personagem)   
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.exists_atributos_banco() and await personagem.carregar_atributos_do_banco():
            return jsonify({
                'forca': personagem.forca,
                'bonus_forca': personagem.bonus_forca,
                'destreza': personagem.destreza,
                'bonus_destreza': personagem.bonus_destreza,
                'inteligencia': personagem.inteligencia,
                'bonus_inteligencia': personagem.bonus_inteligencia,
                'constituicao': personagem.constituicao,
                'bonus_constituicao': personagem.bonus_constituicao,
                'sabedoria': personagem.sabedoria,
                'bonus_sabedoria': personagem.bonus_sabedoria,
                'carisma': personagem.carisma,
                'bonus_carisma': personagem.bonus_carisma,
                'bonus_proficiencia': personagem.bonus_proficiencia_externa}), 200  
        else:
            return jsonify({
                'forca': None,
                'bonus_forca': None,
                'destreza': None,
                'bonus_destreza': None,
                'inteligencia': None,
                'bonus_inteligencia': None,
                'constituicao': None,
                'bonus_constituicao': None,
                'sabedoria': None,
                'bonus_sabedoria': None,
                'carisma': None,
                'bonus_carisma': None,
                'bonus_proficiencia': None
            }), 200 
    except Exception as e:
        print(e)
        return 404
    
@app.put('/atributos/<id_personagem>')
async def atributos_personagem_put(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemAtributos(id_usuario=id_usuario, id_personagem=id_personagem)   
                
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')

        if await personagem.exists_atributos_banco() and chave != 'bonus_proficiencia':
            resultado_update = await personagem.update_atributos_banco(chave=chave, valor=valor)
            bonus_valor_update = await personagem.get_bonus(chave=chave)
            return jsonify({'result': resultado_update,
                'bonus': bonus_valor_update,
                'resistencia': bonus_valor_update}), 200
        elif await personagem.exists_atributos_banco():
            return jsonify({'result': await personagem.update_atributos_banco(chave=chave, valor=valor)}), 200
            
        resultado_adicao = await personagem.adicionar_atributo_banco(chave=chave,valor=valor)
        bonus_valor_adicao = await personagem.get_bonus(chave=chave)
        return jsonify({'result': resultado_adicao,
                        'bonus': bonus_valor_adicao,
                        'resistencia': bonus_valor_adicao}), 200
    except Exception as e:
        print(e)
        return 404

@app.get('/salvaguardas/<id_personagem>')
async def salvaguardas_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemSalvaguardas(id_usuario=id_usuario, id_personagem=id_personagem)  
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.exists_atributos_banco() and await personagem.carregar_atributos_do_banco() and await personagem.carregar_salvaguardas_do_banco():
            return jsonify({
                'forca': personagem.resistencia_forca,
                'destreza': personagem.resistencia_destreza,
                'inteligencia': personagem.resistencia_inteligencia,
                'constituicao': personagem.resistencia_constituicao,
                'sabedoria': personagem.resistencia_sabedoria,
                'carisma': personagem.resistencia_carisma,
                'salvaguardas': personagem.lista_nome_salvaguardas
            }), 200
        else:
            return jsonify({
                'forca': None,
                'destreza': None,
                'inteligencia': None,
                'constituicao': None,
                'sabedoria': None,
                'carisma': None,
                'salvaguardas': None
            }), 200
    except Exception as e:
        print(e)
        return 404

@app.post('/salvaguardas/<id_personagem>')
async def salvaguardas_personagem_post(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemSalvaguardas(id_usuario=id_usuario, id_personagem=id_personagem)  
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
            
        salvaguarda = Salvaguarda(nome_salvaguarda=chave)
            
        if await salvaguarda.carregar_salvaguarda_nome() and await personagem.carregar_atributos_do_banco():
            return jsonify({'result': await personagem.adicionar_salvaguardas_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                            'resistencia': await personagem.get_salvaguardas(chave)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404  
    
@app.delete('/salvaguardas/<id_personagem>')
async def salvaguardas_personagem(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemSalvaguardas(id_usuario=id_usuario, id_personagem=id_personagem)  
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        salvaguarda = Salvaguarda(nome_salvaguarda=chave)
            
        if await salvaguarda.carregar_salvaguarda_nome() and await personagem.carregar_atributos_do_banco():
            if await personagem.exists_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda):
                return jsonify({'result': await personagem.delete_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                                'resistencia': await personagem.get_salvaguardas(chave)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/status_base/<id_personagem>')
async def status_base_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemStatusBase(id_usuario=id_usuario, id_personagem=id_personagem)          

        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_status_base_do_banco():
            return jsonify({
                'nivel': personagem.nivel,
                'alinhamento': personagem.alinhamento,
                'faccao': personagem.faccao,
                'antecendente': personagem.antecendente,
                'xp': personagem.xp,
                'deslocamento': personagem.deslocamento,
                'iniciativa': personagem.iniciativa,
                'vida': personagem.vida,
                'vida_atual': personagem.vida_atual,
                'vida_temporaria': personagem.vida_temporaria,
                'inspiracao': personagem.inspiracao,
                'ca': personagem.ca
            }), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
   
@app.put('/status_base/<id_personagem>')
async def status_base_personagem_put(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemStatusBase(id_usuario=id_usuario, id_personagem=id_personagem)          
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
            
        if await personagem.exists_status_base_banco():
            return jsonify({'result': await personagem.update_status_base_banco(chave=chave, valor=valor)}), 200
        else:
            return jsonify({'result': await personagem.adicionar_status_base_banco(chave=chave,valor=valor)}),200
    except Exception as e:
        print(e)
        return 404

@app.get('/pericias/<id_personagem>')
async def pericias_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.exists_atributos_banco() and await personagem.carregar_atributos_do_banco() and await personagem.carregar_pericias_do_banco():
            return jsonify({
                'pericias': {
                    'acrobacia': personagem.acrobacia,
                    'arcanismo': personagem.arcanismo,
                    'atletismo': personagem.atletismo,
                    'atuacao': personagem.atuacao,
                    'enganacao': personagem.enganacao,
                    'furtividade': personagem.furtividade,
                    'historia': personagem.historia,
                    'intimidacao': personagem.intimidacao,
                    'investigacao': personagem.investigacao,
                    'lidar_com_animais': personagem.lidar_com_animais,
                    'medicina': personagem.medicina,
                    'natureza': personagem.natureza,
                    'percepcao': personagem.percepcao,
                    'persuasao': personagem.persuasao,
                    'prestidigitacao': personagem.prestidigitacao,
                    'religiao': personagem.religiao,
                    'sobrevivencia': personagem.sobrevivencia
                },                
                'pericias_do_personagem': personagem.lista_nome_pericias
            }), 200
        else:
            return jsonify({
                'pericias': {
                    'acrobacia': '',
                    'arcanismo': '',
                    'atletismo': '',
                    'atuacao': '',
                    'enganacao': '',
                    'furtividade': '',
                    'historia': '',
                    'intimidacao': '',
                    'investigacao': '',
                    'lidar_com_animais': '',
                    'medicina': '',
                    'natureza': '',
                    'percepcao': '',
                    'persuasao': '',
                    'prestidigitacao': '',
                    'religiao': '',
                    'sobrevivencia': ''
                },                
                'pericias_do_personagem': ''
            }), 200
    except Exception as e:
        print(e)
        return 404

@app.post('/pericias/<id_personagem>')
async def pericias_personagem_post(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')

        pericia = Pericia(nome_pericia=chave)
            
        if await pericia.carregar_pericia_nome() and await personagem.carregar_atributos_do_banco():
            return jsonify({'result': await personagem.adicionar_pericias_banco(id_pericia=pericia.id_pericia),
                            'pericia': await personagem.get_pericias(chave=chave,status_uso=pericia.status_uso)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.delete('/pericias/<id_personagem>')
async def pericias_personagem_delete(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')

        pericia = Pericia(nome_pericia=chave)
            
        if await pericia.carregar_pericia_nome() and await personagem.carregar_atributos_do_banco():
            if await personagem.exists_pericia_banco(id_pericia=pericia.id_pericia):
                 return jsonify({'result': await personagem.delete_pericias_banco(id_pericia=pericia.id_pericia),
                                'pericia': await personagem.get_pericias(chave=chave,status_uso=pericia.status_uso)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404

@app.get('/habilidades/<id_personagem>')
async def habilidades_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemHabilidades(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                
        if await personagem.exists_habilidade_banco() and await personagem.carregar_habilidades_do_banco():
            return jsonify(personagem.habilidades), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
@app.post('/habilidades/<id_personagem>')
async def habilidades_personagem_post(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemHabilidades(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        id_habilidade = request.form.get('id_habilidade')
            
        return jsonify({'result': await personagem.adicionar_habilidade_banco(id_habilidade=id_habilidade)}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/habilidades/<id_personagem>')
async def habilidades_personagem_delete(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemHabilidades(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        id_habilidade = request.form.get('id_habilidade')
            
        if await personagem.exists_habilidade_especifica_banco(id_habilidade=id_habilidade):
            return jsonify({'result': await personagem.delete_habilidade_banco(id_habilidade_personagem=id_habilidade)}), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
        
@app.put('/update/base/<id_personagem>')
async def update_base_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
                
        return jsonify({'result': await personagem.update_personagem_banco(chave=chave,valor=valor)}), 200
    except Exception as e:
        print(e)
        return 404, "Error"
    
@app.post('/insert/room/<id_personagem>/<code_room>')
async def room_personagem_post(id_personagem, code_room):
    try:
        room = Room(id_room=code_room ,id_personagem=id_personagem)

        return jsonify({'result': room.insert_character_room_bank()}), 200
    except Exception as e:
        print(e)
        return 404