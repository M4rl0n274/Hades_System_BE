from sqlalchemy import Column, Integer, String, Date
from src.models import Base, session

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    documento_identidad = Column(String(50), unique=True, nullable=False)
    rol = Column(String(50), nullable=False)

    def __init__(self, nombre, apellido, correo, password,
                 documento_identidad, rol):

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.password = password
        self.documento_identidad = documento_identidad
        self.rol = rol

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def get():
        return session.query(Usuario).all()

    def get_by_id(id):
        return session.query(Usuario).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()