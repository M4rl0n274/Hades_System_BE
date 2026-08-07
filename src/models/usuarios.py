from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Base, session


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    email = Column(String(190), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default='usuario')

    def __init__(self, email, password, nombre, rol='usuario'):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.nombre = nombre
        self.rol = rol

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def get_by_email(email):
        return session.query(Usuarios).filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return session.query(Usuarios).filter_by(id=id).first()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'rol': self.rol
        }