from django.urls import path
from .views import moderate_template

urlpatterns = [
    path("moderate/", moderate_template, name="moderate_template"),
]
