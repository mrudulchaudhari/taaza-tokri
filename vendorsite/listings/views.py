from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def list_materials(request):
    return render(request, 'listings/list.html')
