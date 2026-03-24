from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM evento")
    eventos = cursor.fetchall()

    conn.close()

    return render_template('index.html', eventos=eventos)

from flask import request, redirect

@app.route('/cadastrar_evento', methods=['GET', 'POST'])
def cadastrar_evento():
    if request.method == 'POST':
        nome = request.form['nome']
        local = request.form['local']
        data = request.form['data']
        horario = request.form['horario']
        publico = request.form['publico']
        organizador = request.form['organizador']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO evento (nome, local, data, horario, publico, organizador)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, local, data, horario, publico, organizador))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('cadastrar_evento.html')

@app.route('/cadastrar_interdicao', methods=['GET', 'POST'])
def cadastrar_interdicao():
    if request.method == 'POST':
        evento_id = request.form['evento_id']
        via = request.form['via']
        trecho_inicio = request.form['trecho_inicio']
        trecho_fim = request.form['trecho_fim']
        tipo_bloqueio = request.form['tipo_bloqueio']
        hora_inicio = request.form['hora_inicio']
        hora_fim = request.form['hora_fim']
        observacoes = request.form['observacoes']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO interdicao (
                evento_id, via, trecho_inicio, trecho_fim,
                tipo_bloqueio, hora_inicio, hora_fim, observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (evento_id, via, trecho_inicio, trecho_fim,
              tipo_bloqueio, hora_inicio, hora_fim, observacoes))

        conn.commit()
        conn.close()

        return redirect('/')

    # buscar eventos para dropdown
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM evento")
    eventos = cursor.fetchall()
    conn.close()

    return render_template('cadastrar_interdicao.html', eventos=eventos)

import sqlite3

def criar_banco():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interdicao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        via TEXT,
        trecho_inicio TEXT,
        trecho_fim TEXT,
        tipo_bloqueio TEXT,
        hora_inicio TEXT,
        hora_fim TEXT,
        observacoes TEXT
    )
""")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)