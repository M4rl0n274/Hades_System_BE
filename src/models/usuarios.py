from sqlalchemy import Column, Integer, String, Date
from src.models import Base, session

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    documento_identidad = Column(String(50), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    rol = Column(String(50), nullable=False)

    def __init__(self, nombre, edad, correo, password,
                 documento_identidad, fecha_nacimiento, rol):

        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.password = password
        self.documento_identidad = documento_identidad
        self.fecha_nacimiento = fecha_nacimiento
        self.rol = rol

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Usuario).all()

    def get_by_id(id):
        return session.query(Usuario).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()