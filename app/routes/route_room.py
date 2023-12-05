from flask_socketio import join_room, leave_room
from flask import session, abort, render_template, request, jsonify, redirect, url_for

from src import Character, Message, Messages, Room, User 
from main import socketio, app

@app.post('/insert/room/<character_id>/<code_room>')
async def post_character_room(character_id, code_room):
    try:
        room = Room(room_id=code_room ,character_id=character_id)

        return jsonify({'result': room.insert_character_room()}), 200
    except Exception as e:
        print(e)
        return 404

@app.route('/roons/<character_id>')
async def roons(character_id):
    try:
        if session.get('user_id') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        room = Room(character_id=character_id)
        
        room.load_character_room()
        
        return render_template('roons.html', titulo = 'Roons', id_personagem = character_id, roons = room.roons), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.route('/room')
async def room():
    try:
        user_id = session.get('user_id')
        character = User(user_id=user_id)
        await character.load_characters()
        return render_template('room.html', titulo = 'Room', personagens = await character.characters), 200
    except Exception as e:
        print(e)
        
@app.post('/room')
async def insert_room():
    try:
        user_id = session.get('user_id')
        character_id = request.form.get('id_personagem')
        code_room = request.form.get('room_id')
        print(character_id, code_room)
        room = Room(character_id=character_id, user_id=user_id, room_id=code_room)
        
        if room.insert_character_room():
            return redirect(url_for('room_personagem', code_room=code_room, id_personagem=character_id))
        return render_template('index.html', msg = 'Erro em adicionar sala'), 500      
    except Exception as e:
        print(e)
        
@app.route('/room/<code_room>/<character_id>')
async def character_room(code_room, character_id):
    try:
        if session.get('user_id') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        #room = Room(room_id=code_room, character_id=character_id)
        
        #room.character_belongs_room()
        
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.get('/messages/room=<room_id>&id_personagem=<character_id>')
def get_messages(room_id,character_id):
    try:
        if session.get('user_id') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        room = Room(room_id=room_id, character_id=character_id)
        room.character_belongs_room()
        
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        
        messages = Messages(room_id=room_id, limit=limit, offset=offset)        
        messages.load_messages()
        
        return jsonify(messages.messages), 200   
    except Exception as e:
        print(e)
        abort(404)
        
@socketio.on('message')
def on_message(data):
    try:
        user_id = session.get('user_id')
        character_id = data.get('id_personagem')
        room = data.get('room')
        if user_id and character_id and room:
            message = Message(message=data['message'], name_character=data['nome_personagem'], character_id=character_id, room=room)
            socketio.emit('message', message.message, room=room)
    except Exception as e:
        print(e)
        return 403

@socketio.on('join')
def on_join(data):
    try:
        user_id = session.get('user_id')
        character_id = data.get('id_personagem')
        room = data.get('room')
        if user_id and character_id and room:
            character_name = data['nome_personagem']
            leave_room(room)
            join_room(room)
            socketio.emit('message', {'message': f'{character_name} join to room'}, room=room)
    except Exception as e:
        print(e)
        return 403
    
@socketio.on('update_coordinates')
def updateSquare(data):
    try:
        print(data)
    except Exception as e:
        print(e)
        return 403
    
@app.get('/squares')
def squares():
    return jsonify({'result': True,'data': [{'id': 0, 'x': 0, 'y': 0}, {'id': 1, 'x': 6, 'y': 1}, {'id': 3, 'x': 3, 'y': 9}]}), 200