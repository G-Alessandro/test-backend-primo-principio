from django.urls import path
from .views import registra_eventi

urlpatterns = [
    path("registra-eventi/", registra_eventi),
]
