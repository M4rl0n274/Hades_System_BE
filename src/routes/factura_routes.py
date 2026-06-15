from flask import Blueprint, request, jsonify
from datetime import datetime

from src.models.factura import Factura
from src.models.detalle_factura import DetalleFactura
from src.models.productos import Productos
from src.models import session

factura_bp = Blueprint('factura', __name__)


# Obtener todas las facturas
@factura_bp.route('/', methods=['GET'])
def get_facturas():

    facturas = Factura.get()

    return jsonify([
        factura.to_dict()
        for factura in facturas
    ]), 200


# Obtener factura por ID
@factura_bp.route('/<int:id>', methods=['GET'])
def get_factura(id):

    factura = Factura.get_by_id(id)

    if not factura:
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    return jsonify(factura.to_dict()), 200


# Crear factura
@factura_bp.route('/', methods=['POST'])
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


# Eliminar factura
@factura_bp.route('/<int:id>', methods=['DELETE'])
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