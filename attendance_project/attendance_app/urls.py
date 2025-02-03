from django.urls import path
from .views import process_csv

urlpatterns = [
    path('', process_csv, name='process_csv'),
]
