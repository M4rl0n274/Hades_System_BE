from flask import Flask
from src.models import Base, engine
from src.models.categorias import Categorias 
from src.models.clientes import Clientes 
from src.models.detalle_factura import DetalleFactura
from src.models.factura import Factura
from src.models.productos import Productos
from src.models.usuarios import Usuario 
from src.models.vendedores import Vendedor
from src.routes import all_blueprints

app = Flask(__name__)

Base.metadata.create_all(engine)

prefix = '/api/v1'
for bp in all_blueprints:
    print(bp)
    url_prefix=f'{prefix}/{bp.name}'
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)

if __name__ == '__main__':
    app.run(debug=True)

