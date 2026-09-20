from flask import Flask
#Se añade CORS para que las peticiones de IONIC no sean rechazadas
from flask_cors import CORS
from src.models import Base, engine
from src.models.categorias import Categorias 
from src.models.clientes import Clientes 
from src.models.detalle_factura import DetalleFactura
from src.models.factura import Factura
from src.models.productos import Productos
from src.models.usuarios import Usuarios
from src.models.vendedores import Vendedor
#importar todas las rutas
from src.routes import all_blueprints

#jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# se añade CORS y App.run para habilitrar los CORS en todas las rutas y probar 
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.run(host='0.0.0.0', port=5000, debug=True)

app.config['JWT_SECRET_KEY'] = os.getenv ('JWT_SECRET_KEY')

#crear la base de datos de los modelos
Base.metadata.create_all(engine)

#publicar el listado de rutas
prefix = '/api/v1'
for bp in all_blueprints:
    print(bp)
    url_prefix=f'{prefix}/{bp.name}'
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)

if __name__ == '__main__':
    app.run(debug=True)

