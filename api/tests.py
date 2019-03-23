from django.contrib.auth.models import User
from django.urls import reverse
import json
from rest_framework.test import APITestCase
from rest_framework import status


def create_user():
    admin = User.objects.create_superuser('admin', "", 'admin')
    user = User.objects.create_user('test', "", 'test')
    return admin, user


class LoginTests(APITestCase):

    def test_login(self):
        create_user()

        # スーパーユーザーのログイン確認
        response = self.client.post("/api/rest-auth/login/", {"username": "admin", 'password': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))

        # 一般ユーザーのログイン確認
        response = self.client.post("/api/rest-auth/login/", {'username': 'test', 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))

        # 不正な入力での確認
        response = self.client.post("/api/rest-auth/login/", {'username': 'hgoe', 'password': 'hoge'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, json.loads(response.content))

        # 不正な入力での確認
        response = self.client.post("/api/rest-auth/login/", {'kfda': 'hgoe', 'fdgsfd': 'hoge'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, json.loads(response.content))

    def test_signup(self):
        # アカウント作成
        response = self.client.post("/api/rest-auth/registration/",
                                    {"username": "suser", 'password1': 'dnaidwad', "password2": "dnaidwad"},
                                    format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))

        # DBに追加されているか
        user = User.objects.first()
        self.assertEqual(user.username, "suser")

    def test_article(self):
        create_user()

        # トークン不保持
        response = self.client.get(reverse("api:article"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.loads(response.content))

        # トークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "test", 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key = json.loads(response.content)["key"]

        # トークン保持してarticleにGET
        response = self.client.get(reverse("api:article"), HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual([], json.loads(response.content))

        # トークン保持してarticleにPOST
        response = self.client.post(reverse("api:article"),  {"text": "TEXT", 'author': 2},
                                    format="json", HTTP_X_AUTH_TOKEN=key)
        res_article = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["text"], "TEXT")

        # トークン保持してarticleにGET、POSTしたデータと同じものがあるか
        response = self.client.get(reverse("api:article"), HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(res_article, json.loads(response.content)[0])

        # <user_id>/article/ で取得できるか確認
        response = self.client.get("/api/2/article/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(res_article, json.loads(response.content)[0])
        self.assertEqual(json.loads(response.content)[0]["text"], "TEXT")

        # PUTで編集
        response = self.client.put("/api/article/1/", {"text": "PUUTTTT", 'author': 2},
                                   format="json", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["text"], "PUUTTTT")

        # DELETEで削除
        response = self.client.delete("/api/article/1/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # articleにGETして中身が無しかどうか
        response = self.client.get(reverse("api:article"), HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual([], json.loads(response.content))

    def test_profile(self):
        create_user()

        # トークン不保持
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.loads(response.content))

        # トークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "test", 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key = json.loads(response.content)["key"]

        # GET
        response = self.client.get("/api/profile/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual([], json.loads(response.content))

        # POST
        response = self.client.post("/api/profile/", {"introduction": "test", 'sex': 1},
                                    format='json', HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("test" in json.loads(response.content).values())

        # １つ追加されているかGETで確認
        response = self.client.get("/api/profile/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(len(json.loads(response.content)), 1)

        # 個別取得にGET
        response = self.client.get("/api/profile/2/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["introduction"], "test")

        # 個別取得にPUT
        response = self.client.put("/api/profile/2/", {"introduction": "PUTTUTUT", 'sex': 2},
                                   format='json', HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["introduction"], "PUTTUTUT")

    def test_blacklist(self):
        create_user()

        # トークン不保持
        response = self.client.get("/api/blacklist/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.loads(response.content))

        # トークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "test", 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key = json.loads(response.content)["key"]

        # ユーザー情報登録（登録しないとブラックリスト機能は使えないため）
        response = self.client.post("/api/profile/", {"introduction": "test", 'sex': 1},
                                    format='json', HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))

        # GET、追加していないので空のリスト
        response = self.client.get("/api/blacklist/", HTTP_X_AUTH_TOKEN=key)
        blacklist = json.loads(response.content)["BlackList"]
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(blacklist, [])

        # POSTで追加
        response = self.client.post("/api/blacklist/", {"add_user_id": 1}, format='json', HTTP_X_AUTH_TOKEN=key)
        blacklist = json.loads(response.content)["black_list"]
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))

        # GETで確認
        response = self.client.get("/api/blacklist/", HTTP_X_AUTH_TOKEN=key)
        blacklist = json.loads(response.content)["BlackList"]
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(blacklist, [1])

        # POSTで削除
        response = self.client.post("/api/blacklist/", {"del_user_id": 1}, format='json', HTTP_X_AUTH_TOKEN=key)
        blacklist = json.loads(response.content)["black_list"]
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))

        # GETで確認
        response = self.client.get("/api/blacklist/", HTTP_X_AUTH_TOKEN=key)
        blacklist = json.loads(response.content)["BlackList"]
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(blacklist, [])

    def test_like(self):
        create_user()

        # トークン不保持
        response = self.client.get("/api/like/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.loads(response.content))

        # トークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "test", 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key = json.loads(response.content)["key"]

        # 別ユーザーのトークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "admin", 'password': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key2 = json.loads(response.content)["key"]

        # 別ユーザーでトークン保持してarticleにPOST
        response = self.client.post(reverse("api:article"),  {"text": "TEXT", 'author': 1},
                                    format="json", HTTP_X_AUTH_TOKEN=key2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["text"], "TEXT")

        # いいねにGET
        response = self.client.get("/api/like/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content), [])
        # TODO　気持ち追加色々

        # GETで全投稿一覧、別ユーザーの投稿が確認
        response = self.client.get("/api/like/add/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)[0]["author"]["id"], 1)

        # POSTでいいねに追加
        response = self.client.post("/api/like/add/", {"article_id": 1}, format='json', HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["article"]["text"], "TEXT")

        # いいねに追加されてるか確認
        response = self.client.get("/api/like/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(len(json.loads(response.content)), 1)

        # いいね個別取得
        response = self.client.get("/api/like/1/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(json.loads(response.content)["article"]["id"], 1)

        # いいねから削除
        response = self.client.delete("/api/like/1/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # いいねから削除できているか確認
        response = self.client.get("/api/like/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_users(self):
        create_user()

        # トークン不保持
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, json.loads(response.content))

        # トークン取得
        response = self.client.post("/api/rest-auth/login/", {"username": "test", 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertTrue("key" in json.loads(response.content))
        key = json.loads(response.content)["key"]

        # ユーザー一覧をGETで取得
        response = self.client.get("/api/users/", HTTP_X_AUTH_TOKEN=key)
        self.assertEqual(response.status_code, status.HTTP_200_OK, json.loads(response.content))
        self.assertEqual(len(json.loads(response.content)), 2)
        self.assertEqual(json.loads(response.content)[1]["username"], "test")
