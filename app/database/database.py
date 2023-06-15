import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('USER_BASE'),
  password=os.getenv('PASSWORD_BASE'),
  database="RPG"
)