from flask import Blueprint, request, jsonify
from src.models.clientes import Clientes

clientes_bp = Blueprint('clientes', __name__)

#? Obtener todos los clientes
@clientes_bp.route('/', methods=['GET'])
def get_clientes():

    clientes = Clientes.get()
    clientes_list = []

    for cliente in clientes:
        clientes_list.append({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'edad': cliente.edad,
            'correo': cliente.correo,
            'documentoIdentidad': cliente.documentoIdentidad,
            'direccion': cliente.direccion,
            'telefono': cliente.telefono,
            'FechaDeNacimiento': cliente.FechaDeNacimiento
        })

    return jsonify(clientes_list), 200


#? Obtener un cliente por ID
@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):

    cliente = Clientes.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    return jsonify({
        'id': cliente.id,
        'nombre': cliente.nombre,
        'apellido': cliente.apellido,
        'edad': cliente.edad,
        'correo': cliente.correo,
        'documentoIdentidad': cliente.documentoIdentidad,
        'direccion': cliente.direccion,
        'telefono': cliente.telefono,
        'FechaDeNacimiento': cliente.FechaDeNacimiento
    }), 200


#? Crear cliente
@clientes_bp.route('/', methods=['POST'])
def create_cliente():

    data = request.get_json()

    campos_requeridos = [
        'nombre',
        'apellido',
        'edad',
        'correo',
        'documentoIdentidad',
        'direccion',
        'telefono',
        'FechaDeNacimiento'
    ]

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'message': f'El campo {campo} es obligatorio'
            }), 400

    if data['nombre'].strip() == '':
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    if data['apellido'].strip() == '':
        return jsonify({'message': 'El apellido es obligatorio'}), 400

    if int(data['edad']) <= 0:
        return jsonify({'message': 'La edad debe ser mayor a cero'}), 400

    if data['correo'].strip() == '':
        return jsonify({'message': 'El correo es obligatorio'}), 400

    if data['documentoIdentidad'].strip() == '':
        return jsonify({'message': 'El documento es obligatorio'}), 400

    if data['direccion'].strip() == '':
        return jsonify({'message': 'La dirección es obligatoria'}), 400

    if data['telefono'].strip() == '':
        return jsonify({'message': 'El teléfono es obligatorio'}), 400

    cliente = Clientes(
        nombre=data['nombre'],
        apellido=data['apellido'],
        edad=data['edad'],
        correo=data['correo'],
        documentoIdentidad=data['documentoIdentidad'],
        direccion=data['direccion'],
        telefono=data['telefono'],
        FechaDeNacimiento=data['FechaDeNacimiento']
    )

    try:
        cliente.save()

        return jsonify({
            'message': 'Cliente creado exitosamente',
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'edad': cliente.edad,
                'correo': cliente.correo,
                'documentoIdentidad': cliente.documentoIdentidad,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono,
                'FechaDeNacimiento': cliente.FechaDeNacimiento
            }
        }), 201

    except Exception as e:
        return jsonify({
            'message': str(e)
        }), 500


#? Actualizar cliente
@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):

    cliente = Clientes.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    data = request.get_json()

    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.apellido = data.get('apellido', cliente.apellido)
    cliente.edad = data.get('edad', cliente.edad)
    cliente.correo = data.get('correo', cliente.correo)
    cliente.documentoIdentidad = data.get(
        'documentoIdentidad',
        cliente.documentoIdentidad
    )
    cliente.direccion = data.get(
        'direccion',
        cliente.direccion
    )
    cliente.telefono = data.get(
        'telefono',
        cliente.telefono
    )
    cliente.FechaDeNacimiento = data.get(
        'FechaDeNacimiento',
        cliente.FechaDeNacimiento
    )

    if cliente.nombre.strip() == '':
        return jsonify({'message': 'El nombre es obligatorio'}), 400

    if cliente.apellido.strip() == '':
        return jsonify({'message': 'El apellido es obligatorio'}), 400

    if int(cliente.edad) <= 0:
        return jsonify({'message': 'La edad debe ser mayor a cero'}), 400

    try:
        cliente.save()

        return jsonify({
            'message': 'Cliente actualizado exitosamente',
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'edad': cliente.edad,
                'correo': cliente.correo,
                'documentoIdentidad': cliente.documentoIdentidad,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono,
                'FechaDeNacimiento': cliente.FechaDeNacimiento
            }
        }), 200

    except Exception as e:
        return jsonify({
            'message': str(e)
        }), 500


#? Eliminar cliente
@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):

    cliente = Clientes.get_by_id(id)

    if not cliente:
        return jsonify({
            'message': 'Cliente no encontrado'
        }), 404

    try:
        cliente.delete()

        return jsonify({
            'message': 'Cliente eliminado exitosamente'
        }), 200

    except Exception as e:
        return jsonify({
            'message': str(e)
        }), 500