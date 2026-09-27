from flask import Blueprint, jsonify, request
from src.models.detalle_factura import DetalleFactura
from src.models.factura import Factura
from src.models import session
from src.utils.auth import token_required, rol_required

detalle_factura_bp = Blueprint(
    'detalle_factura',
    __name__
)


def _recalcular_totales_factura(id_factura):
    """Recalcula subtotal, iva y total de una factura a partir de la suma
    de los subtotal_producto de todos sus detalles, y los persiste."""
    detalles = session.query(DetalleFactura).filter_by(id_factura=id_factura).all()

    subtotal = sum(float(d.subtotal_producto) for d in detalles)
    iva = subtotal * 0.19
    total = subtotal + iva

    factura = Factura.get_by_id(id_factura)
    if factura:
        factura.subtotal = subtotal
        factura.iva = iva
        factura.total = total


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

        #* El precio no se toma del cliente (evita manipulación desde el navegador):
        #* se conserva el precio_unitario ya guardado en el detalle.
        detalle.cantidad = cantidad
        detalle.subtotal_producto = cantidad * float(detalle.precio_unitario)

        #* Recalcular y persistir los totales de la factura padre
        _recalcular_totales_factura(detalle.id_factura)

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

        id_factura = detalle.id_factura

        detalle.delete()

        #* Recalcular y persistir los totales de la factura padre
        _recalcular_totales_factura(id_factura)

        session.commit()

        return jsonify({
            'message': 'Detalle eliminado correctamente'
        }), 200

    except Exception as e:

        session.rollback()

        return jsonify({
            'message': str(e)
        }), 500