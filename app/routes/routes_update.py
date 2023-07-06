from flask import Flask, request, session, jsonify
from flask_session import Session

from main import app
from src import Usuario, Personagem

@app.route('/update/nome_personagem',methods=['POST'])
def update_nome_personagem():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        nome_personagem=request.form.get('nome_personagem')
        personagem.update_personagem_banco(chave='nome_personagem',valor=nome_personagem)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/raca',methods=['POST'])
def update_raca():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        id_raca=request.form.get('id_raca')
        personagem.update_personagem_banco(chave='id_raca',valor=id_raca)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
        
@app.route('/update/classe',methods=['POST'])
def update_classe():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        id_classe=request.form.get('id_classe')
        id_classe_personagem=request.form.get('id_classe_personagem')
        personagem.update_classe_banco(id_classe,id_classe_personagem)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})

@app.route('/update/base',methods=['POST'])
def update_base():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        personagem.update_status_base_banco(chave=chave,valor=valor)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/feitico',methods=['POST'])
def update_feitico():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        id_feitico=request.form.get('id_feitico')
        id_feitico_personagem=request.form.get('id_feitico_personagem')
        personagem.update_feitico_banco(id_feitico,id_feitico_personagem)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})

@app.route('/update/atributos',methods=['POST'])
def update_atributos():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        personagem.update_atributos_banco(chave=chave,valor=valor)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/caracteristicas',methods=['POST'])
def update_caracteristicas():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        personagem.update_caracteristicas_banco(chave=chave,valor=valor)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/salvaguardas',methods=['POST'])
def update_salvaguardas():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        id_salvaguardas=request.form.get('id_salvaguardas')
        id_salvaguardas_personagem=request.form.get('id_salvaguardas_personagem')
        personagem.update_salvaguardas_banco(id_salvaguardas,id_salvaguardas_personagem)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/update/pericias',methods=['POST'])
def update_pericias():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        id_pericias=request.form.get('id_pericias')
        id_pericias_personagem=request.form.get('id_pericias_personagem')
        personagem.update_pericias_banco(id_pericias,id_pericias_personagem)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})

@app.route('/update/usuario',methods=['POST'])
def update_usuario():
    try:
        id_usuario=session.get('id_usuario')
        usuario=Usuario(id=id_usuario)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        usuario.update_usuario(chave=chave,valor=valor)
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    