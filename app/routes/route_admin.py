from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session

from main import app
from src import Usuario, Personagem, Classe, Raca, Pericia, Salvaguarda

@app.route('/admin')
def admin():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/admin_pag.html',titulo='ADMIN')
    return redirect(url_for('index'))

@app.route('/criar_classe')
def nova_classe():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_classe.html',titulo='Nova Classe')
    return redirect(url_for('index'))
    
@app.route('/criar_classe',methods=['POST'])
def insert_classe():
    try:
        usuario=Usuario(id=session.get('id_usuario'))
        if usuario.usuario_admin():
            classe=Classe(nome_classe=request.form.get('nome_classe'))
            return jsonify({'result':classe.insert_classe_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_raca')
def nova_raca():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_raca.html',titulo='Nova raca')
    return redirect(url_for('index'))
    
@app.route('/criar_raca',methods=['POST'])
def insert_raca():
    try:
        usuario=Usuario(id=session.get('id_usuario'))
        if usuario.usuario_admin():
            nome_raca=request.form.get('nome_raca')
            raca=Raca(nome_raca=nome_raca)
            return jsonify({'result':raca.insert_raca_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_pericia')
def nova_pericia():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_pericia.html',titulo='Nova pericia')
    return redirect(url_for('index'))
    
@app.route('/criar_pericia',methods=['POST'])
def insert_pericia():
    try:
        usuario=Usuario(id=session.get('id_usuario'))
        if usuario.usuario_admin():
            nome_pericia=request.form.get('nome_pericia')
            status_uso=request.form.get('status_uso',)
            pericia=Pericia(nome_pericia=nome_pericia,status_uso=status_uso)
            return jsonify({'result':pericia.insert_pericia_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_salvaguarda')
def nova_salvaguarda():
    usuario=Usuario(id=session.get('id_usuario'))
    if usuario.usuario_admin():
        return render_template('admin/add_salvaguarda.html',titulo='Nova salvaguarda')
    return redirect(url_for('index'))
    
@app.route('/criar_salvaguarda',methods=['POST'])
def insert_salvaguarda():
    try:
        usuario=Usuario(id=session.get('id_usuario'))
        if usuario.usuario_admin():
            nome_salvaguarda=request.form.get('nome_salvaguarda')
            salvaguarda=Salvaguarda(nome_salvaguarda=nome_salvaguarda)
            return jsonify({'result':salvaguarda.insert_salvaguarda_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})