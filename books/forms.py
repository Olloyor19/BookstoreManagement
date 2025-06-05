from django import forms
from .models import Book, Review


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'image', 'price', 'stock', 'book_type']



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(),  # 👈 Use dropdown
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
