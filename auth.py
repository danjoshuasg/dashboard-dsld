from flask_login import UserMixin
from app import login_manager
from dotenv import load_dotenv
load_dotenv()

# Clase de usuario para manejo de usuarios con Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Función de carga de usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Aquí puedes cargar el usuario desde una base de datos u otro almacenamiento
    if user_id in users:
        return User(user_id)
    return None

# Simulación de autenticación (en un caso real, esto sería una base de datos)
users = {
    'admin': {'password': 'admin'}
}

def authenticate(username, password):
    """
    Verifica las credenciales del usuario.
    """
    if username in users and users[username]['password'] == password:
        return User(username)
    return None