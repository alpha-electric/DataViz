import os
import json
from pathlib import Path
from dotenv import load_dotenv
from enum import Enum
from modules.sql_interface import SQL_Interface

# just an example, maybe got diff in implementation for postgresql and sqlite and MySQL. MongoDB confim different
class DbType(Enum):
  SQL = 1
  MONGO = 2





# Load the environment variables from .env file
path = Path(__file__).parent / ".env"
if path.exists():
    load_dotenv()
else:
    raise IOError(".env file not found")


class Config:
    base_path = Path(__file__).resolve().parent#.parent.parent
    print(f"base_path: {base_path}")
    DB_PATH = base_path / "data" / "ae.db"
    DB_TYPE = DbType.SQL
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{str(DB_PATH)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = json.loads(
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS").lower()
    )
    SQLALCHEMY_ECHO = json.loads(os.getenv("SQLALCHEMY_ECHO").lower())
    DEBUG = json.loads(os.getenv("DEBUG").lower())
    FAKE_STORE = {
        "MIAO":"WOOF"
    }
    
    

# set up other stuff
if Config.DB_TYPE == DbType.SQL:
    Config.DB = SQL_Interface(Config)



# class App:
#   __conf = {
#     "username": "",
#     "password": "",
#     "MYSQL_PORT": 3306,
#     "MYSQL_DATABASE": 'mydb',
#     "MYSQL_DATABASE_TABLES": ['tb_users', 'tb_groups'],
#     "DB_PATH":"data/ae.db",
#     "SQLALCHEMY_DATABASE_URI": f"sqlite:///{str(db_path)}"
#   }
#   __setters = ["username", "password"]

#   @staticmethod
#   def config(name):
#     return App.__conf[name]

#   @staticmethod
#   def set(name, value):
#     if name in App.__setters:
#       App.__conf[name] = value
#     else:
#       raise NameError("Name not accepted in set() method")