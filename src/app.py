from flask import Flask
from src.models import Base, engine

from src.models.clientes import Clientes
from src.models.usuarios import Usuario
from src.models.vendedores import Vendedor
from src.models.categorias import Categoria
from src.models.productos import Producto
from src.models.factura import Factura
from src.models.detalle_factura import DetalleFactura

app = Flask(__name__)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)

