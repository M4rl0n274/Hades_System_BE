from flask import Blueprint, request, jsonify

from src.models.usuarios import Usuarios
from src.utils.auth import generar_token, token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    for campo in ('email', 'password', 'nombre'):
        if not data.get(campo):
            return jsonify({'message': f'El campo {campo} es obligatorio'}), 400

    if len(data['password']) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    if Usuarios.get_by_email(data['email']):
        return jsonify({'message': 'Ese correo ya está registrado'}), 409

    usuario = Usuarios(
        email=data['email'],
        password=data['password'],
        nombre=data['nombre'],
        rol=data.get('rol', 'usuario')
    )
    usuario.save()

    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Correo y contraseña son obligatorios'}), 400

    usuario = Usuarios.get_by_email(email)

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