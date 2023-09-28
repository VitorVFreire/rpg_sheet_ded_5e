from flask_socketio import join_room, leave_room
from flask import session, abort, render_template, request, jsonify

from src import Personagem, Message, Messages, Room  
from main import socketio, app

@app.route('/roons/<id_personagem>')
async def roons(id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        room = Room(id_personagem=id_personagem)
        
        room.load_character_room()
        
        return render_template('roons.html', titulo = 'Roons', id_personagem = id_personagem, roons = room.roons)
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.route('/room/<code_room>/<id_personagem>')
async def room(code_room, id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        personagem = Personagem(id_usuario=session.get('id_usuario'), id_personagem=id_personagem)
        room = Room(id_room=code_room, id_personagem=id_personagem)
        
        room.character_belongs_room()
        
        return render_template('room_game.html', titulo = 'Room', room = code_room, id_personagem = id_personagem, nome_personagem = await personagem.nome_personagem)
    except Exception as e:
        print(e)
        abort(403, "Deve ser Feito Login para acessar essa pagina")
        
@app.get('/messages/room=<id_room>&id_personagem=<id_personagem>')
def get_messages(id_room,id_personagem):
    try:
        if session.get('id_usuario') is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        room = Room(id_room=id_room, id_personagem=id_personagem)
        room.character_belongs_room()
        
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        
        messages = Messages(id_room=id_room, limit=limit, offset=offset)        
        messages.load_messages_bank()
        
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
            message = Message(message=data['message'], name_character=data['nome_personagem'], id_personagem=id_personagem, room=room)
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
            messages = Messages(id_room=room)
            leave_room(room)
            join_room(room)
            socketio.emit('message', {'message': f'{nome_personagem} join to room'}, room=room)
    except Exception as e:
        print(e)
        return 403