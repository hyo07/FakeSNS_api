from app.models import Article, Profile, Like, BlackList
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from .serializer import UserSerializer, ArticleSerializer, LikeSerializer, AddArticleSerializer
from libs import BlackList


# 投稿一覧と作成
class ArticleIndex(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # ブラックリストを除外
        try:
            str_bl = BlackList.read_bl(self.request.user.profile.black_list)
        except Profile.DoesNotExist:
            return Article.objects.all().order_by("-created_at")

        int_bl = BlackList.str_to_int(str_bl)
        return Article.objects.exclude(author__in=int_bl).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddArticleSerializer
        return ArticleSerializer

    def post(self, request, *args, **kwargs):
        try:
            text = self.request.data["text"]
        except KeyError:
            return Response({"message": "入力が不正です"})
        article = Article(text=text, author_id=self.request.user.id)
        article.save()
        res_art_dic = {}
        res_art_dic["id"] = article.id
        res_art_dic["text"] = article.text
        res_art_dic["created_at"] = article.created_at
        res_art_dic["author"] = {"id": article.author.id, "username":  article.author.username}
        return Response(res_art_dic)


# 投稿の個別取得、編集、削除
class ArticleIndividual(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # 投稿者以外も取得は可能にパーミッションを変更
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (IsAuthorOrReadOnly,)
        return [permission() for permission in permission_classes]

    def put(self, request, *args, **kwargs):
        try:
            text = self.request.data["text"]
        except KeyError:
            return Response({"message": "入力が不正です"})
        article = Article.objects.get(id=self.kwargs["pk"])
        article.text = text
        article.save()
        res_art_dic = {}
        res_art_dic["id"] = article.id
        res_art_dic["text"] = article.text
        res_art_dic["created_at"] = article.created_at
        res_art_dic["author"] = {"id": article.author.id, "username":  article.author.username}
        return Response(res_art_dic)


# ユーザーごとの投稿一覧
class UsersArticle(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        article = Article.objects.filter(author_id=self.kwargs["pk"]).order_by("-created_at")
        return article


# プロフィール一覧、新規登録
class ProfileIndex(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        profiles = Profile.objects.all().select_related("user").order_by("id")
        res_pro_lis = []
        for profile in profiles:
            res_pro_dic = {}
            res_pro_dic["id"] = profile.id
            res_pro_dic["introduction"] = profile.introduction
            res_pro_dic["sex"] = profile.sex
            res_pro_dic["user"] = {"id": profile.user_id, "username": profile.user.username}
            res_pro_lis.append(res_pro_dic)
        return Response(res_pro_lis)

    def post(self, request):
        data = self.request.data
        try:
            introduction = data["introduction"]
            sex = data["sex"]
            if not (sex == 1 or sex == 2):
                return Response({"message": "性別は<1:女性, 2:男性>から選んでください"})
            try:
                if Profile.objects.get(user_id=self.request.user.id):
                    return Response({"message": "既にユーザー情報が登録されています"})
            except Profile.DoesNotExist:
                pass
        except KeyError:
            return Response({"message": "必要なキーは<introduction, sex>です"})
        profile = Profile(introduction=introduction, sex=str(sex), user_id=self.request.user.id)
        profile.save()
        res_pro_dic = {}
        res_pro_dic["message"] = "ユーザー情報を登録しました"
        res_pro_dic["id"] = profile.id
        res_pro_dic["introduction"] = profile.introduction
        res_pro_dic["sex"] = profile.sex
        res_pro_dic["user"] = {"id": profile.user_id, "username": profile.user.username}

        return Response(res_pro_dic)


# プロフィール個別取得、編集
class ProfileIndividual(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(user_id=pk)
        except Profile.DoesNotExist:
            return Response({"message": "指定したユーザーは存在しません"})
        res_pro_dic = {}
        res_pro_dic["id"] = profile.id
        res_pro_dic["introduction"] = profile.introduction
        res_pro_dic["sex"] = profile.sex
        res_pro_dic["user"] = {"id": profile.user_id, "username": profile.user.username}
        return Response(res_pro_dic)

    def put(self, request, pk):
        try:
            User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"message": "指定したユーザーは存在しません"})
        if pk != self.request.user.id:
            return Response({"message": "このアクションを実行する権限がありません。"})
        try:
            profile = Profile.objects.get(user_id=pk)
        except Profile.DoesNotExist:
            return Response({"message": "ユーザー情報が登録されていません"})

        data = self.request.data
        try:
            introduction = data["introduction"]
            sex = data["sex"]
            if not (sex == 1 or sex == 2):
                return Response({"message": "性別は<1:女性, 2:男性>から選んでください"})
        except KeyError:
            return Response({"message": "必要なキーは<introduction, sex>です"})

        profile.introduction = introduction
        profile.sex = str(sex)
        profile.save()

        res_pro_dic = {}
        res_pro_dic["id"] = profile.id
        res_pro_dic["introduction"] = profile.introduction
        res_pro_dic["sex"] = profile.sex
        res_pro_dic["user"] = {"id": profile.user_id, "username": profile.user.username}

        return Response(res_pro_dic)


# ブラックリスト
class Blacklist(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # 自身が登録したブラックリスト一覧
    def get(self, request):
        try:
            profile = Profile.objects.get(user_id=self.request.user.id)
        except Profile.DoesNotExist:
            return Response({"message": "プロフィールを登録すると使用可能になります"})
        str_bl = BlackList.read_bl(profile.black_list)
        int_bl = BlackList.str_to_int(str_bl)
        return Response({
            "username": self.request.user.username,
            "BlackList": int_bl
        })

    # ブラックリストの追加、削除
    def post(self, request):
        my_user_id = self.request.user.id
        try:
            profile = Profile.objects.get(user_id=my_user_id)
        except Profile.DoesNotExist:
            # raise Exception("プロフィールを登録すると使用可能になります")
            return Response({"message": "プロフィールを登録すると使用可能になります"})

        # "add_user_id"を取得し追加
        try:
            add_id = request.data["add_user_id"]
            try:
                User.objects.get(id=int(add_id))
            except User.DoesNotExist:
                return Response({"message": "<user_id: {}>というアカウントは存在しません".format(add_id)})
            if add_id == self.request.user.id:
                return Response({"message": "自身をブラックリストに追加することは出来ません"})
            text = profile.black_list
            old_bl_str = BlackList.read_bl(text)
            old_bl = BlackList.str_to_int(old_bl_str)
            if int(add_id) in old_bl:
                res_dic = {"user_id": "username"}
                for b in old_bl:
                    user = User.objects.get(id=b)
                    res_dic[b] = user.username
                return Response({
                    "your user_id": my_user_id,
                    "BlackList": res_dic,
                    "message": "既に <username: {}> はブラックリストに追加されています".format(res_dic[int(add_id)])
                })
            else:
                bl = BlackList.add_bl(text, str(add_id))
                profile.black_list = bl
                profile.save()
        except KeyError:
            pass

        # "del_user_id"を取得しブラックリストから削除
        try:
            del_id = request.data["del_user_id"]
            try:
                User.objects.get(id=int(del_id))
            except User.DoesNotExist:
                return Response({"message": "<user_id: {}>というアカウントは存在しません".format(del_id)})
            text = profile.black_list
            old_bl_str = BlackList.read_bl(text)
            old_bl = BlackList.str_to_int(old_bl_str)
            if int(del_id) in old_bl:
                bl = BlackList.delete_bl(text, str(del_id))
                profile.black_list = bl
                profile.save()
            else:
                res_dic2 = {"user_id": "user_name"}
                for d in old_bl:
                    user = User.objects.get(id=d)
                    res_dic2[d] = user.username
                return Response({
                    "your user_id": my_user_id,
                    "BlackList": res_dic2,
                    "message": "<user_id: {}> はブラックリストに追加されていません".format(del_id)
                })
        except KeyError:
            pass

        profile = Profile.objects.get(user_id=my_user_id)
        bl = BlackList.str_to_int(BlackList.read_bl(profile.black_list))
        res_dic0 = {"user_id": "user_name"}
        for bd in bl:
            user = User.objects.get(id=bd)
            res_dic0[bd] = user.username
        return Response({"your user_id": my_user_id, "black_list": res_dic0})


# 自身が追加した、いいね一覧
class LikeList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(user_id=self.request.user.id).select_related("article").order_by("created_at")


# いいねするための投稿一覧と、いいね追加
class LikeAdd(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        res_art_lis = []
        articles = Article.objects.all().order_by("-created_at")
        for article in articles:
            res_art_dic = {}
            res_art_dic["id"] = article.id
            res_art_dic["text"] = article.text
            res_art_dic["created_at"] = article.created_at
            res_art_dic["author"] = {"id": article.author_id, "username": article.author.username}
            res_art_lis.append(res_art_dic)
        return Response(res_art_lis)

    def post(self, request):
        try:
            article_id = request.data["article_id"]
            Article.objects.get(id=article_id)
        except KeyError:
            return Response({"message": "<article_id>を入力してください"})
        except Article.DoesNotExist:
            return Response({"message": "<article_id:{}>は存在しません".format(article_id)})
        try:
            if Like.objects.get(article_id=article_id, user_id=self.request.user.id):
                return Response({"message": "すでにいいねに追加しています"})
        except Article.DoesNotExist:
            return Response({"message": "<article_id:{}>は存在しません".format(article_id)})
        except Like.DoesNotExist:
            pass

        like = Like(article_id=int(article_id), user_id=self.request.user.id)
        like.save()

        res_like_dic = {}
        res_like_dic["message"] = "いいねに追加しました"
        res_like_dic["id"] = like.id
        res_like_dic["user"] = {"id": self.request.user.id, "username": self.request.user.username}
        article = Article.objects.get(id=article_id)
        user = User.objects.get(id=article.author_id)
        res_like_dic["article"] = {"id": article.id, "text": article.text, "created_at": article.created_at,
                                   "author": {"id": article.author_id, "username": user.username}}
        return Response(res_like_dic)


# 自身が追加した、いいねを指定取得、削除
class LikeIndividual(generics.RetrieveDestroyAPIView):
    permission_classes = (IsUserOrReadOnly,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


# ユーザー、一覧
class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
