import unittest
import os
import sqlite3
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_ENV'] = 'testing'
        self.app = app.test_client()
        self.app.testing = True

        # Crear la base de datos en memoria
        self.conn = sqlite3.connect(':memory:')
        cursor = self.conn.cursor()

        # Crear tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS table1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL,
                correo TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        cursor.close()

        # Reemplazar get_db_connection con la conexión SQLite en memoria
        app.get_db_connection = lambda: self.conn

    def tearDown(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM table1')
        self.conn.commit()
        cursor.close()
        self.conn.close()

    def test_add_user(self):
        response = self.app.post('/add_user', json={
            'nombre_usuario': 'prueba2user',
            'correo': 'test2@example.com',
            'contrasena': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User added successfully!', response.data)

    def test_get_users(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO table1 (nombre_usuario, correo, contrasena) VALUES (?, ?, ?)',
            ('prueba2user', 'test2@example.com', 'testpassword')
        )
        self.conn.commit()
        cursor.close()

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'prueba2user', response.data)

if __name__ == '__main__':
    unittest.main()

