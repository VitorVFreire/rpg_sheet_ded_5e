import base64
from hashlib import sha256

def criptografar(senha = None):
    if senha is None:
        return None
    hash_senha = sha256(senha.encode())
    senha_digest = hash_senha.digest()
    senha_base64 = base64.b64encode(senha_digest).decode('utf-8')
    return senha_base64