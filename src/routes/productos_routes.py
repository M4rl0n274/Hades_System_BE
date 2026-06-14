from flask import Blueprint, request, jsonify
from src.models.productos import Productos


productos_bp = Blueprint('productos', __name__)

#* Obtener un producto

@productos_bp.route('/', methods=['GET'])
def get_productos():
    productos = Productos.get()
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'unidad_medida': producto.unidad_medida,
            'precio': producto.precio,
            'stock': producto.stock,
            'id_categoria': producto.id_categoria
        })
    return jsonify(productos_list), 200  

#* Obtener un producto por ID

@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto_data = {
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'unidad_medida': producto.unidad_medida,
            'precio': producto.precio,
            'stock': producto.stock,
            'id_categoria': producto.id_categoria
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404


#* Crear un producto

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
    
    #* Guardar el producto y devolver como quedo el producto en la base de datos
    producto.save()
    return jsonify({'message': 'Producto creado exitosamente','producto':producto.to_dict()}), 201
    
    
    
#* Eliminar producto 
    
@productos_bp.route('/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        producto.delete()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
@productos_bp.route('/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Productos.get_by_id(id)
    if producto:
        data = request.get_json()
        producto.codigo = data['codigo']
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.unidad_medida = data['unidad_medida']
        producto.precio = data['precio']
        producto.stock = data['stock']
        producto.id_categoria = data['id_categoria']
        producto.activo = True
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

        producto.save()        
        return jsonify({'message': 'Producto actualizado exitosamente','producto':producto.to_dict()}), 201
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404
    
    