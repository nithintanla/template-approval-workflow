from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.create_template, name='create_template'),
    path('analytics/', views.analytics, name='analytics'),
    path('approvals/settings/', views.approval_settings, name='approval_settings'),
    path('approvals/review/', views.review_templates, name='review_templates'),
    path('approvals/update/<int:template_id>/', views.update_template_status, name='update_template_status'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/create/', views.create_brand, name='create_brand'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/create/', views.create_agent, name='create_agent'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
