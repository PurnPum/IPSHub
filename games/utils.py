from patches.forms import SearchForm
from django.core.exceptions import FieldError

def get_category_hierarchy(category):
    category_hierarchy = {}
    current_category = category
    if current_category is None:
        return category_hierarchy
    category_hierarchy['element'] = current_category
    category_hierarchy['children'] = []
    while current_category.parent_category is not None:
        parent_category = current_category.parent_category
        child_category = {}
        child_category['element'] = parent_category
        child_category['children'] = []
        child_category['children'].append(category_hierarchy)
        category_hierarchy = child_category
        current_category = parent_category
        if current_category is None:
            break
    return category_hierarchy

def search_data(request,object,order_by='name'):
    form = SearchForm(request.GET or None)
    query = request.GET.get('query', '')
    try:
        elements = object.objects.filter(name__icontains=query).order_by(order_by) if query else object.objects.none()
    except FieldError:
        elements = object.objects.filter(title__icontains=query).order_by(order_by) if query else object.objects.none()
    context = {
        'form': form,
        'query': query,
        'elements': elements,
    }
    return context