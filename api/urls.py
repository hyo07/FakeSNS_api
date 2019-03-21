from django.urls import path

from . import views


urlpatterns = [
    path('article/', views.ArticleIndex.as_view()),
    path('article/<int:pk>/', views.ArticleIndividual.as_view()),
    path('<int:pk>/article/', views.UsersArticle.as_view()),
    path('profile/', views.ProfileIndex.as_view()),
    path('profile/<int:pk>/', views.ProfileIndividual.as_view()),
    path('blacklist/', views.Blacklist.as_view()),
    path('like/', views.LikeList.as_view()),
    path('like/add/', views.LikeAdd.as_view()),
    path('like/<int:pk>/', views.LikeIndividual.as_view()),
    path('users/', views.UserList.as_view()),

]
