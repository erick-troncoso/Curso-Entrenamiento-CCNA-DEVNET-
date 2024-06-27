import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


def init_db():
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                otro_registro TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    otro_registro = data['otro_registro']
    password = data['password']

    password_hash = generate_password_hash(password)

    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, otro_registro, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (nombre, apellido, otro_registro, password_hash))
        conn.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre = data['nombre']
    apellido = data['apellido']
    password = data['password']

    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT password_hash FROM usuarios WHERE nombre = ? AND apellido = ?
        ''', (nombre, apellido))
        user = cursor.fetchone()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Login exitoso"}), 200
    else:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

if __name__ == '__main__':
    init_db()
    app.run(port=8500)
