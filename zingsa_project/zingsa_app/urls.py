from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_person, name='add_person'),
    path('delete/<int:person_id>/', views.delete_person, name='delete_person'),
    path('', views.person_list, name='person_list'),
]