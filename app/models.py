from cryptography.fernet import Fernet
from flask_login import UserMixin

FERNET_KEY = b'zX5tkR5oqA2cKA-UkB_R1yysOXtlO-DRpj8LTbf8Ag4='  # Generate with Fernet.generate_key() and set securely

# Example users (store encrypted passwords)
IN_MEMORY_USERS = {
    "user1": {
        "password": "",  # encrypted password will be set at runtime
        "role": "user",
        "name": "Regular User"
    },
    "supervisor1": {
        "password": "",  # encrypted password will be set at runtime
        "role": "supervisor",
        "name": "Supervisor"
    }
}

def set_encrypted_passwords():
    f = Fernet(FERNET_KEY)
    IN_MEMORY_USERS["user1"]["password"] = f.encrypt(b"password1").decode()
    IN_MEMORY_USERS["supervisor1"]["password"] = f.encrypt(b"supervisorpass").decode()

def load_users():
    set_encrypted_passwords()
    return IN_MEMORY_USERS.copy()

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.role = role