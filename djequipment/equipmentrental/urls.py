from django.urls import path
from equipmentrental import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail_equipment/<int:equipment_id>/', views.detail_equipment, name='detail_equipment'),
]