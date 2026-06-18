from flask import Blueprint, jsonify, request

from src.models.detalle_factura import DetalleFactura
from src.models import session

detalle_factura_bp = Blueprint(
    'detalle_factura',
    __name__
)

#? Obtener todos los detalles
@detalle_factura_bp.route('/', methods=['GET'])
def get_detalles():

    detalles = DetalleFactura.get()

    return jsonify([
        detalle.to_dict()
        for detalle in detalles
    ]), 200


#? Obtener detalle por ID
@detalle_factura_bp.route('/<int:id>', methods=['GET'])
def get_detalle(id):

    detalle = DetalleFactura.get_by_id(id)

    if not detalle:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    return jsonify(detalle.to_dict()), 200


#? Actualizar detalle
@detalle_factura_bp.route('/<int:id>', methods=['PUT'])
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