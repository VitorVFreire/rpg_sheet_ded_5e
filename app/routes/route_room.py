from flask_socketio import join_room, leave_room
from flask import session, abort, render_template, request, jsonify, redirect, url_for

from src import Character, Message, Messages, Room, User, Square
from main import socketio, app

@app.post('/room')
def insert_room():
    try:
        user_id = session.get('user_id')
        room_name = request.form.get('room_name')
        room_password = request.form.get('room_password')

        room = Room(user_id=user_id, room_name=room_name, room_password=room_password)

        if room.insert_room():
            return jsonify({'result': True, 'data': {'room_id': room.room_id, 'user_room_id': room.user_room_id, 'room_name': room.room_name, 'can_delete': room.can_delete}}), 200
        return jsonify({'result': False, 'error': room.error}), 200
    except Exception as e:
        print(e)
        
@app.delete('/room')
def delete_room():
    try:
        user_id = session.get('user_id')
        room_id = request.form.get('room_id')

        room = Room(user_id=user_id, room_id=room_id)

        if room.delete_room():
            return jsonify({'result': True}), 200
        return jsonify({'result': False, 'error': room.error}), 200
    except Exception as e:
        print(e)

@app.route('/roons_page')
def page_roons():
    try:
        user_id = session.get('user_id')
        
        if user_id is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        return render_template('index.html', id=user_id), 200     
    except Exception as e:
        print(e)
       
@app.get('/roons')
def get_roons():
    try:
        user_id = session.get('user_id')
        
        room = Room(user_id=user_id)
        
        result = room.load_user_room()
        
        return jsonify({'result': result, 'data': room.roons}), 200     
    except Exception as e:
        print(e)
        
@app.post('/user_room')
def insert_user_room():
    try:
        user_id = session.get('user_id')
        room_name = request.form.get('room_name')
        room_password = request.form.get('room_password')
                
        room = Room(user_id=user_id, room_name=room_name, room_password=room_password)
        
        if room.insert_user_room_with_password():
            return jsonify({'result': True, 'data': {'room_id': room.room_id, 'user_room_id': room.user_room_id, 'room_name': room.room_name, 'can_delete': room.can_delete}}), 200
        return jsonify({'result': False, 'error': room.error}), 200    
    except Exception as e:
        print(e)
               
@app.route('/room/<room_id>/<user_room_id>')
def room(room_id, user_room_id):
    try:
        user_id = session.get('user_id')
        if user_id is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        room = Room(room_id=room_id, user_room_id=user_room_id, user_id=user_id)
                
        room.exists_room()
        room.user_has_room()
        
        return render_template('index.html', id=session.get('user_id')), 200
    except Exception as e:
        print(e)
        abort(404)
        
@app.get('/messages/room=<room_id>')
async def get_messages(room_id):
    try:
        user_id = session.get('user_id')
        if user_id is None:
            abort(403, "Deve ser Feito Login para acessar essa pagina")
        
        #room = Room(room_id=room_id, user_id=user_id)
        #room.character_belongs_room()
        
        #limit = request.args.get('limit', default=None)
        #offset = request.args.get('offset', default=None)
        
        #messages = Messages(room_id=room_id, limit=limit, offset=offset)  
        messages = Messages(room_id=room_id)     
        
        result = await messages.load_messages()
         
        return jsonify({'result': result, 'data': messages.messages}), 200
    except Exception as e:
        print(e)
        abort(404)
        
@socketio.on('message')
def on_message(data):
    try:
        user_id = session.get('user_id')
        if user_id is None:
            abort(403)

        message = data.get('message')
        room = data.get('room_id')
        id = data.get('id')
        
        user_id_message = id.get('user_id') if id.get('user_id') else None
        character_id_message = id.get('character_id') if id.get('character_id') else None
        
        name = id.get('name')
        #para funcionar a rolangem dos dados com bonus deve ser feito : !r 1d20 +1 ou !r 2d20 +2 (o sinal tendo q ficar grudado ao numero e com 1 espaço do dado)
        # para rolar varias combinações de dado é o seguinte: !r 1d20 + 1d30 iria retornar a soma total mas so vai mostrar o roll do primeiro
        msg = Message(message=message, name=name, character_id=character_id_message, user_id=user_id_message, room_id=room)

        socketio.emit('message', msg.message, room=room)
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
