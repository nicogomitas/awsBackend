import os
import sqlite3  # Asegúrate de importar sqlite3
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde tu frontend
CORS(app, resources={r"/*": {"origins": "http://ec2-18-205-177-229.compute-1.amazonaws.com:3000"}})

def get_db_connection():
    if os.getenv('FLASK_ENV') == 'testing':
        # Usar SQLite en memoria para pruebas
        return sqlite3.connect(':memory:')
    else:
        # Conectar a MySQL para producción
        return mysql.connector.connect(
            host='172.31.91.98',
            user='nico',
            password='nicole08',
            database='USERS'
        )

@app.before_first_request
def setup_database():
    if 'test' in app.config['ENV']:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS table1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT,
                correo TEXT,
                contrasena TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)',
            (nombre_usuario, correo, contrasena)
        )
        conn.commit()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to add user'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nombre_usuario, correo FROM table1')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)


