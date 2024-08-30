from django.shortcuts import get_object_or_404, render

from games.utils import search_data
from .models import Category

def categories_list(request):
    return render(request, 'categories/categories_sidebar_layout.html')

def search_categories(request):
    return render(request, 'categories/search/search_query.html', search_data(request,Category))