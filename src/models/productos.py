from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import Base, session
from src.models.categorias import Categorias


class Productos(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
    unidad_medida = Column(String(3), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    def __init__(self, codigo, nombre, descripcion, unidad_medida, precio, stock, id_categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.unidad_medida = unidad_medida
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria

    def save(self):
        session.add(self)
        session.commit()

    def get():
        productos = session.query(Productos).all()
        return productos
    
    def get_by_id(id):
        producto = session.query(Productos).filter_by(id=id).first()
        return producto

    def delete(self):
        session.delete(self)
        session.commit()