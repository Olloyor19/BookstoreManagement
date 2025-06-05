from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.books_by_category, name='book_list'),
    path('books/category/<int:category_id>/', views.books_by_category, name='books_by_category'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]
