from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.top, name='top'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]
