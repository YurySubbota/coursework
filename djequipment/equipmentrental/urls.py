from django.urls import path
from equipmentrental import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail_equipment/<int:equipment_id>/', views.detail_equipment, name='detail_equipment'),
    path('cart/', views.cart_view, name='cart'),
    path('detail_equipment/<int:equipment_id>/add_cart/', views.add_cart, name='add_cart'),
    path('detail_equipment/<int:equipment_id>/remove_cart/', views.remove_cart, name='remove_cart'),
]