from .main import app, socketio
from .database import attributes
from .routes import route_character, route_admin, routes, route_room
from .src import User, Skill, Race, Classe, SavingThrow, Spell, Equipment, Image, Square
from .src import Message, Messages, Room,  Db, TypeDamage, KindEquipment, Coin
from .src import Character, CharacterEquipment, CharacterAttribute, CharacterCharacteristics
from .src import CharacterSavingThrow, CharacterSkills, CharacterSpell, CharacterStatusBase
from .tests import *
