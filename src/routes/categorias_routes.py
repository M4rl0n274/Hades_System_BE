from src.models.categorias import Categorias
from flask import Blueprint, request, jsonify
from src.utils.auth import token_required, rol_required

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
@token_required


def get_categorias():
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    categorias, total = Categorias.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

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





@categorias_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_categoria(id):
    categoria = Categorias.get_by_id(id)
    if categoria:
        categoria_data = {
            'id': categoria.id,
            'nombre': categoria.nombre
        }
        return jsonify(categoria_data), 200
    else:
        return jsonify({'message': 'Categoría no encontrada'}), 404

@categorias_bp.route('/', methods=['POST'])
@token_required
def create_categoria():
    data = request.get_json()
    categoria = Categorias(
        nombre=data['nombre']
    )
    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente'}), 201