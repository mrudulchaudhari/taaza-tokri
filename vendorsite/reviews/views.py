# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ReviewForm
from .models import Review
from supplier.models import Order

User = get_user_model()

@login_required
def add_review(request, order_id, reviewee_id):
    order = get_object_or_404(Order, id=order_id)
    reviewee = get_object_or_404(User, id=reviewee_id)
    
    is_vendor_of_order = (order.user == request.user)
    is_supplier_of_order = order.items.filter(product__supplier__user=request.user).exists()

    if not (is_vendor_of_order or is_supplier_of_order):
        messages.error(request, "You are not authorized to review this order.")
        return redirect('landing')

    if order.status != 'Delivered':
        messages.error(request, "You can only review delivered orders.")
        return redirect('vendor:order_history' if is_vendor_of_order else 'supplier:dashboard')

    if Review.objects.filter(order=order, reviewer=request.user, reviewee=reviewee).exists():
        messages.warning(request, "You have already submitted a review for this order.")
        return redirect('vendor:order_history' if is_vendor_of_order else 'supplier:dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('vendor:order_history' if is_vendor_of_order else 'supplier:dashboard')
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'order': order,
        'reviewee': reviewee
    }
    return render(request, 'reviews/add_review.html', context)


# --- NEW VIEW TO DISPLAY RECEIVED REVIEWS ---
@login_required
def user_reviews(request):
    """
    Displays a list of all reviews that the currently logged-in user has received.
    """
    received_reviews = Review.objects.filter(reviewee=request.user).select_related(
        'reviewer', 'order'
    ).order_by('-created_at')
    
    context = {
        'reviews': received_reviews
    }
    return render(request, 'reviews/user_reviews.html', context)
