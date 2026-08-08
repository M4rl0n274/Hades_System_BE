from sqlalchemy import Column, Integer, String, Date,func
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Base, session

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    documento_identidad = Column(String(50), unique=True, nullable=False)
    rol = Column(String(50), nullable=False)

    def __init__(self, nombre, apellido, correo, password,
                 documento_identidad, rol='usuario'):

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.password_hash = generate_password_hash(password)
        self.documento_identidad = documento_identidad
        self.rol = rol
        
        
    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)  


    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()  # Limpia la transacción si ocurre un error (como IntegrityError)
            raise  # Vuelve a lanzar la excepción para que la ruta la capture

    
    @staticmethod
    def get_by_email(correo):
        return session.query(Usuarios).filter_by(correo=correo).first()
    
    # src/models/usuarios.py

    @staticmethod
    def get_by_documento(documento):
        return session.query(Usuarios).filter_by(documento_identidad=documento).first()
    
    @staticmethod
    def get_by_id(id):
        return session.query(Usuarios).filter_by(id=id).first()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'documento_identidad': self.documento_identidad,
            'rol': self.rol
        }
    @staticmethod        
    def get():
        return session.query(Usuarios).all()
    @staticmethod
    def delete(self):
        session.delete(self)
        session.commit()
        
        
    #Paginación

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}     
        
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Usuarios.id)).scalar())
        usuarios = session.query(Usuarios).offset((page - 1) * per_page).limit(per_page).all()
        return usuarios, total