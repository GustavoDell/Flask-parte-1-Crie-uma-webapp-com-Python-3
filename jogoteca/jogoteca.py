from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = "gustavo"

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario("Gusta", "Gustavo", "1234")
usuario2 = Usuario("Fulano", "Fulano", "56")

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2}

jogo1 = Jogo("Super Mario", "Ação", "SNES")
jogo2 = Jogo("Pokemon Golf", "RPG", "GBA")
jogo3 = Jogo("Mortal Kombat", "Luta", "SNES")
lista = [jogo1, jogo2, jogo3]

@app.route("/")
def index():
    return render_template('lista.html', titulo="Jogos", jogos=lista)

@app.route("/novo")
def novo():
    if("usuario_logado" not in session or session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template("novo.html", titulo="Novo Jogo")

@app.route("/criar", methods=["POST",])
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    return redirect(url_for('index'))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")#args pega os argumetos passado por query string
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST",])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id #session armazena dados do usuario por mais de um ciculo de request
            flash(usuario.nome + " logou com sucesso!")#messagem flash. Mostra a rapido a mensagem
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
        else:
            flash("Senha incorreta!")
            return redirect(url_for('login'))
    else:
        flash("Usuario não cadastrado!")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Usuario deslogado")
    return redirect(url_for('index'))

app.run(host='127.0.0.1', port=8080, debug=True)