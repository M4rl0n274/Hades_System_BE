from .productos_routes import productos_bp
from .categorias_routes import categorias_bp
from .factura_routes import factura_bp
from .detalle_factura_routes import detalle_factura_bp
from .clientes_routes import clientes_bp  
from .usuarios_routes import usuarios_bp  



# Agrupamos todos los componentes en una lista iterable
all_blueprints = [
    productos_bp,
    categorias_bp,
    factura_bp,
    detalle_factura_bp,
    clientes_bp,
    usuarios_bp
]