from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify

from src.models.usuarios import Usuarios



#genera el token
def generar_token(usuario, horas=8):
    payload = {
        'sub': str(usuario.id),          # a quién pertenece el token
        'correo': usuario.correo,
        'rol': usuario.rol,
        'iat': datetime.now(timezone.utc),                          # emitido
        'exp': datetime.now(timezone.utc) + timedelta(hours=horas)  # expira
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'],
                      algorithm='HS256')

#verifica si se recibio un token y permite proteger una ruta y solicitarlo
def token_required(f):
    """Protege una ruta. Deja el usuario en request.usuario."""
    @wraps(f)
    def decorada(*args, **kwargs):
        auth = request.headers.get('Authorization', '')

        if not auth.startswith('Bearer '):
            return jsonify({'message': 'Token faltante o mal formado'}), 401

        token = auth.split(' ', 1)[1].strip()

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'],
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado, inicia sesión de nuevo'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        usuario = Usuarios.get_by_id(int(payload['sub']))
        if not usuario:
            return jsonify({'message': 'Usuario no encontrado'}), 401

        request.usuario = usuario
        return f(*args, **kwargs)

    return decorada


def rol_required(*roles):
    """Se usa después de @token_required."""
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            if request.usuario.rol not in roles:
                return jsonify({'message': 'No tienes permisos para esta acción'}), 403
            return f(*args, **kwargs)
        return decorada
    return decorador