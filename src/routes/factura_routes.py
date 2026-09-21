from flask import Blueprint, request, jsonify,g
from datetime import datetime
from sqlalchemy import text

from src.models.factura import Factura
from src.models.detalle_factura import DetalleFactura
from src.models.productos import Productos
from src.models import session
from src.utils.auth import token_required, rol_required

factura_bp = Blueprint('factura', __name__)


#? Obtener todas las facturas
@factura_bp.route('/', methods=['GET'])
@token_required
def get_factura():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    q = request.args.get('q', '').strip()
    id_cliente = request.args.get('id_cliente', type=int)

    # Lectura segura del usuario almacenado en 'g'
    usuario_actual = getattr(g, 'usuario', {}) or {}
    
    # Manejar si es un diccionario o una instancia de modelo
    rol = usuario_actual.get('rol') if isinstance(usuario_actual, dict) else getattr(usuario_actual, 'rol', None)
    user_id = usuario_actual.get('id') if isinstance(usuario_actual, dict) else getattr(usuario_actual, 'id', None)

    # Control de seguridad: Si es Cliente, forzar a consultar solo sus facturas
    if rol == 'Cliente':
        id_cliente = user_id

    # Resto de tu lógica de consulta y paginación...
    factura, total = Factura.paginate(page=page, per_page=per_page, id_cliente=id_cliente, q=q)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    facturas_list = []
    for f in factura:
        f_dict = f.to_dict()
        
        cliente = session.execute(
            text("SELECT nombre, apellido FROM clientes WHERE id = :id"), 
            {"id": f.id_cliente}
        ).fetchone()
        f_dict['cliente_nombre'] = f"{cliente[0]} {cliente[1]}" if cliente else "Desconocido"
        
        vendedor = session.execute(
            text("SELECT nombre, apellido FROM vendedores WHERE id = :id"), 
            {"id": f.id_vendedor}
        ).fetchone()
        f_dict['vendedor_nombre'] = f"{vendedor[0]} {vendedor[1]}" if vendedor else "Desconocido"
        
        usuario = session.execute(
            text("SELECT nombre, apellido FROM usuarios WHERE id = :id"), 
            {"id": f.id_usuario}
        ).fetchone()
        f_dict['usuario_nombre'] = f"{usuario[0]} {usuario[1]}" if usuario else "Desconocido"
        
        facturas_list.append(f_dict)

    return jsonify({
        'data': facturas_list,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200


#? Obtener factura por ID
@factura_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador', 'Vendedor')
def get_facturas(id):
    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({'message': 'Factura no encontrada'}), 404

    factura_data = factura.to_dict()
    
    # Encabezado (Nombres)
    cliente = session.execute(text("SELECT nombre, apellido FROM clientes WHERE id = :id"), {"id": factura.id_cliente}).fetchone()
    factura_data['cliente_nombre'] = f"{cliente[0]} {cliente[1]}" if cliente else "Desconocido"
    
    vendedor = session.execute(text("SELECT nombre, apellido FROM vendedores WHERE id = :id"), {"id": factura.id_vendedor}).fetchone()
    factura_data['vendedor_nombre'] = f"{vendedor[0]} {vendedor[1]}" if vendedor else "Desconocido"
    
    usuario = session.execute(text("SELECT nombre, apellido FROM usuarios WHERE id = :id"), {"id": factura.id_usuario}).fetchone()
    factura_data['usuario_nombre'] = f"{usuario[0]} {usuario[1]}" if usuario else "Desconocido"

    # Detalles con nombres de producto
    try:
        detalles = session.query(DetalleFactura).filter_by(id_factura=id).all()
        detalles_list = []
        for d in detalles:
            d_dict = d.to_dict()
            prod = session.execute(text("SELECT nombre_producto FROM productos WHERE id = :id"), {"id": d.id_producto}).fetchone()
            d_dict['producto_nombre'] = prod[0] if prod else "Desconocido"
            detalles_list.append(d_dict)
        factura_data['detalles'] = detalles_list
    except Exception as e:
        factura_data['detalles'] = []

    return jsonify(factura_data), 200


#? Actualizar encabezado de factura
@factura_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_factura(id):
    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    data = request.get_json()

    try:
        # Actualizamos solo los datos del encabezado. 
        # Los totales y productos se modifican desde detalle_factura_routes.py
        factura.id_cliente = data.get('id_cliente', factura.id_cliente)
        factura.id_vendedor = data.get('id_vendedor', factura.id_vendedor)
        factura.id_usuario = data.get('id_usuario', factura.id_usuario)

        session.commit()

        return jsonify({
            'message': 'Factura actualizada exitosamente',
            'factura': factura.to_dict()
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            'message': str(e)
        }), 500



#? Crear factura
@factura_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador', 'Vendedor')
def create_factura():

    data = request.get_json()

    detalle = data.get('detalle')

    if not detalle:
        return jsonify({
            'message': 'Debe enviar al menos un producto'
        }), 400

    subtotal = 0
    detalles_guardar = []

    for item in detalle:

        producto = Productos.get_by_id(item['id_producto'])

        if not producto:
            return jsonify({
                'message': f"Producto {item['id_producto']} no existe"
            }), 404

        cantidad = int(item['cantidad'])

        if cantidad <= 0:
            return jsonify({
                'message': 'La cantidad debe ser mayor a cero'
            }), 400

        if producto.stock < cantidad:
            return jsonify({
                'message': f'Stock insuficiente para {producto.nombre_producto}'
            }), 400

        precio = float(producto.valor_unitario)

        subtotal_producto = precio * cantidad

        subtotal += subtotal_producto

        detalles_guardar.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': subtotal_producto
        })

    iva = subtotal * 0.19
    total = subtotal + iva

    try:

        factura = Factura(
            id_cliente=data['id_cliente'],
            id_vendedor=data['id_vendedor'],
            id_usuario=data['id_usuario'],
            fecha_factura=datetime.now(),
            subtotal=subtotal,
            iva=iva,
            total=total
        )

        session.add(factura)
        session.flush()

        for item in detalles_guardar:

            detalle_factura = DetalleFactura(
                id_factura=factura.id,
                id_producto=item['producto'].id,
                cantidad=item['cantidad'],
                precio_unitario=item['precio'],
                subtotal_producto=item['subtotal']
            )

            session.add(detalle_factura)

            item['producto'].stock -= item['cantidad']

        session.commit()

        return jsonify({
            'message': 'Factura creada exitosamente',
            'factura': factura.to_dict()
        }), 201

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 500


#? Eliminar factura
@factura_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_factura(id):

    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    try:

        factura.delete()

        return jsonify({
            'message': 'Factura eliminada correctamente'
        }), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 500