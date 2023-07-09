from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session

from main import app
from src import Usuario, Personagem, Classe

@app.route('/cadastro_usuario',methods=['POST'])
def cadastro_usuario():
    try:
        email=request.form.get('email')
        senha=request.form.get('senha')
        nome=request.form.get('nome')
        data_nascimento=request.form.get('data_nascimento')
        
        usuario=Usuario(nome=nome,email=email,senha=senha,data_nascimento=data_nascimento)
        
        if usuario.create_usuario():
            session['id_usuario']=usuario.id
            return render_template('index.html',titulo='home',msg='logado')
        return render_template('login.html',titulo='login',msg='Erro no Login')
    except EOFError as e:
        print(e)
        return jsonify({'result':False})

@app.route('/insert_classe_personagem',methods=['POST'])
def insert_classe_personagem():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        classe=request.form.getlist('classe')
        
        for id_classe in classe:
            personagem.adicionar_classe_banco(id_classe)
        
        return jsonify({'result':True})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/insert_personagem',methods=['POST'])
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
        
@app.route('/insert_feitico_personagem',methods=['POST'])
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
    
@app.route('/insert_caracteristicas',methods=['POST'])
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
    
@app.route('/insert_pericias',methods=['POST'])
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