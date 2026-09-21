from sqlalchemy import Column, Integer, DateTime,func
from sqlalchemy import Numeric, ForeignKey
from src.models import Base, session

class Factura(Base):
    __tablename__ = 'factura'

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer,ForeignKey('clientes.id'),nullable=False)
    id_vendedor = Column(Integer,ForeignKey('vendedores.id'),nullable=False)
    id_usuario = Column(Integer,ForeignKey('usuarios.id'),nullable=False)
    fecha_factura = Column(DateTime, nullable=False)
    subtotal = Column(Numeric(10,2))
    iva = Column(Numeric(10,2))
    total = Column(Numeric(10,2))

    def __init__(self, id_cliente, id_vendedor,
                 id_usuario, fecha_factura,
                 subtotal, iva, total):

        self.id_cliente = id_cliente
        self.id_vendedor = id_vendedor
        self.id_usuario = id_usuario
        self.fecha_factura = fecha_factura
        self.subtotal = subtotal
        self.iva = iva
        self.total = total

    def save(self):
        session.add(self)
        session.commit()

    def get():
        return session.query(Factura).all()

    def get_by_id(id):
        return session.query(Factura).filter_by(id=id).first()

    def delete(self):
        session.delete(self)
        session.commit()
        
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    
    
    #Paginación

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}     
        
    def paginate(page=1, per_page=5, id_cliente=None, q=None):
            query = session.query(Factura)

            # 1. Filtrar por cliente si se especifica id_cliente
            if id_cliente:
                query = query.filter(Factura.id_cliente == id_cliente)

            # 2. Filtrar por búsqueda 'q' si viene un número de factura
            if q and str(q).strip():
                term = str(q).strip()
                if term.isdigit():
                    query = query.filter(Factura.id == int(term))

            # 3. Conteo total de registros filtrados
            total = query.count()

            # 4. Obtener los registros paginados (ordenados por fecha o ID descendente)
            facturas = query.order_by(Factura.id.desc()).offset((page - 1) * per_page).limit(per_page).all()

            return facturas, total