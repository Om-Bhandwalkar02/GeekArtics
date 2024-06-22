from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.create_article, name='create_article'),
    path('edit/<int:pk>/', views.edit_article, name='edit_article'),
    path('delete/<int:pk>/', views.delete_article, name='delete_article'),
]