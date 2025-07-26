from django.shortcuts import render

def login_view(request):
    """
    This view will show your login page.
    """
    return render(request, 'login.html')
