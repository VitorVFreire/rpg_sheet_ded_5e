from flask import Flask, request, session, jsonify
from src import Usuario,Personagem

@app.route('/insert/classe_personagem',methods=['POST'])
def insert_classe_personagem():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        id_classe=request.form.get('id_classe')
        
        personagem.adicionar_classe_banco(id_classe)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/personagem',methods=['POST'])
def insert_personagem():
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario)
        
        id_raca=request.form.get('id_raca')
        nome_personagem=request.form.get('nome_personagem')
        
        personagem.adicionar_personagem_banco(id_raca,nome_personagem)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/status_base',methods=['POST'])
def insert_status_base():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        vida=request.form.get('vida')
        xp=request.form.get('xp')
        nivel=request.form.get('nivel')
        alinhamento=request.form.get('alinhamento')
        antecendente=request.form.get('antecendente')
        faccao=request.form.get('faccao')
        inspiracao=request.form.get('inspiracao')
        ca=request.form.get('ca')
        iniciativa=request.form.get('iniciativa')
        deslocamento=request.form.get('deslocamento')
        vida_atual=request.form.get('vida_atual')
        vida_temporaria=request.form.get('vida_temporaria')
        
        personagem.adicionar_status_base_banco(vida,xp,nivel,alinhamento,antecendente,faccao,inspiracao,ca,iniciativa,deslocamento,vida_atual,vida_temporaria)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/feitico_personagem',methods=['POST'])
def insert_feitico_personagem():
    try:
        id_usuario=session.get('id_usuario')        
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)

        id_feitico=request.form.get('id_feitico')

        personagem.adicionar_feitico_banco(id_feitico)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/atributos',methods=['POST'])
def insert_atributos():
    try:
        id_usuario=session.get('id_usuario')        
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)

        forca=request.form.get('forca')
        destreza=request.form.get('destreza')
        constituicao=request.form.get('constituicao')
        inteligencia=request.form.get('inteligencia')
        sabedoria=request.form.get('sabedoria')
        carisma=request.form.get('carisma')
        bonus_proficiencia=request.form.get('bonus_proficiencia')

        personagem.adicionar_atributos_banco(forca,destreza,constituicao,inteligencia,sabedoria,carisma,bonus_proficiencia)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/caracteristicas',methods=['POST'])
def insert_caracteristicas():
    try:
        id_usuario=session.get('id_usuario')        
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)

        idade=request.form.get('idade')
        cor_olhos=request.form.get('cor_olhos')
        cor_pele=request.form.get('cor_pele')
        cor_cabelo=request.form.get('cor_cabelo')
        peso=request.form.get('peso')
        altura=request.form.get('altura')
        imagem_personagem=request.form.get('imagem_personagem')

        personagem.adicionar_caracteristicas_banco(idade,cor_olhos,cor_pele,cor_cabelo,peso,altura,imagem_personagem)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/salvaguardas',methods=['POST'])
def insert_salvaguardas():
    try:
        id_usuario=session.get('id_usuario')        
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)

        id_salvaguarda=request.form.get('id_salvaguarda')

        personagem.adicionar_salvaguardas_banco(id_salvaguarda)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert/pericias',methods=['POST'])
def insert_pericias():
    try:
        id_usuario=session.get('id_usuario')        
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)

        id_pericia=request.form.get('id_pericia')

        personagem.adicionar_pericias_banco(id_pericia)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})