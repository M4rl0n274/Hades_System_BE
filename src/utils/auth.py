from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify, g

from src.models.usuarios import Usuarios
from src.models.clientes import Clientes



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
    """Protege una ruta. Deja la instancia en request.usuario y sus datos en g.usuario."""
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

        sub_id = int(payload['sub'])
        rol_token = payload.get('rol')

        usuario = None

        # 1. Si el payload especifica el rol 'Cliente', buscar directamente en la tabla Clientes
        if rol_token == 'Cliente':
            usuario = Clientes.get_by_id(sub_id)
        else:
            # 2. Si no, buscar primero en Usuarios y como alternativa en Clientes
            usuario = Usuarios.get_by_id(sub_id)
            if not usuario:
                usuario = Clientes.get_by_id(sub_id)

        if not usuario:
            return jsonify({'message': 'Usuario o cliente no encontrado'}), 401

        # Mantiene el objeto ORM en request.usuario para retrocompatibilidad
        request.usuario = usuario

        # Asigna el diccionario en g.usuario para que g.usuario.get('rol') y g.usuario.get('id') funcionen
        if hasattr(usuario, 'to_dict'):
            g.usuario = usuario.to_dict()
        else:
            g.usuario = usuario

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