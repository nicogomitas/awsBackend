import unittest
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# Define tus modelos aquí

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
