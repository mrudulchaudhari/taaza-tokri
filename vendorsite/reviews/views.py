# reviews/views.py (FIXED VERSION)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import json

from .models import Review, ReviewResponse, ReviewHelpful
from .forms import ReviewForm, ReviewFilterForm

# Use get_user_model() instead of importing User directly
User = get_user_model()


@login_required
def add_review(request, user_id):
    reviewee = get_object_or_404(User, id=user_id)
    
    # Determine user types - customize this based on your user model structure
    # You might need to adjust this logic based on how you identify vendors vs suppliers
    def get_user_type(user):
        # Option 1: If you have user.user_type field
        if hasattr(user, 'user_type'):
            return user.user_type
        
        # Option 2: If you have separate profile models
        if hasattr(user, 'vendor_profile'):
            return 'vendor'
        elif hasattr(user, 'supplier_profile'):
            return 'supplier'
        
        # Option 3: If you have groups
        if user.groups.filter(name='vendors').exists():
            return 'vendor'
        elif user.groups.filter(name='suppliers').exists():
            return 'supplier'
        
        # Default fallback
        return 'vendor'
    
    reviewer_type = get_user_type(request.user)
    reviewee_type = get_user_type(reviewee)
    
    if request.user == reviewee:
        messages.error(request, "You cannot review yourself.")
        return redirect('reviews:user_reviews', user_id=user_id)
    
    existing_review = Review.objects.filter(reviewer=request.user, reviewee=reviewee).first()
    if existing_review:
        messages.error(request, "You have already reviewed this user.")
        return redirect('reviews:user_reviews', user_id=user_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = reviewee
            review.reviewer_type = reviewer_type
            review.reviewee_type = reviewee_type
            review.save()
            
            messages.success(request, "Review submitted successfully!")
            return redirect('reviews:user_reviews', user_id=user_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'reviewee': reviewee,
        'reviewee_type': reviewee_type,
    })


def user_reviews(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Use the same user type detection function
    def get_user_type(user):
        if hasattr(user, 'user_type'):
            return user.user_type
        if hasattr(user, 'vendor_profile'):
            return 'vendor'
        elif hasattr(user, 'supplier_profile'):
            return 'supplier'
        if user.groups.filter(name='vendors').exists():
            return 'vendor'
        elif user.groups.filter(name='suppliers').exists():
            return 'supplier'
        return 'vendor'
    
    user_type = get_user_type(user)
    
    filter_form = ReviewFilterForm(request.GET)
    reviews = Review.objects.filter(
        reviewee=user,
        reviewee_type=user_type,
        status='approved'
    ).select_related('reviewer')
    
    if filter_form.is_valid():
        if filter_form.cleaned_data['rating']:
            reviews = reviews.filter(rating=filter_form.cleaned_data['rating'])
        sort_by = filter_form.cleaned_data['sort_by'] or '-created_at'
        reviews = reviews.order_by(sort_by)
    
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    stats = Review.get_user_stats(user, user_type)
    can_review = (request.user.is_authenticated and 
                 request.user != user and 
                 not Review.objects.filter(reviewer=request.user, reviewee=user).exists())
    
    return render(request, 'reviews/user_reviews.html', {
        'user': user,
        'user_type': user_type,
        'reviews': page_obj,
        'stats': stats,
        'filter_form': filter_form,
        'can_review': can_review,
    })


@login_required
@require_POST
def add_review_response(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user != review.reviewee:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if hasattr(review, 'response'):
        return JsonResponse({'error': 'Response already exists'}, status=400)
    
    try:
        data = json.loads(request.body)
        response_text = data.get('response', '').strip()
        
        if not response_text:
            return JsonResponse({'error': 'Response cannot be empty'}, status=400)
        
        response = ReviewResponse.objects.create(
            review=review,
            responder=request.user,
            response=response_text
        )
        
        return JsonResponse({
            'success': True,
            'response': {
                'id': response.id,
                'response': response.response,
                'created_at': response.created_at.strftime('%B %d, %Y'),
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def mark_review_helpful(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.user == review.reviewer:
        return JsonResponse({'error': 'Cannot mark your own review'}, status=400)
    
    try:
        data = json.loads(request.body)
        is_helpful = data.get('is_helpful', True)
        
        # Determine user type
        def get_user_type(user):
            if hasattr(user, 'user_type'):
                return user.user_type
            if hasattr(user, 'vendor_profile'):
                return 'vendor'
            elif hasattr(user, 'supplier_profile'):
                return 'supplier'
            if user.groups.filter(name='vendors').exists():
                return 'vendor'
            elif user.groups.filter(name='suppliers').exists():
                return 'supplier'
            return 'vendor'
        
        user_type = get_user_type(request.user)
        
        helpful_vote, created = ReviewHelpful.objects.get_or_create(
            review=review,
            user=request.user,
            defaults={'user_type': user_type, 'is_helpful': is_helpful}
        )
        
        if not created:
            helpful_vote.is_helpful = is_helpful
            helpful_vote.save()
        
        helpful_count = review.helpful_votes.filter(is_helpful=True).count()
        
        return JsonResponse({
            'success': True,
            'helpful_count': helpful_count,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_user_stats(request, user_id):
    """API endpoint to get user review stats"""
    user = get_object_or_404(User, id=user_id)
    
    def get_user_type(user):
        if hasattr(user, 'user_type'):
            return user.user_type
        if hasattr(user, 'vendor_profile'):
            return 'vendor'
        elif hasattr(user, 'supplier_profile'):
            return 'supplier'
        if user.groups.filter(name='vendors').exists():
            return 'vendor'
        elif user.groups.filter(name='suppliers').exists():
            return 'supplier'
        return 'vendor'
    
    user_type = get_user_type(user)
    stats = Review.get_user_stats(user, user_type)
    return JsonResponse(stats)