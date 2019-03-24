from app.models import Article, Like
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", 'username')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Article
        fields = ('id', 'text', 'created_at', 'author')


class AddArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'text', 'created_at')


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    article = ArticleSerializer()

    class Meta:
        model = Like
        fields = ("id", "user", "article")
