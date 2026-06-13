from sqlalchemy import Column, Integer
from sqlalchemy import Numeric, ForeignKey
from src.models import Base, session

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'

    id = Column(Integer, primary_key=True)
    id_factura = Column(Integer,ForeignKey('factura.id'),nullable=False)

    id_producto = Column(Integer,ForeignKey('productos.id'),nullable=False)

    cantidad = Column(Integer, nullable=False)

    precio_unitario = Column(
        Numeric(10,2),
        nullable=False
    )

    subtotal_producto = Column(
        Numeric(10,2),
        nullable=False
    )

    def __init__(self, id_factura, id_producto,
                 cantidad, precio_unitario,
                 subtotal_producto):

        self.id_factura = id_factura
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal_producto = subtotal_producto

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(DetalleFactura).all()

    def get_by_id(id):
        return session.query(DetalleFactura).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()