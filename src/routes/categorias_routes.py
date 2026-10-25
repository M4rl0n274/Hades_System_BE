from flask import Blueprint, request, jsonify
from src.models.categorias import Categorias
from src.utils.auth import token_required, rol_required

categorias_bp = Blueprint('categorias', __name__)

#? 1. Obtener todas (Funciona)
@categorias_bp.route('/', methods=['GET'])
# @token_required
def get_categorias():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    categorias, total = Categorias.paginate(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page 

    return jsonify({
        'data': [categoria.to_dict() for categoria in categorias],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200


#? 2. Cargar para Editar (Corregido: Usa nombre_categoria)
@categorias_bp.route('/', methods=['GET'])
# @token_required
def get_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404
        
    return jsonify({
        'id': categoria.id,
        'nombre': categoria.nombre_categoria  # El backend lo extrae del modelo
    }), 200


#? 3. Crear (Corregido: El controlador envía 'nombre', el modelo guarda 'nombre_categoria')
@categorias_bp.route('/', methods=['POST'])
# @token_required
def create_categoria():
    data = request.get_json()
# 1. Verificar si data existe y contiene la clave 'nombre_categoria'
    if not data or 'nombre_categoria' not in data:
        return jsonify({'message': 'Datos incompletos'}), 400

    # 2. Limpiar espacios en blanco al inicio y final
    nombre = str(data['nombre_categoria']).strip()

    # 3. Validar que no esté vacío después del strip
    if not nombre:
        return jsonify({'message': 'El nombre de la categoría no puede estar vacío'}), 400

    # 4. (Opcional) Validar longitud mínima
    if len(nombre) < 3:
        return jsonify({'message': 'El nombre debe tener al menos 3 caracteres'}), 400

    categoria = Categorias(
        nombre_categoria=nombre
    )
    categoria.save()

    return jsonify({
        'message': 'Categoría creada exitosamente',
        'categorias': [categoria.to_dict()]
    }), 201


#? 4. Actualizar / Editar (Ruta que faltaba)
@categorias_bp.route('/', methods=['PUT'])
# @token_required
def update_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    data = request.get_json()
    if data and 'nombre' in data:
        categoria.nombre_categoria = data['nombre'].strip()
        categoria.save()
        return jsonify({'message': 'Categoría actualizada exitosamente'}), 200
        
    return jsonify({'message': 'No se enviaron datos para actualizar'}), 400


#? 5. Eliminar (Corregido: Faltaba el / en la URL)
@categorias_bp.route('/', methods=['DELETE'])
# @token_required
def delete_categoria(id):
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    try:
        categoria.delete()
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': f'Error de base de datos: {str(e)}'}), 400