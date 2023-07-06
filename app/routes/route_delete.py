from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session

from main import app
from src import Usuario, Personagem

@app.route('/delete/usuario',methods=['POST'])
def delete_usuario():
    try:
        id_usuario=session.get('id_usuario')
        usuario=Usuario(id_usuario=id_usuario)
                
        usuario.delete_usuario(id_classe)
        
        return render_template('index.html',titulo='home',msg='Conta Encerrada!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão da conta!')
    
@app.route('/delete/classe',methods=['POST'])
def delete_classe():
    try:
        id_usuario=session.get('id_usuario')
        id_classe_personagem=request.form.get('id_classe_personagem')
        
        personagem=Personagem(id_usuario=id_usuario)
                
        personagem.delete_classe_banco(id_classe_personagem)
        
        return render_template('index.html',titulo='home',msg='Classe Apagada!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão da classe!')
    
@app.route('/delete/status_base',methods=['POST'])
def delete_status_base():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
                
        personagem.delete_status_base_banco()
        
        return render_template('index.html',titulo='home',msg='Status Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão dos status!')
    
@app.route('/delete/feitico',methods=['POST'])
def delete_feitico():
    try:
        id_usuario=session.get('id_usuario')
        id_feitico_personagem=request.form.get('id_feitico_personagem')
        
        personagem=Personagem(id_usuario=id_usuario)
                
        personagem.delete_feitico_banco(id_feitico_personagem)
        
        return render_template('index.html',titulo='home',msg='Feitiço Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão do feitiço!')
    
@app.route('/delete/atributos',methods=['POST'])
def delete_atributos():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
                
        personagem.delete_atributos_banco()
        
        return render_template('index.html',titulo='home',msg='Atributos Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão dos atributos!')
    
@app.route('/delete/caracteristicas',methods=['POST'])
def delete_caracteristicas():
    try:
        id_usuario=session.get('id_usuario')
        id_personagem=request.form.get('id_personagem')
        
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
                
        personagem.delete_caracteristicas_banco()
        
        return render_template('index.html',titulo='home',msg='caracteristicas Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão dos caracteristicas!')
    
@app.route('/delete/salvaguarda',methods=['POST'])
def delete_salvaguarda():
    try:
        id_usuario=session.get('id_usuario')
        id_salvaguarda_personagem=request.form.get('id_salvaguarda_personagem')
        
        personagem=Personagem(id_usuario=id_usuario)
                
        personagem.delete_salvaguarda_banco(id_salvaguarda_personagem)
        
        return render_template('index.html',titulo='home',msg='Salvaguada Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão do salvaguarda!')
    
@app.route('/delete/pericia',methods=['POST'])
def delete_pericia():
    try:
        id_usuario=session.get('id_usuario')
        id_pericia_personagem=request.form.get('id_pericia_personagem')
        
        personagem=Personagem(id_usuario=id_usuario)
                
        personagem.delete_pericias_banco(id_pericia_personagem)
        
        return render_template('index.html',titulo='home',msg='Pericia Apagado!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão da pericia!')