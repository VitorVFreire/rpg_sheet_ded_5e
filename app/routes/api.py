from flask import Flask, request, session, flash, jsonify
from flask_session import Session
import asyncio

from main import app
from src import Usuario, Pericia, Raca, Classe, Salvaguarda
from src import Personagem, PersonagemAtributos, PersonagemCaracteristicas, PersonagemHabilidades
from src import PersonagemPericias, PersonagemSalvaguardas, PersonagemStatusBase

@app.route('/insert_personagem',methods=['POST'])
async def insert_personagem():
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario)
        
        id_raca = request.form.get('id_raca')
        nome_personagem = request.form.get('nome_personagem')
                
        return jsonify({'result': await personagem.adicionar_personagem_banco(id_raca,nome_personagem)})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/caracteristicas/<id_personagem>', methods=['POST', 'GET'])
async def caracteristicas_db(id_personagem):
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
                'imagem_personagem': personagem.imagem_personagem
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False}) 

@app.route('/atributos/<id_personagem>',methods=['POST','GET'])
async def atributos_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemAtributos(id_usuario=id_usuario, id_personagem=id_personagem)        
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_atributos_do_banco():
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
                'bonus_proficiencia': personagem.bonus_proficiencia
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False}) 
    
@app.route('/salvaguardas/<id_personagem>', methods=['POST','GET'])
async def salvaguardas_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemSalvaguardas(id_usuario=id_usuario, id_personagem=id_personagem)  
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_atributos_do_banco() and await personagem.carregar_salvaguardas_do_banco():
            return jsonify({
                'forca': personagem.resistencia_forca,
                'destreza': personagem.resistencia_destreza,
                'inteligencia': personagem.resistencia_inteligencia,
                'constituicao': personagem.resistencia_constituicao,
                'sabedoria': personagem.resistencia_sabedoria,
                'carisma': personagem.resistencia_carisma,
                'salvaguardas': personagem.lista_nome_salvaguardas
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False})
    
@app.route('/status_base/<id_personagem>', methods=['POST', 'GET'])
async def status_base_db(id_personagem):
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
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False})

@app.route('/pericias/<id_personagem>',methods=['POST','GET'])
async def pericias_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_atributos_do_banco() and await personagem.carregar_pericias_do_banco():
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
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False})
    
@app.route('/valores/pericias/<id_personagem>',methods=['POST','GET'])
async def novo_pericias_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_atributos_do_banco() and await personagem.carregar_pericias_do_banco():
            return jsonify({
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
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False})

@app.route('/update/atributos/<id_personagem>',methods=['POST'])
async def update_atributos_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemAtributos(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
        
        if await personagem.exists_atributos_banco() and chave != 'bonus_proficiencia':
            return jsonify({'result': await personagem.update_atributos_banco(chave=chave, valor=valor),
                'bonus': int(await personagem.get_bonus(chave=chave)),'resistencia':int(await personagem.get_bonus(chave=chave))})
        elif await personagem.exists_atributos_banco():
            return jsonify({'result': await personagem.update_atributos_banco(chave=chave, valor=valor)})
        
        return jsonify({'result': await personagem.adicionar_atributo_banco(chave=chave,valor=valor),
                        'bonus':int(await personagem.get_bonus(chave=chave)),'resistencia':int(await personagem.get_bonus(chave=chave))})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/salvaguarda/<id_personagem>',methods=['POST'])
async def update_salvaguardas_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemSalvaguardas(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()        
        
        chave = request.form.get('chave')
        tipo = request.form.get('tipo')
        
        salvaguarda = Salvaguarda(nome_salvaguarda=chave)
        
        await salvaguarda.carregar_salvaguarda_nome()
        await personagem.carregar_atributos_do_banco()
        
        if await personagem.exists_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda) and tipo=='remover':
            return jsonify({'result': await personagem.delete_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                            'resistencia':int(await personagem.get_salvaguardas(chave))})
        elif tipo=='adicionar':
            return jsonify({'result': await personagem.adicionar_salvaguardas_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                            'resistencia':int(await personagem.get_salvaguardas(chave))})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/status_base/<id_personagem>',methods=['POST'])
async def update_status_base_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemStatusBase(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
        
        if await personagem.exists_status_base_banco():
            return jsonify({'result': await personagem.update_status_base_banco(chave=chave, valor=valor)})
        else:
            return jsonify({'result': await personagem.adicionar_status_base_banco(chave=chave,valor=valor)})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})

@app.route('/update/nova_pericia/<id_personagem>',methods=['POST'])
async def update_adicionar_perica_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemPericias(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()        
        
        chave = request.form.get('chave')
        tipo = request.form.get('tipo')

        pericia = Pericia(nome_pericia=chave)
        
        await pericia.carregar_pericia_nome()
        await personagem.carregar_atributos_do_banco()

        if tipo == 'remover' and await personagem.exists_pericia_banco(id_pericia=pericia.id_pericia):
            return jsonify({'result': await personagem.delete_pericias_banco(id_pericia=pericia.id_pericia),
                            'pericia':int(await personagem.get_pericias(chave=chave,status_uso=pericia.status_uso))})
        elif tipo=='adicionar':
            return jsonify({'result': await personagem.adicionar_pericias_banco(id_pericia=pericia.id_pericia),
                            'pericia':int(await personagem.get_pericias(chave=chave,status_uso=pericia.status_uso))})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/caracteristicas_personagem/<id_personagem>',methods=['POST'])
async def update_caracteristicas_personagems_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemCaracteristicas(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()       
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
                
        if await personagem.exists_caracteristicas_banco():
            return jsonify({'result': await personagem.update_caracteristicas_banco(chave=chave,valor=valor)})
        else:
            return jsonify({'result': await personagem.adicionar_caracteristicas_banco(chave=chave,valor=valor)})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/base/<id_personagem>',methods=['POST'])
async def update_base_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
                
        return jsonify({'result': await personagem.update_personagem_banco(chave=chave,valor=valor)})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})