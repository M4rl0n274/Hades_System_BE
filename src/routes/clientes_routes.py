from src.models.clientes import Clientes
from flask import Blueprint, request, jsonify
from src.utils.auth import token_required

clientes_bp = Blueprint('clientes', __name__)

# Obtener todos los clientes
@clientes_bp.route('/', methods=['GET'])
#decorado (@) para solicitar el jwt
@token_required
def get_clientes():
    
    #paginación
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=100, type=int)

    clientes, total = Clientes.paginate(page=page, per_page=per_page)

    total_pages = (total + per_page - 1) // per_page  # Calcular el número total de páginas

    return jsonify({
        'data': [cliente.to_dict() for cliente in clientes],
        'meta' : {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200
    
    
    # clientes = Clientes.get()
    # clientes_list = []

    # for cliente in clientes:
    #     clientes_list.append({
    #         'id': cliente.id,
    #         'documento': cliente.documento,
    #         'nombre': cliente.nombre,
    #         'direccion': cliente.direccion,
    #         'telefono': cliente.telefono,
    #         'email': cliente.email
    #     })

    # return jsonify(clientes_list), 200


# Obtener un cliente por ID
@clientes_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_cliente(id):
    cliente = Clientes.get_by_id(id)

    if cliente:
        cliente_data = {
            'id': cliente.id,
            'documento': cliente.documento,
            'nombre': cliente.nombre,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'email': cliente.email
        }

        return jsonify(cliente_data), 200

    else:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404


# Crear cliente
@clientes_bp.route('/', methods=['POST'])
@token_required
def create_cliente():

    data = request.get_json()

    cliente = Clientes(
        documento=data['documento'],
        nombre=data['nombre'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        email=data['email']
    )

    # Validaciones
    if cliente.documento == "":
        return jsonify({
            'message': 'El documento es obligatorio'
        }), 400

    if cliente.nombre == "":
        return jsonify({
            'message': 'El nombre es obligatorio'
        }), 400

    if cliente.direccion == "":
        return jsonify({
            'message': 'La dirección es obligatoria'
        }), 400

    if cliente.telefono == "":
        return jsonify({
            'message': 'El teléfono es obligatorio'
        }), 400

    if cliente.email == "":
        return jsonify({
            'message': 'El correo es obligatorio'
        }), 400

    cliente.save()

    return jsonify({
        'message': 'Cliente creado exitosamente'
    }), 201


# Actualizar cliente
@clientes_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente:

        data = request.get_json()

        cliente.documento = data['documento']
        cliente.nombre = data['nombre']
        cliente.direccion = data['direccion']
        cliente.telefono = data['telefono']
        cliente.email = data['email']

        # Validaciones
        if cliente.documento == "":
            return jsonify({
                'message': 'El documento es obligatorio'
            }), 400

        if cliente.nombre == "":
            return jsonify({
                'message': 'El nombre es obligatorio'
            }), 400

        if cliente.direccion == "":
            return jsonify({
                'message': 'La dirección es obligatoria'
            }), 400

        if cliente.telefono == "":
            return jsonify({
                'message': 'El teléfono es obligatorio'
            }), 400

        if cliente.email == "":
            return jsonify({
                'message': 'El correo es obligatorio'
            }), 400

        cliente.save()

        return jsonify({
            'message': 'Cliente actualizado exitosamente'
        }), 200

    else:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404


# Eliminar cliente
@clientes_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(id):

    cliente = Clientes.get_by_id(id)

    if cliente:

        cliente.delete()

        return jsonify({
            'message': 'Cliente eliminado exitosamente'
        }), 200

    else:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404