from src.models.categorias import Categorias
from flask import Blueprint, request, jsonify

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])

def get_categorias():
    categorias = Categorias.get()
    categorias_list = []
    for categoria in categorias:
        categorias_list.append({
            'id': categoria.id,
            'nombre': categoria.nombre
        })
    return jsonify(categorias_list), 200

@categorias_bp.route('/<int:id>', methods=['GET'])
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
def create_categoria():
    data = request.get_json()
    categoria = Categorias(
        nombre=data['nombre']
    )
    categoria.save()
    return jsonify({'message': 'Categoría creada exitosamente'}), 201