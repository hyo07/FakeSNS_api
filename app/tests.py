from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='passoworld')
        self.client.login(username='TestUser', password='passoworld')

    def test_top(self):
        response = self.client.get(resolve_url('app:top'))
        self.assertEqual(200, response.status_code)

    def test_IndexView(self):
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['article_list'].count())

    def test_CreateView(self):
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)

    def test_UpdateView(self):
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)

    def test_DeleteView(self):
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
