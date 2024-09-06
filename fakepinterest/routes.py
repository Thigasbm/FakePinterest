# criar as rotas do site
from datetime import datetime

from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


# url_for serve pra usar o link pelo def (usado no html como variavel)

@app.route('/', methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    if formLogin.validate_on_submit(): # se preencheu o formulário e está válido:
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first() # procura pelo primeiro usuário com o login usado na validação
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formLogin.senha.data): # checa se o usuário existe. bcrypt: checa se o parametro 1 (senha hash do banco) é idêntico ao parametro 2 (senha digitada no formulario). retorna True or False
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formLogin)

@app.route('/criarconta', methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()
    if formCriarConta.validate_on_submit(): # so valida se o usuario clicar no submit
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data).decode("utf-8")
        usuario = Usuario(nickname=formCriarConta.nickname.data,
                          senha=senha,
                          email=formCriarConta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True) # loga o usuário - remember=True -> caso o usuário feche a janela e abra novamente,                                     ficará logado
        return redirect(url_for('perfil', id_usuario=usuario.id)) # passando como parametro a função, e o usuário criado
    return render_template("criar_conta.html", form=formCriarConta)

@app.route('/perfil/<id_usuario>', methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario está vendo o próprio perfil
        formFoto = FormFoto()
        if formFoto.validate_on_submit():
            arquivo = formFoto.foto.data
            nome_seguro = secure_filename(arquivo.filename) # cria um nome sem caracteres especiais para o arquivo
            # salvar o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), # caminho absoluto do arquivo original - (caminho do arquivo atual - no caso routes)
                              app.config["UPLOAD_FOLDER"],
                              nome_seguro) # pega os pedaços dos caminhos de diferentes arquivos e os junta em um caminho único
            arquivo.save(caminho)
            # registrar esse arquivo no db
            foto = Foto(img=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template('perfil.html', usuario=current_user, form=formFoto)
    else:
        # vendo o perfil de outros
        usu = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usu, form=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:50] # desc mostra a ultima foto, depois a penultima...
    return render_template('feed.html', fotos=fotos)

@app.route('/delete/<id>', methods=['POST'])
def deletarfoto(id):
    ft = Foto.query.get(id)
    if ft and ft.id_usuario == current_user.id:
        database.session.delete(ft)
        database.session.commit()
        return redirect(url_for('perfil', id_usuario=current_user.id))
    else:
        return redirect(url_for('feed'))