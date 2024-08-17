from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('vote/<int:content_type_id>/<int:object_id>/', views.vote, name='vote'),
    path('report/<int:content_type_id>/<int:object_id>/', views.report, name='report'),
]