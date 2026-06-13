from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from src.models import Base, session

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)

    id_categoria = Column(
        Integer,
        ForeignKey('categorias.id'),
        nullable=False
    )

    nombre_producto = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    valor_unitario = Column(Numeric(10,2), nullable=False)

    def __init__(self, id_categoria, nombre_producto,
                 descripcion, valor_unitario):

        self.id_categoria = id_categoria
        self.nombre_producto = nombre_producto
        self.descripcion = descripcion
        self.valor_unitario = valor_unitario

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Producto).all()

    def get_by_id(id):
        return session.query(Producto).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()