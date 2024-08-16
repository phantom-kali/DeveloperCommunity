from django.urls import path
from . import views

urlpatterns = [
    path('', views.error_list, name='error_list'),
    path('create/', views.create_error, name='share_error'),
    path('<int:pk>/', views.error_detail, name='error_detail'),
    path('<int:pk>/edit/', views.edit_error, name='edit_error'),
    path('<int:pk>/delete/', views.delete_error, name='delete_error'),
    path('<int:error_pk>/accept_solution/<int:solution_pk>/', views.accept_solution, name='accept_solution'),
]