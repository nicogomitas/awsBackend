import os
import unittest
import sqlite3
from app import app  # Asegúrate de que importas tu aplicación Flask correctamente

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary in-memory database."""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['DATABASE'] = ':memory:'
        cls.client = cls.app.test_client()

        # Crear tabla en la base de datos en memoria
        with cls.app.app_context():
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE table1 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT,
                    correo TEXT,
                    contrasena TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()

    def setUp(self):
        """Set up the database connection for each test."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.app.config['DATABASE'] = ':memory:'

    def tearDown(self):
        """Clean up after each test."""
        self.conn.close()

    def test_add_user(self):
        response = self.client.post('/add_user', json={
            'nombre_usuario': 'Test User',
            'correo': 'test@example.com',
            'contrasena': 'password123'
        })
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()


