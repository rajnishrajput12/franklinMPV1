from flask_login import UserMixin
from cryptography.fernet import Fernet
from flask import current_app

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role

def authenticate(username, password):
    users = current_app.users
    f = Fernet(current_app.config.get("FERNET_KEY", b'zX5tkR5oqA2cKA-UkB_R1yysOXtlO-DRpj8LTbf8Ag4='))
    user = users.get(username)
    if not user:
        return None
    try:
        decrypted = f.decrypt(user["password"].encode()).decode()
        if decrypted == password:
            return User(username, user["role"])
    except Exception:
        return None
    return None