from django.test import TestCase
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from app.models import Article, Profile, Like
from django.utils import timezone


class SignUpTest(TestCase):
    def test_SignUpView(self):
        # アカウント作成テスト
        data = {
            'username': 'hogetaro',
            'password1': 'pas19240ls',
            'password2': 'pas19240ls'
        }
        response = self.client.post(resolve_url('accounts:signup'), data)
        self.assertRedirects(response, resolve_url("login"))
        self.client.login(username="hogetaro", password="pas19240ls")
        response = self.client.get(resolve_url("app:index"))
        self.assertEqual(200, response.status_code)


class ViewTest(TestCase):

    def setUp(self):
        # ログイン設定
        self.user = User.objects.create_user(username='TestUser', password='passoworld')
        self.client.login(username='TestUser', password='passoworld')

    def test_UserDetail(self):
        # アクセスの確認
        response = self.client.get(resolve_url('accounts:user_detail', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        # ユーザー情報作成
        Profile.objects.create(introduction="create", sex=1, user_id=self.user.id)
        response = self.client.get(resolve_url('accounts:user_update', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        # ユーザー情報更新
        profile = Profile.objects.get(user_id=self.user.id)
        profile.introduction = "update"
        profile.save()
        response = self.client.get(resolve_url('accounts:user_update', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        self.assertTrue("update", response.context["profile"])
        # ユーザーページ上の投稿一覧
        Article.objects.create(text="create1", author_id=self.user.id, created_at=timezone.now())
        Article.objects.create(text="create2", author_id=self.user.id, created_at=timezone.now())
        Article.objects.create(text="create3", author_id=self.user.id, created_at=timezone.now())
        response = self.client.get(resolve_url('accounts:user_detail', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.context["my_article"].count())

    def test_UserUpdate(self):
        # ユーザー情報作成
        Profile.objects.create(introduction="create", sex=1, user_id=self.user.id)
        response = self.client.get(resolve_url('accounts:user_update', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        # アクセスの確認
        response = self.client.get(resolve_url('accounts:user_update', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        # ユーザー情報更新
        profile = Profile.objects.get(user_id=self.user.id)
        profile.introduction = "update"
        profile.save()
        response = self.client.get(resolve_url('accounts:user_update', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context["profile"])

    def test_UserCreate(self):
        # アクセスの確認
        response = self.client.get(resolve_url('accounts:user_create', pk=self.user.id))
        self.assertEqual(200, response.status_code)

    def test_PasswordChange(self):
        # アクセスの確認
        response = self.client.get(resolve_url('accounts:password_change', pk=self.user.id))
        self.assertEqual(200, response.status_code)

    def test_MyLikeArticle(self):
        # アクセスの確認
        response = self.client.get(resolve_url('accounts:mylike', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        # いいねを追加し、追加した分がcontextに渡されているか
        article = Article.objects.create(text="Do you like?", author_id=11, created_at=timezone.now())
        article_id = article.id
        Like.objects.create(article_id=article_id, user_id=self.user.id, created_at=timezone.now())
        response = self.client.get(resolve_url('accounts:mylike', pk=self.user.id))
        self.assertEqual(200, response.status_code)
        self.assertTrue(1, len(response.context["like_list"]))
