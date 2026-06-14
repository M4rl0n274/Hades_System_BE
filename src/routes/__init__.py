from .productos_routes import productos_bp
from .categorias_routes import categorias_bp


# Agrupamos todos los componentes en una lista iterable
all_blueprints = [
    productos_bp,
    categorias_bp
]