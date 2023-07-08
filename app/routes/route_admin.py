from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session

from main import app
from src import Usuario, Personagem, Classe, Raca

@app.route('/criar_classe')
def nova_classe():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_classe.html',titulo='Nova Classe')
    return redirect(url_for('index'))
    
@app.route('/insert_classe',methods=['POST'])
def insert_classe():
    try:
        classe=Classe(nome_classe=request.form.get('nome_classe'))
        return jsonify({'result':classe.insert_classe_banco()})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_raca')
def nova_raca():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_raca.html',titulo='Nova raca')
    return redirect(url_for('index'))
    
@app.route('/insert_raca',methods=['POST'])
def insert_raca():
    try:
        nome_raca=request.form.get('nome_raca')
        raca=Raca(nome_raca=nome_raca)
        return jsonify({'result':raca.insert_raca_banco()})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})