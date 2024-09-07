import re
import unicodedata

from core import add_real_data_to_db

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

def normalize_query(query):
    normalized = unicodedata.normalize('NFKD', query)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def normalize_string(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    s = re.sub(r'[^\w\s]', '', s).lower()
    return s

def search_data(request,object,order_by='name'):
    query = request.GET.get('query', '')
    normalized_query = normalize_query(query)
    elements = object.objects.filter(normalized_name__icontains=normalized_query).order_by(order_by) if normalized_query else object.objects.none()
    context = {
        'query': query,
        'elements': elements,
    }
    return context

def add_data_to_bd():
    add_real_data_to_db.clean_db()
    add_real_data_to_db.add_users()
    add_real_data_to_db.add_real_games_to_db()
    add_real_data_to_db.add_real_categories_to_db()
    add_real_data_to_db.add_real_patch_options_to_db()
    add_real_data_to_db.add_real_fields_to_db()
    add_real_data_to_db.add_real_patches_to_db()
    add_real_data_to_db.add_real_diff_files_to_db()