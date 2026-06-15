from sqlalchemy import Column, Integer, String, DateTime
from src.models import Base, session

class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String(50), unique=True, nullable=False)
    documentoIdentidad = Column(String(50), unique=True, nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    FechaDeNacimiento= Column(DateTime, nullable=False)

    def __init__(self, nombre, apellido, edad,correo, documentoIdentidad,
                direccion, telefono,FechaDeNacimiento):

        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.correo = correo
        self.documentoIdentidad = documentoIdentidad
        self.direccion = direccion
        self.telefono = telefono
        self.FechaDeNacimiento = FechaDeNacimiento  
            

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