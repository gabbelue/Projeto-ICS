from flask import Flask, render_template, request, url_for,redirect

import sqlite3, os.path

DATABASE = 'database.db'

app = Flask(__name__)

app.config['SECRET_KEY'] = 'muitodificil'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_connection()
    aluno = conn.execute("SELECT * FROM alunos").fetchall()
    conn.close()
    return render_template('index.html',alunos=aluno)

@app.route('/dash',methods=['GET','POST'])
def dash():
    if request.method=='POST':
        nome = request.form['nome']
        mat = request.form['mat']

        conn = get_connection()
        conn.execute("INSERT INTO alunos(nome,matricula) VALUES (?,?)",(nome, mat))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('dashboard.html')

@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):

    # obter informação do usuário
    conn = get_connection()
    aluno = conn.execute('SELECT id, nome, matricula FROM alunos WHERE id == ?', (str(id))).fetchone()

    if aluno == None:
        return redirect(url_for('error', message='Usuário Inexistente'))

    if request.method == 'POST':
        nome = request.form['nome']
        mat = request.form['mat']

        conn.execute('UPDATE alunos SET nome=?, matricula=? WHERE id=?', (nome, mat, (str(id))))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('edit.html', aluno=aluno)
