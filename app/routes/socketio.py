from flask_socketio import emit, join_room, leave_room, send
from flask import session

from src import Message
from main import socketio

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
            leave_room(room)
            join_room(room) 
            socketio.emit('message', {'message': f'{nome_personagem} join to room'}, room=room)
    except Exception as e:
        print(e)
        return 403