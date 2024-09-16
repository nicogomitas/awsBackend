import unittest
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

# Configuración de la aplicación Flask y base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# Modelo de ejemplo para la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)

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

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{
        'nombre_usuario': user.nombre_usuario,
        'correo': user.correo
    } for user in users])

def get_db_connection():
    import mysql.connector
    return mysql.connector.connect(
        host='localhost',
        user='yourusername',
        password='yourpassword',
        database='yourdatabase'
    )

class FlaskTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.data.decode(), 'Hello, World!')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        response = self.client.post(
            '/add_user',
            json={'nombre_usuario': 'test_user', 'correo': 'test@example.com', 'contrasena': 'password123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User added successfully!')

    def test_get_users(self):
        self.client.post(
            '/add_user',
            json={'nombre_usuario': 'test_user', 'correo': 'test@example.com', 'contrasena': 'password123'}
        )
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.json
        self.assertGreater(len(users), 0)
        self.assertEqual(users[0]['nombre_usuario'], 'test_user')
        self.assertEqual(users[0]['correo'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()


