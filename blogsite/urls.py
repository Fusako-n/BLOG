from django.urls import path
from . import views

app_name = 'blogsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic_detail/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topic_good/<int:pk>/', views.topic_good, name='topic_good'),
    path('topic_delete/<int:pk>/', views.topic_delete, name='topic_delete'),
    path('topic_edit/<int:pk>/', views.topic_edit, name='topic_edit'),
    path('topic_create/', views.topic_create, name='topic_create'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage_edit/', views.mypage_edit, name='mypage_edit'),
]