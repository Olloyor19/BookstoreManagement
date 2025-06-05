from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import Order
from .forms import OrderForm
from datetime import timedelta
from django.utils.timezone import now

@login_required
def create_order(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.book = book

            if order.order_type == 'borrow':
                order.due_date = now().date() + timedelta(days=14)  # 2 weeks default

            if order.order_type == 'buy' and order.quantity > book.stock:
                form.add_error('quantity', 'Not enough stock.')
            else:
                book.stock -= order.quantity
                book.save()
                order.save()
                return redirect('my_orders')
    else:
        form = OrderForm(initial={'book': book, 'quantity': 1})

    return render(request, 'orders/create_order.html', {'form': form, 'book': book})


@login_required
def my_orders(request):
    orders = Order.objects.select_related('book').filter(user=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})


