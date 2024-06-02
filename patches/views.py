from django.shortcuts import render
from .models import Patch, PatchOption

def patches_list(request):
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
        
        categories = [c.name for c in categories if c.parent_category is None]
        
        categories_string = ", ".join(categories)
        
        patch_list.append({
            'patch': patch,
            'game': game,
            'categories': categories_string
        })
    
    return render(request, 'patches/patches.html', {'patches': patch_list})
