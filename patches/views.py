from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Patch, PatchOption
from categories.models import Category
from games.models import Game
from . import add_real_data_to_db

def patches_list(request):
    
    add_real_data_to_db.clean_db()
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
        
    top_8_games = Game.objects.annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:8]
    top_8_categories = Category.objects.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    top_8_parent_patches = Patch.objects.annotate(subpatch_count=Count('subpatches')).filter(subpatch_count__gt=0).order_by('-subpatch_count')[:8]
    context = {'patches': patch_list, 'top8games': top_8_games, 'top8categories': top_8_categories, 'top8parentpatches': top_8_parent_patches, 'amountCat': len(top_8_categories), 'amountPat': len(top_8_parent_patches)}

    return render(request, 'patches/patches.html', context)

# Endpoint to filter out categories for a given game and return the top 8 categories based on the amount of patches associated with them, used in the dropdown menus.
def filter_categories(request):
    game_id = request.GET.get('selectedGame', None)
    if game_id and game_id != 'any':
        categories = Category.objects.filter(base_game__id=game_id).annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    else:
        categories = Category.objects.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    try:
        return render(request, 'filters/filter_categories.html', {'top8categories': categories, 'amountCat': len(categories)})
    except IOError:
        return HttpResponseNotFound('<h1>File does not exist</h1>')

# Endpoint to filter out patches for a given category and return the top 8 patches based on the amount of subpatches associated with them, used in the dropdown menus.
def filter_patches(request):
    category_id = request.GET.get('selectedCategory', None)
    patches = Patch.objects.all()

    if category_id and category_id != 'any':
        patches = patches.filter(patch_options__category_id=category_id).annotate(subpatch_count=Count('subpatches')).filter(subpatch_count__gt=0).order_by('-subpatch_count')[:8]

    else:
        patches = patches.annotate(subpatch_count=Count('subpatches')).filter(subpatch_count__gt=0).order_by('-subpatch_count')[:8]
    try:
        return render(request, 'filters/filter_patches.html', {'top8parentpatches': patches,})
    except IOError:
        return HttpResponseNotFound('<h1>File does not exist</h1>')
    
def filter_categories_and_patches(request):
    game_id = request.GET.get('selectedGame')
    categories = Category.objects.all()
    patches = Patch.objects.all()
    
    if game_id and game_id != 'any':
        categories = categories.filter(base_game_id=game_id)
    categories = categories.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    
    if game_id and game_id != 'any':
        patches = patches.filter(patch_options__category__base_game_id=game_id)
    patches = patches.annotate(subpatch_count=Count('subpatches')).filter(subpatch_count__gt=0).order_by('-subpatch_count')[:8]

    return render(request, 'filters/filter_categories_and_patches.html', {
        'top8categories': categories,
        'top8parentpatches': patches,
        'amountCat': len(categories),
        'amountPat': len(patches)
    })
