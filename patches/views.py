from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Patch
from categories.models import Category
from games.models import Game
from . import add_real_data_to_db
from django.core.paginator import Paginator

def paginate(request, qs, limit=4):
    paginated_qs = Paginator(qs, limit)
    page_no = request.GET.get("page")
    return paginated_qs.get_page(page_no)

def patches_list(request):
    
    add_real_data_to_db.clean_db()
    add_real_data_to_db.add_real_games_to_db()
    add_real_data_to_db.add_real_categories_to_db()
    add_real_data_to_db.add_real_patch_options_to_db()
    add_real_data_to_db.add_real_patches_to_db()
    
    return main_filter(request, 'all')

def main_filter(request,htmlkey,extravars={},game_id=None,category_id=None,patch_id=None):
    
    htmls = {'all': 'patches/patches.html', 'base_game': 'filters/filter.html' , 'category': 'filters/filter_patches_and_main.html', 'base_patch': 'filters/filter_main.html', 'patch_list_page': 'filters/filter_patch_list_no_oob.html'}
    html = htmls['all']
    
    categories = Category.objects.all()
    patches = Patch.objects.all()
    patch_list = Patch.objects.all()

    if game_id and game_id != 'any' and game_id != 'none':
        patch_list = patch_list.filter(patch_options__category__base_game_id=game_id)
        patches = patches.filter(patch_options__category__base_game_id=game_id)
        categories = categories.filter(base_game_id=game_id)
    
    if category_id and category_id != 'none' and category_id != 'any':
        patch_list = patch_list.filter(patch_options__category_id=category_id)
        patches = patches.filter(patch_options__category_id=category_id)

    if patch_id and patch_id != 'none' and patch_id != 'any':
        patch_list = patch_list.filter(parent_patch__id=patch_id)
        html = htmls['patch_list']
        
    try:
        html = htmls[htmlkey]
    except:
        print("Error in htmlkey: " + htmlkey)
        
    patch_list = patch_list.distinct()
    
    paginated_patches = paginate(request, patch_list)
    
    final_patch_list = []
    for patch in paginated_patches:
        patch_options = patch.patch_options.all()
        loop_categories = [p.category for p in patch_options]
        games = set(category.base_game for category in loop_categories)
        
        if len(games) == 1:
            game = games.pop()
        else:
            game = None  # TODO
        
        func_get_parent = lambda c: c.name if (c.parent_category is None) else func_get_parent(c.parent_category)
    
        loop_categories = set([func_get_parent(c) for c in loop_categories])
        
        categories_string = ", ".join(loop_categories)
        
        final_patch_list.append({
            'patch': patch,
            'game': game,
            'categories': categories_string         
        })
    
    top_8_games = Game.objects.annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:8]
    
    top_8_categories = categories.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    
    top_8_parent_patches = patches.annotate(subpatch_count=Count('subpatches')).filter(subpatch_count__gt=0).order_by('-subpatch_count')[:8]
    
    context = {
        'patches' : final_patch_list,
        'paginated_patches': paginated_patches,
        'top8categories': top_8_categories,
        'top8parentpatches': top_8_parent_patches,
        'top8games': top_8_games,
        'amountCat': len(top_8_categories),
        'amountPat': len(top_8_parent_patches),
        'extravars': extravars
    }
    
    return render(request, html, context)

def filter(request, htmlkey=None, extravars={}):
    game_id = request.GET.get('selectedGame','any')
    category_id = request.GET.get('selectedCategory','any')
    patch_id = request.GET.get('selectedPatch','any')
    print(game_id, category_id, patch_id)
    if htmlkey is None:
        if game_id == 'any' or category_id == 'any':
            htmlkey = 'base_game'
        elif patch_id == 'any':
            htmlkey = 'category'
        else:
            htmlkey = 'base_patch'
    return main_filter(request, htmlkey, extravars=extravars, game_id=game_id, category_id=category_id, patch_id=patch_id)

def get_patch_list_only(request):
    display_mode = request.GET.get('display_mode')
    return filter(request, 'patch_list_page', {'display_mode': display_mode})