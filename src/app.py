from flask import Flask
from src.models import Base, engine
from src.models.clientes import Clientes
from src.models.productos import Productos
#importar todas las rutas
from src.routes import all_blueprints


app = Flask(__name__)

#crear la base de datos de los modelos
Base.metadata.create_all(engine)

#publicar el listado de rutas
prefix =  '/api/v1'
for bp in all_blueprints:
    print(bp)
    url_prefix=f'{prefix}/{bp.name}'
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)

if __name__ == '__main__':
    app.run(debug=True)
