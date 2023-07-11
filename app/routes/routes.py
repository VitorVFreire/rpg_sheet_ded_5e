from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session

from main import app
from src import Usuario, Personagem, Pericia, Raca, Classe, Salvaguarda

@app.route('/')
def index():
    return render_template('index.html',titulo='home')
    
@app.route('/login')
def login():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('login.html',titulo='login',msg='Erro no Login')

@app.post('/login')
def cadastro_login():
    usuario=Usuario(email=request.form.get('email'),senha=request.form.get('senha'))
    if usuario.valid_usuario():
        session['id_usuario']=usuario.id
        return render_template('index.html',titulo='home',msg='Logado')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['id_usuario'] = None
    return render_template('index.html',titulo='home',msg='Logout')

@app.route('/cadastro_usuario')
def criar_usuario():
    if session.get('id_usuario'):
        return render_template('index.html',titulo='home')
    return render_template('cadastro_usuario.html',titulo='cadastro de usuario')

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

@app.route('/criar_personagem')
def criar_personagem():
    racas=Raca()
    return render_template('create_personagem.html',titulo='Criar Personagem',racas=racas.racas)
    
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

@app.route('/personagens')
def personagens():
    usuario=Usuario(id=session.get('id_usuario'))
    return render_template('personagens.html',titulo='Personagens',personagens=usuario.personagens)

@app.route('/personagem/<id_personagem>')
def personagem(id_personagem):
    personagem=Personagem(id_usuario=session.get('id_usuario'),id_personagem=id_personagem)
    classe=Classe()
    personagem.carregar_atributos_do_banco()
    personagem.carregar_salvaguardas_do_banco()
    personagem.carregar_status_base_do_banco()
    personagem.carregar_pericias_do_banco()
    personagem.carregar_caracteristicas_do_banco()
    return render_template('ficha_personagem.html', titulo=personagem.nome_personagem, personagem=personagem,classes=classe.classes)

@app.route('/atributos/<id_personagem>',methods=['POST'])
def atributos_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        
        if personagem.exists_atributos_banco() and chave != 'bonus_proficiencia':
            return jsonify({'result': personagem.update_atributos_banco(chave=chave, valor=valor),
                'bonus': int(personagem.get_bonus(chave=chave)),'resistencia':int(personagem.get_bonus(chave=chave))})
        elif personagem.exists_atributos_banco():
            return jsonify({'result': personagem.update_atributos_banco(chave=chave, valor=valor)})
        
        return jsonify({'result':personagem.adicionar_atributo_banco(chave=chave,valor=valor),
                        'bonus':int(personagem.get_bonus(chave=chave)),'resistencia':int(personagem.get_bonus(chave=chave))})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/salvaguarda/<id_personagem>',methods=['POST'])
def salvaguardas_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        chave=request.form.get('chave')
        tipo=request.form.get('tipo')
        
        salvaguarda=Salvaguarda(nome_salvaguarda=chave)
        salvaguarda.carregar_salvaguarda_nome()
        personagem.carregar_atributos_do_banco()
        
        if personagem.exists_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda) and tipo=='remover':
            return jsonify({'result':personagem.delete_salvaguarda_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                            'resistencia':int(personagem.get_salvaguardas(chave))})
        elif tipo=='adicionar':
            return jsonify({'result':personagem.adicionar_salvaguardas_banco(id_salvaguarda=salvaguarda.id_salvaguarda),
                            'resistencia':int(personagem.get_salvaguardas(chave))})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/status_base/<id_personagem>',methods=['POST'])
def status_base_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        chave=request.form.get('chave')
        valor=request.form.get('valor')
        
        if personagem.exists_status_base_banco():
            return jsonify({'result': personagem.update_status_base_banco(chave=chave, valor=valor)})
        else:
            return jsonify({'result':personagem.adicionar_status_base_banco(chave=chave,valor=valor)})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/pericias/<id_personagem>',methods=['POST'])
def pericias_db(id_personagem):
    try:
        id_usuario = session.get('id_usuario')
        personagem = Personagem(id_usuario=id_usuario, id_personagem=id_personagem)
        if personagem.carregar_atributos_do_banco() and personagem.carregar_pericias_do_banco():
            return jsonify({
                'acrobacia': int(personagem.acrobacia),
                'arcanismo': int(personagem.arcanismo),
                'atletismo': int(personagem.atletismo),
                'atuacao': int(personagem.atuacao),
                'enganacao': int(personagem.enganacao),
                'furtividade': int(personagem.furtividade),
                'historia': int(personagem.historia),
                'intimidacao': int(personagem.intimidacao),
                'investigacao': int(personagem.investigacao),
                'lidar_com_animais': int(personagem.lidar_com_animais),
                'medicina': int(personagem.medicina),
                'natureza': int(personagem.natureza),
                'percepcao': int(personagem.percepcao),
                'persuasao': int(personagem.persuasao),
                'prestidigitacao': int(personagem.prestidigitacao),
                'religiao': int(personagem.religiao),
                'sobrevivencia': int(personagem.sobrevivencia)
            })
        return jsonify({'result': False})
    except EOFError as e:
        print(e)
        return jsonify({'result': False})

@app.route('/nova_pericia/<id_personagem>',methods=['POST'])
def adicionar_perica_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        chave=request.form.get('chave')
        tipo=request.form.get('tipo')

        pericia=Pericia(nome_pericia=chave)
        pericia.carregar_pericia_nome()
        personagem.carregar_atributos_do_banco()

        if tipo=='remover' and personagem.exists_pericia_banco(id_pericia=pericia.id_pericia):
            return jsonify({'result':personagem.delete_pericias_banco(id_pericia=pericia.id_pericia),
                            'pericia':int(personagem.get_pericias(chave=chave,status_uso=pericia.status_uso))})
        elif tipo=='adicionar':
            return jsonify({'result':personagem.adicionar_pericias_banco(id_pericia=pericia.id_pericia),
                            'pericia':int(personagem.get_pericias(chave=chave,status_uso=pericia.status_uso))})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/caracteristicas_personagem/<id_personagem>',methods=['POST'])
def caracteristicas_personagems_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        chave=request.form.get('chave')
        valor=request.form.get('valor')
                
        if personagem.exists_caracteristicas_banco():
            return jsonify({'result':personagem.update_caracteristicas_banco(chave=chave,valor=valor)})
        else:
            return jsonify({'result':personagem.adicionar_caracteristicas_banco(chave=chave,valor=valor)})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/base/<id_personagem>',methods=['POST'])
def base_db(id_personagem):
    try:
        id_usuario=session.get('id_usuario')
        personagem=Personagem(id_usuario=id_usuario,id_personagem=id_personagem)
        
        chave=request.form.get('chave')
        valor=request.form.get('valor')
                
        return jsonify({'result':personagem.update_personagem_banco(chave=chave,valor=valor)})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})