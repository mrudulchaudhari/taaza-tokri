from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def supplier_dashboard(request):
    return render(request, 'supplier/dashboard.html')
