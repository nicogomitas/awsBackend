import os
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde tu frontend
CORS(app, resources={r"/*": {"origins": "http://ec2-18-205-177-229.compute-1.amazonaws.com:3000"}})

# Configuración de conexión a la base de datos
def get_db_connection():
    if os.getenv('FLASK_ENV') == 'testing':
        raise RuntimeError("In test environment, use a different script to handle database operations")
    else:
        return mysql.connector.connect(
            host='172.31.91.98',
            user='nico',
            password='nicole08',
            database='USERS'
        )

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
