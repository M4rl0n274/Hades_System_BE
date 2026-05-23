from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

engine = create_engine("mysql+pymysql://root@localhost:3306/HadesSystem?charset=utf8mb4")

Connection = engine.conenct()

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()
Base.metadata.bien = engine

