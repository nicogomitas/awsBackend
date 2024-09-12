import unittest
from flask import json
import requests

class FlaskTestCase(unittest.TestCase):
    BASE_URL = 'http://ec2-3-85-102-61.compute-1.amazonaws.com:5000'  # Reemplaza <EC2_PUBLIC_IP> con la IP pública de tu instancia EC2

    def test_hello_world(self):
        response = requests.get(f'{self.BASE_URL}/')
        self.assertEqual(response.text, 'Hello, World!')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        response = requests.post(
            f'{self.BASE_URL}/add_user',
            json={'nombre_usuario': 'test_user', 'correo': 'test@example.com', 'contrasena': 'password123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'User added successfully!')

    def test_get_users(self):
        # Insertar un usuario en la base de datos (esto puede no ser necesario si el usuario ya está en la base de datos)
        requests.post(
            f'{self.BASE_URL}/add_user',
            json={'nombre_usuario': 'test_user', 'correo': 'test@example.com', 'contrasena': 'password123'}
        )

        response = requests.get(f'{self.BASE_URL}/users')
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreater(len(users), 0)
        self.assertEqual(users[0]['nombre_usuario'], 'test_user')
        self.assertEqual(users[0]['correo'], 'test@example.com')

if _name_ == '_main_':
    unittest.main()
