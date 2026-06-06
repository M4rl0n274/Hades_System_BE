from sqlalchemy import Column, Integer, String
from src.models import Base, session 

class Categorias(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)

#constructor de la clase
    def __init__(self, nombre):
        self.nombre = nombre

    def save(self):
        session.add(self)
        session.commit()

    def get():
        categorias = session.query(Categorias).all()
        return categorias
    
    def get_by_id(id):
        categoria = session.query(Categorias).filter_by(id=id).first()
        return categoria

    def delete(self):
        session.delete(self)
        session.commit()