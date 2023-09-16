from flask_socketio import emit, join_room, leave_room, send
from flask import request, redirect, session, jsonify
from flask_session import Session
import datetime

from src import Personagem
from main import socketio

@socketio.on('message')
async def on_message(data):
    try:
        print('mensagem:')
        print(data)
        id_usuario = session.get('id_usuario')
        id_personagem = data['id_personagem']
        room = data['room']
        if id_usuario and id_personagem:
            personagem = Personagem(id_personagem=id_personagem, id_usuario=id_usuario)
            hora = datetime.datetime.now().strftime('%H:%M:%S')
            message = data['message']
            await socketio.emit('message', {'hora': hora, 'name': 'personagem.nome_personagem', 'message': message}, room=room)
    except Exception as e:
        print(e)
        return 403

@socketio.on('join')
def on_join(data):
    try:
        print('entrando:')
        print(data)
        id_personagem = data['id_personagem']
        room = data['room']
        id_usuario = session.get('id_usuario')
        if id_usuario and id_personagem:
            leave_room(room)
            join_room(room) 
            socketio.emit('message', {'message': f'{id_personagem} entrou'}, room=room)  # Use socketio.emit para enviar a mensagem
    except Exception as e:
        print(e)