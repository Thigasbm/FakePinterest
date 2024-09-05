# criar o aplicativo

from flask import Flask # primeiro importa e cria o que precisa
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)

# Verifica se o ambiente é de desenvolvimento ou produção
if os.getenv("DEBUG") == 0: # '0' como string, pois getenv retorna strings
    link_banco = os.getenv("DATABASE_URL")
else:
    link_banco = "sqlite:///comunidade.db"
app.config["SQLALCHEMY_DATABASE_URI"] = link_banco
app.config["SECRET_KEY"] = "f7d51183b5b7ec5005c5d66d9fa887f4"
app.config["UPLOAD_FOLDER"] = "static/fotos_post"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes # depois importa as rotas
