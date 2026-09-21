from sqlalchemy import Column, Integer, String, DateTime, func
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Base, session

class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    documentoIdentidad = Column(String(50), unique=True, nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    FechaDeNacimiento = Column(DateTime, nullable=False)

    def __init__(self, nombre, apellido, edad, correo, documentoIdentidad,
                 direccion, telefono, FechaDeNacimiento, password=None):

        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.correo = correo.strip().lower() if correo else ''
        self.documentoIdentidad = documentoIdentidad
        self.direccion = direccion
        self.telefono = telefono
        self.FechaDeNacimiento = FechaDeNacimiento
        
        # Asignar la contraseña recibida o el documento de identidad como clave por defecto
        clave_inicial = str(password).strip() if password and str(password).strip() != '' else str(documentoIdentidad).strip()
        self.password_hash = generate_password_hash(clave_inicial)

    # Propiedad dinámica para que create_token(entidad) pueda leer 'entidad.rol'
    @property
    def rol(self):
        return 'Cliente'

    def verificar_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def get():
        return session.query(Clientes).all()
    
    @staticmethod
    def get_by_id(id):
        return session.query(Clientes).filter_by(id=id).first()

    @staticmethod
    def get_by_email(correo):
        if not correo:
            return None
        return session.query(Clientes).filter(func.lower(Clientes.correo) == correo.strip().lower()).first()

    def delete(self):
        session.delete(self)
        session.commit()

    def to_dict(self):
        data = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        data.pop('password_hash', None)
        data['rol'] = 'Cliente'
        return data  

    @staticmethod    
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Clientes.id)).scalar())
        clientes = session.query(Clientes).offset((page - 1) * per_page).limit(per_page).all()
        return clientes, total