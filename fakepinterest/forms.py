# criar os formulários do site
from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Logar")
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("O usuário informado não está cadastrado")
    # falta validar a senha





class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(4, 30)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")]) # , EqualTo("senha")
    nickname = StringField("Apelido", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Cadastrar-se")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar")
    def validate_nickname(self, nickname):
        nick = Usuario.query.filter_by(nickname=nickname.data).first()
        if nick:
            raise ValidationError("Apelido de usuário já existe")


class FormFoto(FlaskForm):
    foto = FileField("foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")