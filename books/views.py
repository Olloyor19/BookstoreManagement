from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import Book, Review, Category
from django.db.models import Avg, Count, Q
# from .models import Book, Category
from .forms import ReviewForm

def book_list(request):
    filter_type = request.GET.get('type')
    if filter_type:
        books = Book.objects.filter(book_type=filter_type)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.select_related('user').all().order_by('-created_at')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
            return redirect('book_detail', pk=book.pk)
    else:
        review_form = ReviewForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'review_form': review_form,
    })


#
# def books_by_category(request, category_id=None):
#     categories = Category.objects.all()
#
#     if category_id:
#         selected_category = get_object_or_404(Category, id=category_id)
#         books = Book.objects.filter(category=selected_category)
#     else:
#         selected_category = None
#         books = Book.objects.all()
#
#     return render(request, 'books/book_list.html', {
#         'categories': categories,
#         'books': books,
#         'selected_category': selected_category
#     })


def home_view(request):
    categories = Category.objects.all()

    # Featured books (3 per category)
    featured_books = {}
    for category in categories:
        books = Book.objects.filter(category=category)[:3]
        if books:
            featured_books[category] = books

    # Top rated books by average review
    top_rated_books = Book.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:3]

    # Most borrowed books
    most_borrowed_books = Book.objects.annotate(
        borrows=Count('orders', filter=Q(orders__order_type='borrow'))
    ).order_by('-borrows')[:3]

    return render(request, 'home.html', {
        'categories': categories,
        'featured_books': featured_books,
        'top_rated_books': top_rated_books,
        'most_borrowed_books': most_borrowed_books,
    })


# def books_by_category(request, category_id=None):
#     categories = Category.objects.all()
#     selected_category = None
#     books = Book.objects.all()
#
#     # Filter by category if provided
#     if category_id is not None:
#         selected_category = get_object_or_404(Category, id=category_id)
#         books = books.filter(category=selected_category)
#
#     # Get filter values from query string
#     price_min = request.GET.get('price_min')
#     price_max = request.GET.get('price_max')
#     book_type = request.GET.get('book_type')
#
#     # Apply price filters if valid
#     try:
#         if price_min:
#             price_min = float(price_min)
#             books = books.filter(price__gte=price_min)
#     except ValueError:
#         price_min = None
#
#     try:
#         if price_max:
#             price_max = float(price_max)
#             books = books.filter(price__lte=price_max)
#     except ValueError:
#         price_max = None
#
#     # Apply book type filter
#     if book_type and book_type != 'all':
#         books = books.filter(book_type=book_type)
#
#     context = {
#         'categories': categories,
#         'selected_category': selected_category,
#         'books': books,
#         'filters': {
#             'price_min': price_min if price_min is not None else '',
#             'price_max': price_max if price_max is not None else '',
#             'book_type': book_type or 'all'
#         }
#     }
#
#     return render(request, 'books/book_list.html', context)

from django.db.models import Q

def books_by_category(request, category_id=None):
    categories = Category.objects.all()
    selected_category = None
    books = Book.objects.all()

    # 🧠 Filter by category if selected
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        books = books.filter(category=selected_category)

    # 🔍 Handle search query
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # 💰 Optional: other filters (price, type)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    book_type = request.GET.get('book_type')

    if price_min:
        books = books.filter(price__gte=price_min)
    if price_max:
        books = books.filter(price__lte=price_max)
    if book_type and book_type != 'all':
        books = books.filter(book_type=book_type)

    return render(request, 'books/book_list.html', {
        'categories': categories,
        'selected_category': selected_category,
        'books': books,
        'filters': {
            'price_min': price_min or '',
            'price_max': price_max or '',
            'book_type': book_type or 'all'
        },
        'search_query': search_query or ''
    })

