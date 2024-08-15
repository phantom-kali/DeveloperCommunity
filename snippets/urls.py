from django.urls import path
from . import views

urlpatterns = [
    path('', views.snippet_list, name='snippet_list'),
    path('create/', views.create_snippet, name='create_snippet'),
    path('<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('<int:pk>/edit/', views.edit_snippet, name='edit_snippet'),
    path('<int:pk>/delete/', views.delete_snippet, name='delete_snippet'),
]