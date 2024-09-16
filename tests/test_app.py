import unittest
import os
from app import app, get_db_connection

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
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
        self.conn.close()

    def test_add_user(self):
        response = self.app.post('/add_user', json={
            'nombre_usuario': 'testuser',
            'correo': 'testuser@example.com',
            'contrasena': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

    def test_get_users(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)',
            ('testuser', 'testuser@example.com', 'testpassword')
        )
        self.conn.commit()
        cursor.close()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

if _name_ == '_main_':
    unittest.main()
