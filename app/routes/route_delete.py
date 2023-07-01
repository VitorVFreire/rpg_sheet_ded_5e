from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session

from app import app
from src import Usuario, Personagem

@app.route('/delete/usuario',methods=['POST'])
def insert_delete_usuario():
    try:
        id_usuario=session.get('id_usuario')
        usuario=Usuario(id_usuario=id_usuario)
                
        usuario.delete_usuario(id_classe)
        
        return render_template('index.html',titulo='home',msg='Conta Encerrada!')
    except EOFError as e:
        print(e)
        return render_template('index.html',titulo='home',msg='Erro na Exclusão da conta!')