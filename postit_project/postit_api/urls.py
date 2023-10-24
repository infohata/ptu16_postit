from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('post/<int:pk>/comments/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
]
