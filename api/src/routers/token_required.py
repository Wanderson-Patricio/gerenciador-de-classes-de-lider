from functools import wraps
from flask import g, request, jsonify
from ..errors import TokenMissingError

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-api-token')
        if not token:
            return jsonify(TokenMissingError("GitHub API token must be provided when requested by API.").send_error()), 401
        
        # Opcional: Você pode instanciar o manager aqui e guardar no 'g'
        g.token = token
        return f(*args, **kwargs)
    return decorated

