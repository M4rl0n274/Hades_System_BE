from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from src.models.clientes import Clientes
from src.utils.auth import generar_token, token_required, g

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
    correo = data.get('correo', '').strip().lower()
    password = data.get('password', '')

    if not correo or not password:
        return jsonify({'message': 'Correo y contraseña son obligatorios'}), 400

    # 1. Buscar en Usuarios (Administrador, Vendedor, Usuario)
    entidad = Usuarios.get_by_email(correo)
    
    # 2. Si no existe, buscar en Clientes
    if not entidad:
        entidad = Clientes.get_by_email(correo)

    # 3. Validar credenciales
    if not entidad or not entidad.verificar_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    # 4. Generar Token usando el objeto de la entidad (ahora ambos tienen la propiedad .rol)
    token = generar_token(entidad)

    usuario_dict = entidad.to_dict()

    return jsonify({
        'access_token': token,
        'usuario': usuario_dict
    }), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    usuario_data = getattr(g, 'usuario', {})
    return jsonify(request.usuario.to_dict()), 200