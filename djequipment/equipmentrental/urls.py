from django.urls import path
from equipmentrental import views

urlpatterns = [
    path('', views.index, name='index'),
]