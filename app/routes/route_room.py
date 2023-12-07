from flask_socketio import join_room, leave_room
from flask import session, abort, render_template, request, jsonify, redirect, url_for

from src import Character, Message, Messages, Room, User, Square
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
        
        return render_template('roons.html', titulo = 'Roons', character_id = character_id, roons = room.roons), 200
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
        character_id = request.form.get('character_id')
        code_room = request.form.get('room_id')
        print(character_id, code_room)
        room = Room(character_id=character_id, user_id=user_id, room_id=code_room)
        
        if room.insert_character_room():
            return redirect(url_for('room_personagem', code_room=code_room, character_id=character_id))
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
        
@app.get('/messages/room=<room_id>')
def get_messages(room_id):
    try:
        """user_id = session.get('user_id')
        if user_id is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        room = Room(room_id=room_id, user_id=user_id)
        #room.character_belongs_room()
        
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        
        messages = Messages(room_id=room_id, limit=limit, offset=offset)        
        messages.load_messages()
        
        return jsonify(messages.messages), 200 """
        messages = [
            {
                'message_id': 1,
                'message': 'bla bla bla'
            },
            {
                'message_id': 2,
                'message': 'bla ola bla'    
            },
            {
                'message_id': 3,
                'message': 'bla bla bllnsdlf'
            }
        ]  
        return jsonify({'messages': messages})
    except Exception as e:
        print(e)
        abort(404)
        
@socketio.on('message')
def on_message(data):
    try:
        """user_id = session.get('user_id')
        character_id = data.get('character_id')
        room = data.get('room')
        if user_id and character_id and room:
            message = Message(message=data['message'], name_character=data['nome_personagem'], character_id=character_id, room=room)
            socketio.emit('message', message.message, room=room)""" 
        message = data.get('message')
        room = data.get('room_id')
        print(message)
        socketio.emit('message', {'message': message}, room=room)
    except Exception as e:
        print(e)
        return 403
   
@socketio.on('join')
def on_join(data):
    try:
        #user_id = session.get('user_id')
        #character_id = data.get('character_id')
        room = data.get('room_id')
        leave_room(room)
        join_room(room)
    except Exception as e:
        print(e)
        return 403

@socketio.on('leave')
def on_leave(data):
    try:
        room = data.get('room_id')
        leave_room(room)
    except Exception as e:
        print(e)
        return 403
    
@socketio.on('update_coordinates')
def updateSquare(data):
    try:
        square_id = data.get('square_id')
        x = data.get('x') 
        y = data.get('y')
        room = data.get('room_id')
        socketio.emit('update_square', {'square_id': square_id, 'x': x, 'y': y}, room=room)
    except Exception as e:
        print(e)
        return 403
    
@socketio.on('new_square_position')
def new_square_postion(data):
    try:
        square_id = data.get('square_id')
        x = data.get('x')
        y = data.get('y')
        room = data.get('room_id')    
        square = Square(square_id=square_id, x=x, y=y)
        square.update_square_position()   
    except Exception as e:
        print(e)
        return 403
    
@app.get('/squares/<room_id>')
def get_squares(room_id):
    try:
        squares = Square(room_id=room_id)
        squares.load_squares()
        room = Room(room_id=room_id)
        room.load_room()
        return jsonify({'result': True, 'background': room.background_cartesian_plane_load, 'data': squares.squares}), 200    
    except Exception as e:  
        print(e)
        return jsonify({'result': False, 'error': 'Erro interno do servidor'}), 500
    
@app.post('/squares/<room_id>')
def post_squares(room_id):
    try:
        user_room_id = request.form.get('key')
        square = Square(user_room_id=user_room_id)
        result, squares = square.insert_square()
        socketio.emit('new_squares', squares, room=room_id)
        return jsonify({'result': result,  'data': squares}), 200    
    except Exception as e:  
        print(e)
        return jsonify({'result': False}), 403
    
@app.put('/squares/<room_id>')
def put_squares(room_id):
    try:
        image = request.files.get('image')
        square_id = request.form.get('square_id')
        square = Square(square_id=square_id, square_image=image)
        result, url_image = square.update_square_image()
        socketio.emit('update_squares', {'square_image': url_image, 'square_id': square_id}, room=room_id)
        return jsonify({'result': result,  'data': {'square_image': url_image, 'square_id': square_id}}), 200    
    except Exception as e:  
        print(e)
        return jsonify({'result': False}), 403
    
@app.delete('/squares/<room_id>')
def delete_squares(room_id):
    try:
        square_id = request.form.get('key')
        square = Square(square_id=square_id)
        result = square.delete_square()
        print(square_id)
        socketio.emit('delete_square', {'square_id': square_id}, room=room_id)
        return jsonify({'result': result}), 200    
    except Exception as e:  
        print(e)
        return jsonify({'result': False}), 403
    
@app.put('/background_cartesian_plane/<room_id>')
def put_background_cartesian_plane(room_id):
    try:
        image = request.files.get('image')
        room = Room(background_cartesian_plane=image, room_id=room_id)
        result, url_image = room.update_room_image()
        socketio.emit('new_background', {'background_image': url_image}, room=room_id)
        return jsonify({'result': result,  'data': {'background_image': url_image}}), 200    
    except Exception as e:  
        print(e)
        return jsonify({'result': False}), 403
