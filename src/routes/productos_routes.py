from flask import Blueprint, request, jsonify
from src.models.productos import Productos
from src.utils.auth import token_required, rol_required


productos_bp = Blueprint('productos', __name__)

#? Obtener todos los producto
@productos_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador', 'Vendedor')

def get_productos():
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    productos, total = Productos.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

    return jsonify({
        'data': [productos.to_dict() for productos in productos],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200


# def get_productos():
#     productos = Productos.get()
#     productos_list = []
#     for producto in productos:
#         productos_list.append({
#             'id': producto.id,
#             'id_categoria': producto.id_categoria,
#             'nombre_producto': producto.nombre_producto,
#             'descripcion': producto.descripcion,
#             'valor_unitario': producto.valor_unitario,
#             'stock': producto.stock,
#             'codigo': producto.codigo
#         })
#     return jsonify(productos_list), 200



#? Obtener un producto por ID
@productos_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador', 'Vendedor')
def get_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto_data = {
            'id': producto.id,
            'id_categoria': producto.id_categoria,
            'nombre_producto': producto.nombre_producto,
            'descripcion': producto.descripcion,
            'valor_unitario': producto.valor_unitario,
            'stock': producto.stock,
            'codigo': producto.codigo,
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

#? Crear un producto
@productos_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_producto():
    data = request.get_json()
    producto = Productos(
        id_categoria=data['id_categoria'],
        nombre_producto=data['nombre_producto'],
        descripcion=data['descripcion'],
        valor_unitario=data['valor_unitario'],
        stock=data['stock'],
        codigo=data['codigo']
    )
    #* Validación de los datos
    try:
        float(producto.valor_unitario)
    except ValueError:
        return jsonify({'message': 'El precio del producto debe ser un número válido'}), 400
     
    if producto.nombre_producto == '':
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    if producto.descripcion == '':
        return jsonify({'message': 'La descripción del producto es obligatoria'}), 400
    if producto.valor_unitario <= 0:
        return jsonify({'message': 'El precio del producto debe ser mayor a cero'}), 400
    if producto.stock < 0:
        return jsonify({'message': 'El stock del producto no puede ser negativo'}), 400
    if producto.id_categoria <= 0:
        return jsonify({'message': 'La categoría del producto es obligatoria'}), 400
    #* Guardar el producto y devolver como quedo el producto en la base de datos
    producto.save()
    return jsonify({'message': 'Producto creado exitosamente','producto':producto.to_dict()}), 201
 
#? Eliminar un producto
@productos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto.delete()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
#? editar un producto
@productos_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        data = request.get_json()
        producto.id_categoria = data['id_categoria']
        producto.nombre_producto = data['nombre_producto']
        producto.descripcion = data['descripcion']
        producto.valor_unitario = data['valor_unitario']
        producto.stock = data['stock']
        producto.codigo = data['codigo']
        
        try:
            float(producto.valor_unitario)
        except ValueError:
            return jsonify({'message': 'El precio del producto debe ser un número válido'}), 400
         
        if producto.nombre_producto == '':
            return jsonify({'message': 'El nombre_producto del producto es obligatorio'}), 400
        if producto.descripcion == '':
            return jsonify({'message': 'La descripción del producto es obligatoria'}), 400
        if producto.valor_unitario <= 0:
            return jsonify({'message': 'El valor_unitario del producto debe ser mayor a cero'}), 400
        if producto.stock < 0:
            return jsonify({'message': 'El stock del producto no puede ser negativo'}), 400
        if producto.id_categoria <= 0:
            return jsonify({'message': 'La categoría del producto es obligatoria'}), 400
        

    
        producto.save()        
        return jsonify({'message': 'Producto actualizado exitosamente','producto':producto.to_dict()}), 201
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404