from flask_socketio import join_room, leave_room
from flask import session, abort, render_template, request, jsonify, redirect, url_for

from src import Character, Message, Messages, Room, User 
from main import socketio, app

@app.post('/insert/room/<id_personagem>/<code_room>')
async def room_personagem_post(id_personagem, code_room):
    try:
        room = Room(id_room=code_room ,id_character=id_personagem)

        return jsonify({'result': room.insert_character_room()}), 200
    except Exception as e:
        print(e)
        return 404

@app.route('/roons/<id_personagem>')
async def roons(id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        room = Room(id_character=id_personagem)
        
        room.load_character_room()
        
        return render_template('roons.html', titulo = 'Roons', id_personagem = id_personagem, roons = room.roons), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.route('/room')
async def room():
    try:
        id_usuario = session.get('id_usuario')
        personagens = User(id=id_usuario)
        await personagens.load_characters()
        return render_template('room.html', titulo = 'Room', personagens = await personagens.characters), 200
    except Exception as e:
        print(e)
        
@app.post('/room')
async def insert_room():
    try:
        id_usuario = session.get('id_usuario')
        id_personagem = request.form.get('id_personagem')
        code_room = request.form.get('id_room')
        print(id_personagem, code_room)
        room = Room(id_character=id_personagem, id_user=id_usuario, id_room=code_room)
        
        if room.insert_character_room():
            return redirect(url_for('room_personagem', code_room=code_room, id_personagem=id_personagem))
        return render_template('index.html', msg = 'Erro em adicionar sala'), 500      
    except Exception as e:
        print(e)
        
@app.route('/room/<code_room>/<id_personagem>')
async def room_personagem(code_room, id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        personagem = Character(id_user=session.get('id_usuario'), id_character=id_personagem)
        room = Room(id_room=code_room, id_character=id_personagem)
        
        room.character_belongs_room()
        
        return render_template('room_game.html', titulo = 'Room', room = code_room, id_personagem = id_personagem, nome_personagem = await personagem.character_name)
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.get('/messages/room=<id_room>&id_personagem=<id_personagem>')
def get_messages(id_room,id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        room = Room(id_room=id_room, id_character=id_personagem)
        room.character_belongs_room()
        
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        
        messages = Messages(id_room=id_room, limit=limit, offset=offset)        
        messages.load_messages()
        
        return jsonify(messages.messages), 200   
    except Exception as e:
        print(e)
        abort(404)
        
@socketio.on('message')
def on_message(data):
    try:
        id_usuario = session.get('id_usuario')
        id_personagem = data.get('id_personagem')
        room = data.get('room')
        if id_usuario and id_personagem and room:
            message = Message(message=data['message'], name_character=data['nome_personagem'], id_character=id_personagem, room=room)
            socketio.emit('message', message.message, room=room)
    except Exception as e:
        print(e)
        return 403

@socketio.on('join')
def on_join(data):
    try:
        id_usuario = session.get('id_usuario')
        id_personagem = data.get('id_personagem')
        room = data.get('room')
        if id_usuario and id_personagem and room:
            nome_personagem = data['nome_personagem']
            leave_room(room)
            join_room(room)
            socketio.emit('message', {'message': f'{nome_personagem} join to room'}, room=room)
    except Exception as e:
        print(e)
        return 403