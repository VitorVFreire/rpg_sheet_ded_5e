from flask import Flask
from flask_session import Session
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)

from routes import *

if __name__ == '__main__':
    socketio.run(app, port=8085, host='0.0.0.0', debug=True)

