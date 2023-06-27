from flask import Flask, render_template, request,redirect, session, flash, url_for

from app import app
from src import Usuario

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    return render_template('login.html',titulo='login')

@app.post('/login')
def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if usuario.valid_usuario():
        return render_template('index.html',titulo='home',msg='logado')
    return redirect(url_for('login'))