import os
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import unittest

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde tu frontend
CORS(app, resources={r"/*": {"origins": "http://ec2-18-205-177-229.compute-1.amazonaws.com:3000"}})

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
    try:
        if os.getenv('FLASK_ENV') == 'testing':
            cursor.execute(
                'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)',
                (nombre_usuario, correo, contrasena)
            )
        else:
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
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT nombre_usuario, correo FROM table1')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura la app para pruebas
        os.environ['FLASK_ENV'] = 'testing'
        self.app = app.test_client()
        self.app.testing = True

        # Crear la tabla en SQLite en memoria
        self.conn = get_db_connection()
        cursor = self.conn.cursor()

        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS table1 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                nombre_usuario TEXT NOT NULL,
                correo TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        cursor.close()

    def tearDown(self):
        # Cerrar la conexión después de cada prueba
        self.conn.close()

    def test_add_user(self):
        # Probar la adición de un usuario
        response = self.app.post('/add_user', json={
            'nombre_usuario': 'testuser',
            'correo': 'testuser@example.com',
            'contrasena': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

    def test_get_users(self):
        # Añadir un usuario de ejemplo
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (?, ?, ?)',
            ('testuser', 'testuser@example.com', 'testpassword')
        )
        self.conn.commit()
        cursor.close()

        # Probar la obtención de usuarios
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

if __name__ == '__main__':
    # Ejecutar pruebas si el script se ejecuta directamente
    if 'CI' in os.environ:
        unittest.main()
    else:
        app.run(port=5000, host='0.0.0.0', debug=True)
