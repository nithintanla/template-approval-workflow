from django.urls import path
from . import views

urlpatterns = [
    path('review_templates/', views.review_templates, name='review_templates'),
    path('update_template_status/<int:template_id>/', views.update_template_status, name='update_template_status'),
]
