from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

with app.app_context():
    database.create_all()

    # para criar no Render, usa a chave externa no app.config["SQLALCHEMY_DATABASE_URI"] = "chave_externa"
    # e então roda esse arquivo