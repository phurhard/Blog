from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign_up', views.signup, name='sign_up'),
    path('post', views.post, name='post'),
    path('articles', views.articles, name='article'),
]