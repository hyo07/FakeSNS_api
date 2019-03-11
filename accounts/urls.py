from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('<int:pk>/detail', views.UserDetail.as_view(), name='user_detail'),
    path('<int:pk>/update', views.UserUpdate.as_view(), name='user_update'),
    path('<int:pk>/create', views.UserCreate.as_view(), name='user_create'),
    path('black_list/<int:pk>', views.black_list, name='black_list'),

    path('<int:pk>/password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('<int:pk>/password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
