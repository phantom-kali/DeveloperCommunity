from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/delete/', views.delete_document, name='delete_document'),
    path('links/', views.link_list, name='link_list'),
    path('links/add/', views.add_link, name='add_link'),
    path('links/<int:pk>/delete/', views.delete_link, name='delete_link'),
    path('report/<int:pk>/', views.report_link, name='report_link'),
]