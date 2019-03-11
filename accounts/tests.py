from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='passoworld')
        self.client.login(username='TestUser', password='passoworld')

    def test_UserDetail(self):
        response = self.client.get(resolve_url('accounts:user_detail'))
        self.assertEqual(200, response.status_code)

    def test_UserUpdate(self):
        response = self.client.get(resolve_url('accounts:user_update'))
        self.assertEqual(200, response.status_code)

    def test_UserCreate(self):
        response = self.client.get(resolve_url('accounts:user_create'))
        self.assertEqual(200, response.status_code)

    def test_PasswordChange(self):
        response = self.client.get(resolve_url('accounts:password_change'))
        self.assertEqual(200, response.status_code)
