from django.shortcuts import get_object_or_404, render

from core.utils import search_data
from patches.forms import SearchForm
from .models import Category

def categories_list(request):
    return render(request, 'categories/categories_sidebar_layout.html')

def search_categories(request):
    context = search_data(request,Category)
    context.update({'form':SearchForm(request.GET or None)})
    return render(request, 'categories/search/search_query.html', context)