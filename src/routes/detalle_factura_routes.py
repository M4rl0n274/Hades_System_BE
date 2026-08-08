from flask import Blueprint, jsonify, request
from src.models.detalle_factura import DetalleFactura
from src.models import session
from src.utils.auth import token_required, rol_required

detalle_factura_bp = Blueprint(
    'detalle_factura',
    __name__
)

#? Obtener todos los detalles
@detalle_factura_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador', 'Vendedor')

def get_detalleFactura():
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    detalleFactura, total = DetalleFactura.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

    return jsonify({
        'data': [detalleFactura.to_dict() for detalleFactura in detalleFactura],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200







# def get_detalles():
#     detalles = DetalleFactura.get()
#     return jsonify([
#         detalle.to_dict()
#         for detalle in detalles
#     ]), 200


#? Obtener detalle por ID
@detalle_factura_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador', 'Vendedor')
def get_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if not detalle:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    return jsonify(detalle.to_dict()), 200


#? Actualizar detalle
@detalle_factura_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador', 'Vendedor')
def update_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if not detalle:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    data = request.get_json()

    try:

        cantidad = int(data['cantidad'])

        if cantidad <= 0:
            return jsonify({
                'message': 'Cantidad inválida'
            }), 400

        precio = float(data['precio_unitario'])

        if precio <= 0:
            return jsonify({
                'message': 'Precio inválido'
            }), 400

        detalle.cantidad = cantidad
        detalle.precio_unitario = precio
        detalle.subtotal_producto = cantidad * precio

        session.commit()

        return jsonify({
            'message': 'Detalle actualizado',
            'detalle': detalle.to_dict()
        }), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 500


#? Eliminar detalle
@detalle_factura_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if not detalle:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    try:

        detalle.delete()

        return jsonify({
            'message': 'Detalle eliminado correctamente'
        }), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 500