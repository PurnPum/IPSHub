from django.shortcuts import get_object_or_404, render
from .models import Category

def categories_list(request):
    return render(request, 'categories/categories_sidebar_layout.html')

