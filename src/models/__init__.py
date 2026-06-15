from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

#motor de conexión
engine = create_engine("mysql+pymysql://root@127.0.0.1:3308/hades?charset=utf8mb4")

#se inicia el motor
connection = engine.connect()

#inicio de seión del motor
Session = sessionmaker(bind=engine)

session = Session()
#se crea el objeto que permite crear los objetos de la base de datos 
Base = declarative_base()
Base.metadata.bind = engine


