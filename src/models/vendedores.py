from sqlalchemy import Column, Integer, String,func
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
    
    
    #Paginación

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}     
        
    def paginate(page=1, per_page=5):
        total = (session.query(func.count(Vendedor.id)).scalar())
        vendedor = session.query(Vendedor).offset((page - 1) * per_page).limit(per_page).all()
        return vendedor, total



