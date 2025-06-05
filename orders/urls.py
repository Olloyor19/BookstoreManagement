from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:book_id>/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
