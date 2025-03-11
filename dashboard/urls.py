from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.create_template, name='create_template'),
]
