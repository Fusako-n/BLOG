from django.urls import path
from . import views

app_name = 'blogsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('topic_edit/<int:pk>/', views.post_edit, name='post_edit'),
]