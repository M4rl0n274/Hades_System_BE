from .productos_routes import productos_bp
from .categorias_routes import categorias_bp
from .clientes_routes import clientes_bp
from .auth_routes import auth_bp


# Agrupamos todos los componentes en una lista iterable
all_blueprints = [
    productos_bp,
    categorias_bp,
    clientes_bp,
    auth_bp
]

