from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session

from app import app
from src import Usuario, Personagem

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('login.html',titulo='login',msg='Erro no Login')

@app.route('/logout')
def logout():
    session['id_usuario'] = None
    return render_template('index.html',titulo='home',msg='Logout')

@app.post('/login')
def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if usuario.valid_usuario():
        session['id_usuario']=usuario.id
        return render_template('index.html',titulo='home',msg='Logado')
    return redirect(url_for('login'))