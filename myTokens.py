# Para usar tokens vamos a instalar > pip install PyJWT
import jwt

def createToken(data: dict):
    token: str = jwt.encode(payload=data, key='my_secret_key', algorithm='HS256')
    return token

def validateToken(token: str) -> dict:
    try:
        data = jwt.decode(token, key='my_secret', algorithms=['HS256'])
        return data
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expirado'}
    except jwt.InvalidTokenError:
        return {'error': 'Token invalido'}
    
