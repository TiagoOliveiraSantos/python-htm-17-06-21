import sqlite3
from flask import Flask, g, render_template, request

# Configurações

DATABASE = './flaskr.db'
SECRET_KEY = "pudim"
USERNAME = 'admin'
PASSWORD = 'admin'

# Aplicação

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before():
    g.db = connect_db()

@app.teardown_request
def after(exception):
    g.db.close()

@app.route('/')
def index():
    sql = 'SELECT titulo, texto from entradas order by id desc'
    cur = g.db.execute(sql)
    entradas = [dict(titulo=titulo, texto=texto) for titulo, texto in cur.fetchall()]
    return render_template('index.html', entradas=entradas)

@app.route('/inserir', methods=['POST'])
def inserir():
    sql = "INSERT INTO entradas(titulo, texto) values (?, ?)"
    g.db.execute(sql, [request.form['titulo'], request.form['texto']])
    g.db.commit()
    return render_template('index.html')