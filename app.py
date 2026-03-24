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

        # 🔹 DADOS DO EVENTO
        nome = request.form['nome']
        local = request.form['local']
        data = request.form['data']
        horario = request.form['horario']
        publico = request.form['publico']
        organizador = request.form['organizador']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # 🔥 SALVA EVENTO
        cursor.execute("""
            INSERT INTO evento (nome, local, data, horario, publico, organizador)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, local, data, horario, publico, organizador))

        evento_id = cursor.lastrowid

        # 🔹 DADOS DAS INTERDIÇÕES
        vias = request.form.getlist('via[]')
        trechos_inicio = request.form.getlist('trecho_inicio[]')
        trechos_fim = request.form.getlist('trecho_fim[]')
        tipos = request.form.getlist('tipo_bloqueio[]')
        horas_inicio = request.form.getlist('hora_inicio[]')
        horas_fim = request.form.getlist('hora_fim[]')
        observacoes = request.form.getlist('observacoes[]')

        # 🔥 SALVA TODAS AS INTERDIÇÕES
        for i in range(len(vias)):
            if vias[i]:  # evita salvar vazio
                cursor.execute("""
                    INSERT INTO interdicao (
                        evento_id, via, trecho_inicio, trecho_fim,
                        tipo_bloqueio, hora_inicio, hora_fim, observacoes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    evento_id,
                    vias[i],
                    trechos_inicio[i],
                    trechos_fim[i],
                    tipos[i],
                    horas_inicio[i],
                    horas_fim[i],
                    observacoes[i]
                ))

        conn.commit()
        conn.close()

        return redirect('/eventos')

    return render_template('cadastrar_evento.html')


@app.route('/eventos')
def listar_eventos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM evento
        ORDER BY id DESC
    """)  # 🔥 MAIS RECENTE PRIMEIRO

    eventos = cursor.fetchall()

    conn.close()

    return render_template('eventos.html', eventos=eventos)

@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        local = request.form['local']
        data = request.form['data']
        horario = request.form['horario']
        publico = request.form['publico']
        organizador = request.form['organizador']

        cursor.execute("""
            UPDATE evento
            SET nome=?, local=?, data=?, horario=?, publico=?, organizador=?
            WHERE id=?
        """, (nome, local, data, horario, publico, organizador, id))

        conn.commit()
        conn.close()

        return redirect('/eventos')

    cursor.execute("SELECT * FROM evento WHERE id=?", (id,))
    evento = cursor.fetchone()
    conn.close()

    return render_template('editar_evento.html', evento=evento)


@app.route('/excluir_evento/<int:id>')
def excluir_evento(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM evento WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/eventos')

@app.route('/visualizar_evento/<int:id>')
def visualizar_evento(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Evento
    cursor.execute("SELECT * FROM evento WHERE id=?", (id,))
    evento = cursor.fetchone()

    # Interdições
    cursor.execute("SELECT * FROM interdicao WHERE evento_id=?", (id,))
    interdicoes = cursor.fetchall()

    conn.close()

    return render_template(
        'visualizar_evento.html',
        evento=evento,
        interdicoes=interdicoes
    )

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