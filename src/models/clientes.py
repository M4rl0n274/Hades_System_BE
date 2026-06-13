from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    documento = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(50), unique=True, nullable=False)

    def __init__(self, documento, nombre, direccion, telefono, email):
        self.documento = documento
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def save(self):
        session.add(self)
        session.commit()

    def get():
        clientes = session.query(Clientes).all()
        return clientes
    
    def get_by_id(id):
        cliente = session.query(Clientes).filter_by(id=id).first()
        return cliente

    def delete(self):
        session.delete(self)
        session.commit()
        
        
        
        