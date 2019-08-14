import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service"""

    def test_users(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        with self.client as client:
            response = client.post(
                '/users',
                data=json.dumps({
                    'username': 'marc',
                    'email': 'marc@devilleres.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('marc@devilleres.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client as client:
            response = client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        with self.client as client:
            response = client.post(
                '/users',
                data=json.dumps({
                    'email': 'mpdevilleres@gmail.com',
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        with self.client as client:
            client.post(
                '/users',
                data=json.dumps({
                    'username': 'mpdevilleres',
                    'email': 'mpdevilleres@gmail.com'
                }),
                content_type='application/json',
            )
            response = client.post(
                '/users',
                data=json.dumps({
                    'username': 'mpdevilleres',
                    'email': 'mpdevilleres@gmail.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        user = add_user('mpdevilleres', 'mpdevilleres@gmail.com')
        with self.client as client:
            response = client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('mpdevilleres', data['data']['username'])
            self.assertIn('mpdevilleres@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        with self.client as client:
            response = client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        with self.client as client:
            response = client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        add_user('marc', 'marc@gmail.com')
        add_user('philippe', 'philippe@gmail.com')
        add_user('mpdevilleres', 'mpdevilleres@gmail.com')

        with self.client as client:
            response = client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 3)
            self.assertIn('marc', data['data']['users'][0]['username'])
            self.assertIn('marc@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('philippe', data['data']['users'][1]['username'])
            self.assertIn(
                'philippe@gmail.com', data['data']['users'][1]['email']
            )
            self.assertIn('mpdevilleres', data['data']['users'][2]['username'])
            self.assertIn(
                'mpdevilleres@gmail.com', data['data']['users'][2]['email']
            )

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Users', response.data.decode())
        self.assertIn('<p>No users!</p>', response.data.decode())

    def test_main_with_users(self):
        add_user('marc', 'marc@gmail.com')
        add_user('mpdevilleres', 'mpdevilleres@gmail.com')
        with self.client as client:
            response = client.get('/')
            data = response.data.decode()
            self.assertEqual(response.status_code, 200)
            self.assertIn('All Users', data)
            self.assertNotIn('<p>No users!</p>', data)
            self.assertIn('marc', data)
            self.assertIn('mpdevilleres', data)

    def test_main_add_user(self):
        with self.client as client:
            response = client.post(
                '/',
                data={
                    'username': 'marc',
                    'email': 'marc@gmail.com',
                },
                follow_redirects=True
            )
            data = response.data.decode()
            self.assertEqual(response.status_code, 200)
            self.assertIn('All Users', data)
            self.assertNotIn('<p>No users!</p>', data)
            self.assertIn('marc', data)


if __name__ == '__main__':
    unittest.main()
