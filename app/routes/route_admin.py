from flask import Flask, request, session, jsonify, render_template, url_for, redirect
from flask_session import Session
import asyncio

from main import app
from src import Usuario, Personagem, Classe, Raca, Pericia, Salvaguarda, Habilidade, Equipamento

@app.route('/admin')
async def admin():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/admin_pag.html',titulo='ADMIN')
    return redirect(url_for('index'))

@app.route('/criar_classe')
async def nova_classe():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/add_classe.html',titulo='Nova Classe')
    return redirect(url_for('index'))
    
@app.post('/criar_classe')
async def insert_classe():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            classe = Classe(nome_classe=request.form.get('nome_classe'))
            return jsonify({'result': await classe.insert_classe_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_raca')
async def nova_raca():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/add_raca.html',titulo='Nova raca')
    return redirect(url_for('index'))
    
@app.post('/criar_raca')
async  def insert_raca():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            nome_raca = request.form.get('nome_raca')
            
            raca = Raca(nome_raca=nome_raca)
            
            return jsonify({'result': await raca.insert_raca_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_pericia')
async def nova_pericia():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/add_pericia.html',titulo='Nova pericia')
    return redirect(url_for('index'))
    
@app.post('/criar_pericia')
async def insert_pericia():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            nome_pericia = request.form.get('nome_pericia')
            status_uso = request.form.get('status_uso',)
            
            pericia = Pericia(nome_pericia=nome_pericia,status_uso=status_uso)
            
            return jsonify({'result': await pericia.insert_pericia_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_salvaguarda')
async def nova_salvaguarda():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/add_salvaguarda.html',titulo='Nova salvaguarda')
    return redirect(url_for('index'))
    
@app.post('/criar_salvaguarda')
async def insert_salvaguarda():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            nome_salvaguarda = request.form.get('nome_salvaguarda')
            
            salvaguarda = Salvaguarda(nome_salvaguarda=nome_salvaguarda)
            
            return jsonify({'result': await salvaguarda.insert_salvaguarda_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_habilidade')
async def nova_habilidade():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        return render_template('admin/add_habilidade.html',titulo='Nova habilidade')
    return redirect(url_for('index'))
    
@app.post('/criar_habilidade')
async def insert_habilidade():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            nome_habilidade = request.form.get('nome_habilidade')
            nome_atributo = request.form.get('nome_atributo')
            lados_dados = request.form.get('lados_dados')
            link_detalhes = request.form.get('link_detalhes')
            tipo_dano = request.form.get('tipo_dano')
            qtd_dados = request.form.get('qtd_dados')
            nivel_habilidade = request.form.get('nivel_habilidade')
            adicional_por_nivel = request.form.get('adicional_por_nivel')
            
            habilidade = Habilidade(
                nome_atributo=nome_atributo,
                lados_dados=lados_dados,
                link_detalhes=link_detalhes,
                nome_habilidade=nome_habilidade,
                tipo_dano=tipo_dano,
                qtd_dados=qtd_dados,
                nivel_habilidade=nivel_habilidade,
                adicional_por_nivel=adicional_por_nivel
                )
            
            return jsonify({'result': await habilidade.insert_habilidade_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})
    
@app.route('/criar_equipamento')
async def novo_equipamento():
    usuario = Usuario(id=session.get('id_usuario'))
    
    if await usuario.usuario_admin():
        tipo_equipamentos = Equipamento()
        await tipo_equipamentos.carregar_tipo_equipamentos()
        return render_template('admin/add_equipamento.html',titulo='Novo equipamento', tipo_equipamentos = tipo_equipamentos.tipo_equipamentos)
    return redirect(url_for('index'))
    
@app.post('/criar_equipamento')
async def insert_equipamento():
    try:
        usuario = Usuario(id=session.get('id_usuario'))
        
        if await usuario.usuario_admin():
            id_tipo_equipamento = request.form.get("id_tipo_equipamento") 
            nome_equipamento = request.form.get('nome_equipamento')
            descricao = request.form.get('descricao')
            preco = request.form.get('preco')
            peso = request.form.get('peso')
            ca = request.form.get('ca')
            dado = request.form.get('dado')
            bonus = request.form.get('bonus')
            imagem_equipamento = request.files.get('imagem_equipamento')
            
            equipamento = Equipamento(
                id_tipo_equipamento=id_tipo_equipamento,
                nome_equipamento=nome_equipamento,
                descricao=descricao,
                preco=preco,
                peso=peso,
                ca=ca,
                dado=dado,
                bonus=bonus,
                imagem_equipamento=imagem_equipamento
            )
            
            return jsonify({'result': await equipamento.insert_equipamento_banco()})
        return jsonify({'result':False})
    except EOFError as e:
        print(e)
        return jsonify({'result':False})