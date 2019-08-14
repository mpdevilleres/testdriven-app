import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('marc', 'marc@gmail.com', 'randompasswordtest')

        self.assertTrue(user.id)
        self.assertEqual(user.username, 'marc')
        self.assertEqual(user.email, 'marc@gmail.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user('marc', 'marc@gmail.com', 'randompasswordtest')
        duplicate_user = User(
            username='marc',
            email='marc1@gmail.com',
            password='randompasswordtest'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('marc1', 'marc@gmail.com', 'randompasswordtest')
        duplicate_user = User(
            username='marc',
            email='marc@gmail.com',
            password='randompasswordtest'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('marc1', 'marc@gmail.com', 'randompasswordtest')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('marc', 'marc@gmail.com', 'randompasswordtest')
        user_two = add_user('marc1', 'marc1@gmail.com', 'randompasswordtest')
        self.assertNotEqual(user_one.password, user_two.password)


if __name__ == '__main__':
    unittest.main()
