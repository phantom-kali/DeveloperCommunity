from django.urls import path
from . import views

urlpatterns = [
    path('', views.snippet_list, name='snippet_list'),
    path('add/', views.add_snippet, name='add_snippet'),
    path('<int:pk>/', views.snippet_detail, name='snippet_detail'),
]