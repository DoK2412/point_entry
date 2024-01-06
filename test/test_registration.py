import unittest

from httpx import AsyncClient

from app import app

from faker import Faker
import pandas as pd



class TestUM(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = AsyncClient(app=app, base_url='http://127.0.0.1:8081')

    def tearDown(self):
        pass

    fake = Faker()

    registr_params = {
        'mail': fake.email(),
        'password': '451183311qQ',
        'password_repeat': '451183311qQ',
        'first_name': fake.name().split(' ')[0],
        'last_name': fake.name().split(' ')[1],
        'dev': True
    }


    # async def test_logout(self):
    #     async with self.client as test_client:
    #         response = await test_client.get('/logout')
    #
    #     response_json = response.json()
    #
    #     self.assertEqual(response_json['answercode'], 1)


    async def test_registration_1(self):
        async with self.client as test_client:
            response = await test_client.post('/registration',
                                              json=TestUM.registr_params)
        response_json = response.json()
        self.assertEqual(response_json['answercode'], 1)

    session = [
        {'moi':
            {
                'email': None,
                'uid_session': 'f4cc5ac4-264e-4152-87f6-28408c5b29c4',
                'update': False,
                'user_id': 93},
            'session': 'active'
        }
    ]

    confirm_reg_params = {
        "code": "666666",
        "public_key": "Открытый ключ",
        "private_key": "Закрытый ключ пользователя"
    }

    async def test_confirmRegistration_1(self):
        async with self.client as test_client:
            response = await test_client.post('/confirmRegistration',
                                              json=TestUM.confirm_reg_params,
                                              )
        response_json = response.json()
        self.assertEqual(response_json['answercode'], 1)


if __name__ == '__main':
    unittest.main()

