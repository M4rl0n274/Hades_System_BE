from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from src.utils.auth import generar_token, token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    # 1. Validar campos obligatorios
    for campo in ('nombre', 'apellido', 'correo', 'password', 'documento_identidad', 'rol'):
        if not data.get(campo):
            return jsonify({'message': f'El campo {campo} es obligatorio'}), 400

    # 2. Validar longitud de la contraseña
    if len(data['password']) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    # 3. Validar correo duplicado
    if Usuarios.get_by_email(data['correo']):
        return jsonify({'message': 'Ese correo ya está registrado'}), 409

    # 4. Validar documento duplicado (Responde mensaje específico en Postman)
    if Usuarios.get_by_documento(data['documento_identidad']):
        return jsonify({'message': 'Ese documento de identidad ya está registrado'}), 409

    # 5. Instanciar usuario
    usuario = Usuarios(
        nombre=data['nombre'],
        apellido=data['apellido'],
        correo=data['correo'],
        password=data['password'],
        documento_identidad=data['documento_identidad'],
        rol=data.get('rol', 'usuario')
    )

    # 6. Intentar guardar
    try:
        usuario.save()
    except Exception:
        return jsonify({'message': 'Error al registrar el usuario en la base de datos'}), 500

    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    correo = data.get('correo')
    password = data.get('password')

    if not correo or not password:
        return jsonify({'message': 'Correo y contraseña son obligatorios'}), 400

    usuario = Usuarios.get_by_email(correo)

    # mismo mensaje en ambos casos: no le regales al atacante
    # la información de qué correos existen
    if not usuario or not usuario.verificar_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    return jsonify({
        'access_token': generar_token(usuario),
        'token_type': 'Bearer',
        'expires_in': 28800,
        'usuario': usuario.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    return jsonify(request.usuario.to_dict()), 200