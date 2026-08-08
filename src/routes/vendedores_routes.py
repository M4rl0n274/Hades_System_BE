from flask import Blueprint, request, jsonify
from src.models.vendedores import Vendedor
from src.utils.auth import token_required, rol_required

vendedores_bp = Blueprint('vendedores', __name__)

#? Obtener todos los vendedores
@vendedores_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')

def get_vendedores():
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    vendedores, total = Vendedor.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

    return jsonify({
        'data': [vendedores.to_dict() for vendedores in vendedores],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200


# def get_vendedores():
#     vendedores = Vendedor.get()
#     vendedores_list = []
#     for vendedor in vendedores:
#         vendedores_list.append({
#             'id': vendedor.id,
#             'nombre': vendedor.nombre,
#             'apellido': vendedor.apellido,
#             'documento_identidad': vendedor.documento_identidad,
#             'correo': vendedor.correo
#         })
#     return jsonify(vendedores_list), 200


#? Obtener vendedor por ID
@vendedores_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_vendedor(id):

    vendedor = Vendedor.get_by_id(id)

    if not vendedor:
        return jsonify({
            'message': 'Vendedor no encontrado'
        }), 404

    return jsonify({
        'id': vendedor.id,
        'nombre': vendedor.nombre,
        'apellido': vendedor.apellido,
        'documento_identidad': vendedor.documento_identidad,
        'correo': vendedor.correo
    }), 200


#? Crear vendedor
@vendedores_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_vendedor():

    data = request.get_json()

    campos_requeridos = [
        'nombre',
        'apellido',
        'documento_identidad',
        'correo'
    ]

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'message': f'El campo {campo} es obligatorio'
            }), 400

    if data['nombre'].strip() == '':
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if data['apellido'].strip() == '':
        return jsonify({
            'message': 'El apellido es obligatorio'
        }), 400

    if data['documento_identidad'].strip() == '':
        return jsonify({
            'message': 'El documento de identidad es obligatorio'
        }), 400

    if data['correo'].strip() == '':
        return jsonify({
            'message': 'El correo es obligatorio'
        }), 400

    vendedor = Vendedor(
        nombre=data['nombre'],
        apellido=data['apellido'],
        documento_identidad=data['documento_identidad'],
        correo=data['correo']
    )

    try:

        vendedor.save()

        return jsonify({
            'message': 'Vendedor creado exitosamente',
            'vendedor': {
                'id': vendedor.id,
                'nombre': vendedor.nombre,
                'apellido': vendedor.apellido,
                'documento_identidad': vendedor.documento_identidad,
                'correo': vendedor.correo
            }
        }), 201

    except Exception as e:

        return jsonify({
            'message': str(e)
        }), 500


#? Actualizar vendedor
@vendedores_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_vendedor(id):

    vendedor = Vendedor.get_by_id(id)

    if not vendedor:
        return jsonify({
            'message': 'Vendedor no encontrado'
        }), 404

    data = request.get_json()

    vendedor.nombre = data.get('nombre', vendedor.nombre)
    vendedor.apellido = data.get('apellido', vendedor.apellido)
    vendedor.documento_identidad = data.get(
        'documento_identidad',
        vendedor.documento_identidad
    )
    vendedor.correo = data.get(
        'correo',
        vendedor.correo
    )

    if vendedor.nombre.strip() == '':
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if vendedor.apellido.strip() == '':
        return jsonify({
            'message': 'El apellido es obligatorio'
        }), 400

    if vendedor.documento_identidad.strip() == '':
        return jsonify({
            'message': 'El documento de identidad es obligatorio'
        }), 400

    if vendedor.correo.strip() == '':
        return jsonify({
            'message': 'El correo es obligatorio'
        }), 400

    try:

        vendedor.save()

        return jsonify({
            'message': 'Vendedor actualizado exitosamente',
            'vendedor': {
                'id': vendedor.id,
                'nombre': vendedor.nombre,
                'apellido': vendedor.apellido,
                'documento_identidad': vendedor.documento_identidad,
                'correo': vendedor.correo
            }
        }), 200

    except Exception as e:

        return jsonify({
            'message': str(e)
        }), 500


#? Eliminar vendedor
@vendedores_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_vendedor(id):

    vendedor = Vendedor.get_by_id(id)

    if not vendedor:
        return jsonify({
            'message': 'Vendedor no encontrado'
        }), 404

    try:

        vendedor.delete()

        return jsonify({
            'message': 'Vendedor eliminado exitosamente'
        }), 200

    except Exception as e:

        return jsonify({
            'message': str(e)
        }), 500