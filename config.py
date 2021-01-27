import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(verbose=True)
HOST = os.getenv("HOST")
PWD = os.getenv("PWD")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
DB = os.getenv("DB")

db_path = "mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8".format(USER, PWD, HOST,DB)
engine = create_engine(db_path, encoding='utf-8')
plus_path = os.getenv("PLUS")
id = os.getenv("ID")
password = os.getenv("PASSWORD")
credential = os.getenv("CREDENTIAL")