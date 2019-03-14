from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from django.utils import timezone
from .models import Article, Profile, Like


# モデルテスト
class ArticleTest(TestCase):
    def test___str__(self):
        article = Article.objects.create(text="test", author_id=1, created_at=timezone.now())
        self.assertTrue(article)
        self.assertEqual("test", article.text)


# モデルテスト
class ProfileTest(TestCase):
    def test___str__(self):
        profile = Profile.objects.create(introduction="test", sex=1, user_id=1)
        self.assertTrue(profile)
        self.assertEqual("test", profile.introduction)


def create_article(text, author_id):
    return Article.objects.create(text=text, author_id=author_id, created_at=timezone.now())


def update_article(text, author_id, update_text):
    article = Article.objects.get(text=text, author_id=author_id)
    article.text = update_text
    return article.save()


def delete_article(text, author_id):
    article = Article.objects.get(text=text, author_id=author_id)
    return article.delete()


class ViewTest(TestCase):

    # ログイン設定
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='passoworld')
        self.client.login(username='TestUser', password='passoworld')

    def test_top(self):
        response = self.client.get(resolve_url('app:top'))
        self.assertEqual(200, response.status_code)

    def test_IndexView(self):
        # アクセスと、何もデータが無いか
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['article_list'].count())
        # データを一つ追加し、レスポンスが１つ増えているか
        create_article("create", self.user.id)
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context['article_list'].count())
        # データを一つ削除し、レスポンスが０になっているか
        delete_article("create", self.user.id)
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.context['article_list'].count())

    def test_CreateView(self):
        # アクセスの確認
        response = self.client.get(resolve_url('app:create'))
        self.assertEqual(200, response.status_code)
        # データを追加できているか
        create_article("create", self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Article.objects.get(text="create", author_id=self.user.id))

    def test_UpdateView(self):
        # アクセスの確認
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        # データを追加できているか
        create_article("create", self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Article.objects.get(text="create", author_id=self.user.id))
        # データを編集出来ているか
        update_article("create", self.user.id, "update")
        self.assertEqual(200, response.status_code)
        self.assertTrue(Article.objects.get(text="update"))

    def test_DeleteView(self):
        # アクセスの確認
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        # データを追加できているか
        create_article("create", self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Article.objects.get(text="create", author_id=self.user.id))
        # データを削除できているか
        delete_article("create", self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Article.objects.all().count())

    def test_like(self):
        # データを一つ追加し、いいね確認
        article = Article.objects.create(text="Do you like?", author_id=11, created_at=timezone.now())
        article_id = article.id
        Like.objects.create(article_id=article_id, user_id=self.user.id, created_at=timezone.now())
        response = self.client.get(resolve_url('app:index'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context['likes'][1])
