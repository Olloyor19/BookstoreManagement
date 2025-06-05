from django.db import models
from django.conf import settings
from books.models import Book

class Order(models.Model):
    BUY = 'buy'
    BORROW = 'borrow'

    ORDER_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (BORROW, 'Borrow'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=6, choices=ORDER_TYPE_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    due_date = models.DateField(null=True, blank=True)  # Only for borrow

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.order_type})"

    class Meta:
        ordering = ['-created_at']

