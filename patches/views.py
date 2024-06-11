from django.shortcuts import render
from .models import Patch, PatchOption
from categories.models import Category
from . import add_junk_to_db, add_real_data_to_db

def patches_list(request):
    
    add_junk_to_db.clean_db()
    add_real_data_to_db.add_real_games_to_db()
    add_real_data_to_db.add_real_categories_to_db()
    add_real_data_to_db.add_real_patch_options_to_db()
    add_real_data_to_db.add_real_patches_to_db()
    
    patches = Patch.objects.all()
    patch_list = []
    for patch in patches:
        patch_options = patch.patch_options.all()
        categories = [p.category for p in patch_options]
        games = set(category.base_game for category in categories)
        
        if len(games) == 1:
            game = games.pop()
        else:
            game = None  # TODO
        
        func_get_parent = lambda c: c.name if (c.parent_category is None) else func_get_parent(c.parent_category)
    
        categories = set([func_get_parent(c) for c in categories])
        
        categories_string = ", ".join(categories)
        
        patch_list.append({
            'patch': patch,
            'game': game,
            'categories': categories_string
        })
   
    return render(request, 'patches/patches.html', {'patches': patch_list})
