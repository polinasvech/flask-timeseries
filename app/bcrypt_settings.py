from flask import current_app as app
from flask_bcrypt import Bcrypt

# для шифрования паролей
bcrypt = Bcrypt(app)
