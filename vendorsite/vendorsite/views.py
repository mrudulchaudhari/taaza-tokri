from django.shortcuts import render

def index(request):
    return render(request, 'landing.html')

def login_view(request):
    """
    This view will show your login page.
    """
    return render(request, 'login.html')
