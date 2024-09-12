from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde tu frontend
CORS(app, resources={r"/*": {"origins": "http://ec2-44-203-140-8.compute-1.amazonaws.com:3000"}})
# Configuración de conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='172.31.91.98',  # IP privada de tu servidor MySQL
        user='nico',          # Usuario de MySQL
        password='nicole08',  # Contraseña de MySQL
        database='USERS'      # Nombre de la base de datos
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
    cursor.execute(
        'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)',
        (nombre_usuario, correo, contrasena)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added successfully!'})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT nombre_usuario, correo FROM table1')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
