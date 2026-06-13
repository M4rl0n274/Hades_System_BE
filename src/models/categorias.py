from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(String(255))

    def __init__(self, nombre_categoria, descripcion):
        self.nombre_categoria = nombre_categoria
        self.descripcion = descripcion

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Categoria).all()

    def get_by_id(id):
        return session.query(Categoria).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()     