from flask import request, redirect, session, jsonify
from flask_session import Session
import asyncio

from main import app
from src import Usuario, Pericia, Raca, Classe, Salvaguarda, Habilidade, Room, Image, Equipamento
from src import Personagem, PersonagemAtributos, PersonagemCaracteristicas, PersonagemHabilidades
from src import PersonagemPericias, PersonagemSalvaguardas, PersonagemStatusBase, PersonagemEquipamento

@app.post('/personagem')
async def personagem_post():
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

@app.put('/personagem/<id_personagem>')
async def personagem_put(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
        
        chave = request.form.get('chave')
        valor = request.form.get('valor')
                
        return jsonify({'result': await personagem.update_personagem_banco(chave=chave,valor=valor)}), 200
    except Exception as e:
        print(e)
        return 404
    
@app.delete('/personagem/<id_personagem>')
async def personagem_delete(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemCaracteristicas(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                
        return jsonify({'result': (await personagem.delete_caracteristicas_banco() and await personagem.delete_personagem_banco())}), 200
    except Exception as e:
        print(e)
        return 404
    
@app.get('/caracteristicas/<id_personagem>')
async def caracteristicas_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemCaracteristicas(id_personagem=id_personagem,id_usuario=id_usuario)
            
        await personagem.personagem_pertence_usuario()
        
        if await personagem.carregar_caracteristicas_do_banco():
            return jsonify(personagem.caracteristica), 200
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
            return jsonify({'result': await personagem.save_img_personagem(file=file_upload), 'img_personagem': personagem.url_img}), 200 

        if await personagem.exists_caracteristicas_banco():
            return jsonify({'result': await personagem.update_caracteristicas_banco(chave=chave,valor=valor)}), 200
        else:               
            return jsonify({'result': await personagem.adicionar_caracteristicas_banco(chave=chave,valor=valor)}), 200
    except Exception as e:
        print(e)
        return 404  

@app.get('/atributos/<id_personagem>')
async def atributos_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemAtributos(id_usuario=id_usuario, id_personagem=id_personagem)   
        
        await personagem.personagem_pertence_usuario()
        
        if await personagem.exists_atributos_banco():
            await personagem.carregar_atributos_do_banco()
        
        return jsonify(personagem.atributos)              
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
        
        if await personagem.exists_atributos_banco():
            await personagem.carregar_atributos_do_banco()
            await personagem.carregar_salvaguardas_do_banco()
        
        return jsonify(personagem.salvaguardas)        
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
            return jsonify(personagem.status_base), 200
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
        
        if await personagem.exists_atributos_banco():
            await personagem.carregar_atributos_do_banco()
            await personagem.carregar_pericias_do_banco()
        return jsonify(personagem.pericia)
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
                            'pericia': await personagem.get_pericias(chave=chave)}), 200
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
                                'pericia': await personagem.get_pericias(chave=chave)}), 200
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
    
@app.get('/equipamentos/<id_personagem>')
async def equipamentos_personagem_get(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = PersonagemEquipamento(id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                
        if await personagem.exists_equipamento_banco() and await personagem.carregar_equipamentos_do_banco():
            return jsonify(personagem.equipamentos_lista), 200
        return jsonify({'result': False}), 404
    except Exception as e:
        print(e)
        return 404
    
@app.post('/equipamentos/<id_personagem>')
async def equipamentos_personagem_post(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        id_equipamento = request.form.get('id_equipamento')
        qtd = request.form.get('qtd')
        personagem = PersonagemEquipamento(qtd=qtd,id_equipamento=id_equipamento,id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                    
        return jsonify({'result': await personagem.adicionar_equipamento_banco()}), 200
    except Exception as e:
        print(e)
        return 404

@app.put('/equipamentos/<id_personagem>')
async def equipamentos_personagem_put(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        id_equipamento = request.form.get('id_equipamento')
        qtd = request.form.get('qtd')
        personagem = PersonagemEquipamento(qtd=qtd,id_equipamento=id_equipamento,id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
                    
        return jsonify({'result': await personagem.update_equipamento_banco()}), 200
    except Exception as e:
        print(e)
        return 404

@app.delete('/equipamentos/<id_personagem>')
async def equipamentos_personagem_delete(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        id_equipamento = request.form.get('id_equipamento')
        personagem = PersonagemEquipamento(id_equipamento=id_equipamento,id_usuario=id_usuario, id_personagem=id_personagem)
        
        await personagem.personagem_pertence_usuario()
            
        if await personagem.exists_equipamento_especifica_banco():
            return jsonify({'result': await personagem.delete_equipamento_banco()}), 200
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