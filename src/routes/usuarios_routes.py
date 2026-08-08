from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from sqlalchemy.exc import IntegrityError
from src.utils.auth import token_required, rol_required

usuarios_bp = Blueprint('usuarios', __name__)

#? Obtener usuarios
@usuarios_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')

def get_usuarios():
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)

    usuarios, total = Usuarios.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

    return jsonify({
        'data': [usuarios.to_dict() for usuarios in usuarios],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200



# def get_usuarios():
#     usuarios = Usuarios.get()
#     usuarios_list = []
#     for usuario in usuarios:
#         usuarios_list.append({
#             'id': usuario.id,
#             'nombre': usuario.nombre,
#             'apellido': usuario.apellido,
#             'correo': usuario.correo,
#             'documento_identidad': usuario.documento_identidad,
#             'rol': usuario.rol
#         })
#     return jsonify(usuarios_list), 200

#? Obtener usuarios por ID
@usuarios_bp.route('/<int:id>', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if usuario:
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'correo': usuario.correo,
            'documento_identidad': usuario.documento_identidad,
            'rol': usuario.rol
        }), 200

    return jsonify({
        'message': 'Usuario no encontrado'
    }), 404
    
#?  Crear Usuario
@usuarios_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_usuario():

    data = request.get_json()

    campos_requeridos = [
        'nombre',
        'apellido',
        'correo',
        'password',
        'documento_identidad',
        'rol'
    ]

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'message': f'El campo {campo} es obligatorio'
            }), 400

    usuario = Usuarios(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo=data['correo'],
        password=data['password'],
        documento_identidad=data['documento_identidad'],
        rol=data['rol']
    )

    if usuario.nombre.strip() == '':
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    if usuario.apellido.strip() == '':
        return jsonify({'message': 'El apellido es obligatorio'}), 400

    if usuario.correo.strip() == '':
        return jsonify({'message': 'El correo es obligatorio'}), 400

    if usuario.password.strip() == '':
        return jsonify({'message': 'La contraseña es obligatoria'}), 400

    if usuario.documento_identidad.strip() == '':
        return jsonify({'message': 'El documento es obligatorio'}), 400

    if usuario.rol.strip() == '':
        return jsonify({'message': 'El rol es obligatorio'}), 400

    try:
        usuario.save()

        return jsonify({
            'message': 'Usuario creado exitosamente'
        }), 201

    except IntegrityError:
        return jsonify({
            'message': 'El correo o documento ya existen'
        }), 400
        
#? Actualizar usuario
@usuarios_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if not usuario:
        return jsonify({
            'message': 'Usuario no encontrado'
        }), 404

    data = request.get_json()

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.correo = data.get('correo', usuario.correo)
    usuario.password = data.get('password', usuario.password)
    usuario.documento_identidad = data.get('documento_identidad',usuario.documento_identidad)
    usuario.rol = data.get('rol', usuario.rol)

    try:
        usuario.save()

        return jsonify({
            'message': 'Usuario actualizado exitosamente'
        }), 200

    except IntegrityError:
        return jsonify({
            'message': 'El correo o documento ya existen'
        }), 400
        
#? Eliminar usuario
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_usuario(id):

    usuario = Usuarios.get_by_id(id)

    if not usuario:
        return jsonify({
            'message': 'Usuario no encontrado'
        }), 404

    usuario.delete()

    return jsonify({
        'message': 'Usuario eliminado exitosamente'
    }), 200

