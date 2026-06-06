from flask import Blueprint, request, jsonify
from src.models.productos import Productos


productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/', methods=['POST'])
def create_producto():
    data = request.get_json()
    producto = Productos(
        codigo=data['codigo'],
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        unidad_medida=data['unidad_medida'],
        precio=data['precio'],
        stock=data['stock'],
        id_categoria=data['id_categoria']
    )
    
    #* Validación de los datos
    try:
        float(producto.precio)
    except ValueError:
        return jsonify({'message': 'El precio del producto debe ser un número válido'}), 400
     
    if producto.nombre == '':
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    if producto.descripcion == '':
        return jsonify({'message': 'La descripción del producto es obligatoria'}), 400
    if producto.unidad_medida == '':
        return jsonify({'message': 'La unidad de medida del producto es obligatoria'}), 400
    if producto.precio <= 0:
        return jsonify({'message': 'El precio del producto debe ser mayor a cero'}), 400
    if producto.stock < 0:
        return jsonify({'message': 'El stock del producto no puede ser negativo'}), 400
    if producto.id_categoria <= 0:
        return jsonify({'message': 'La categoría del producto es obligatoria'}), 400
    
    #* Guardar el producto
    producto.save()
    return jsonify({'message': 'Producto creado exitosamente'}), 201
    
    
    
    