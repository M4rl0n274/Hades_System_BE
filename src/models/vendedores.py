from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Vendedor(Base):
    __tablename__ = 'vendedores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento_identidad = Column(String(50), unique=True, nullable=False)
    correo = Column(String(150), unique=True)

    def __init__(self, nombre, apellido,
                 documento_identidad, correo):

        self.nombre = nombre
        self.apellido = apellido
        self.documento_identidad = documento_identidad
        self.correo = correo

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Vendedor).all()

    def get_by_id(id):
        return session.query(Vendedor).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()
    










