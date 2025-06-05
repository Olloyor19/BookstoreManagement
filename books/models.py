from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    SELL = 'sell'
    BORROW = 'borrow'
    BOTH = 'both'

    BOOK_TYPE_CHOICES = [
        (SELL, 'For Sale'),
        (BORROW, 'For Borrowing'),
        (BOTH, 'For Sale & Borrowing'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES, default=SELL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}⭐"