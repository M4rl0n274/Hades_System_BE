from sqlalchemy import Column, Integer, String,func
from src.models import Base, session


class Clientes(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    documento = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)

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
        
        
        
        
                
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}     
        
    def paginate(page=1, per_page=100):
        total = (session.query(func.count(Clientes.id)).scalar())
        clientes = session.query(Clientes).offset((page - 1) * per_page).limit(per_page).all()
        return clientes, total
        
        