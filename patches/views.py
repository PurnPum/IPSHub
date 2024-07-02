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

def main_filter(request,htmlkey,sorting_order='descending',extravars={},game_id=None,category_id=None,patch_id=None,sorting_by=None):
    
    htmls = {'all': 'patches/patches.html', 'base_game': 'filters/filter.html' , 'category': 'filters/filter_patches_and_main.html', 'base_patch': 'filters/filter_main.html', 'patch_list_page': 'filters/filter_patch_list_no_oob.html'}
    html = htmls['all']
    
    sorting_criteria = {'Downloads': 'downloads', 'Favorites': 'favorites', 'Creation Date': 'creation_date', 'Name': 'name', 'Sub-patches': 'subpatches'}
    
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
    
    try:
        html = htmls[htmlkey]
    except:
        print("Error in htmlkey: " + htmlkey)
        
    patch_list = patch_list.distinct()
    
    if sorting_by is None or sorting_by not in sorting_criteria.keys():
        sorting_by = list(sorting_criteria.keys())[0]
    
    sorting_char = '-'
    
    if sorting_order == 'ascending':
        sorting_char = ''
    
    if sorting_by == 'Sub-patches':
        patch_list = patch_list.annotate(subpatch_count=Count('subpatches')).order_by(sorting_char+'subpatch_count')
    else:
        patch_list = patch_list.order_by(sorting_char+sorting_criteria[sorting_by])
    
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
    
    top_5_games = Game.objects.annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:5]
    
    sidebar_games = []
    
    for game in top_5_games:
        game_patches = Patch.objects.filter(patch_options__category__base_game=game)
        game_patches_amount = game_patches.count()
        game_categories_amount = game.categories.count()
        latest_patch = game_patches.order_by('-creation_date').first().creation_date
        sidebar_games.append({
            'game': game,
            'patches_amount': game_patches_amount,
            'latest_patch': latest_patch,
            'categories_amount': game_categories_amount
        })
    
    top_5_categories = categories.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:5]
    
    sidebar_categories = []
    
    for category in top_5_categories:
        category_patches = Patch.objects.filter(patch_options__category=category)
        category_patches_amount = category_patches.count()
        base_game = category.base_game
        latest_patch = category_patches.order_by('-creation_date').first().creation_date
        patch_options_amount = category.patchoption_set.count()
        sidebar_categories.append({
            'category': category,
            'patches_amount': category_patches_amount,
            'latest_patch': latest_patch,
            'base_game': base_game,
            'patch_options_amount': patch_options_amount
        })
    
        
    context = {
        'patches' : final_patch_list,
        'paginated_patches': paginated_patches,
        'top8categories': top_8_categories,
        'top8parentpatches': top_8_parent_patches,
        'top8games': top_8_games,
        'sidebar_categories': sidebar_categories,
        'sidebar_games': sidebar_games,
        'amountCat': len(top_8_categories),
        'amountPat': len(top_8_parent_patches),
        'sorting_criteria': sorting_criteria,
        'extravars': extravars
    }
    
    return render(request, html, context)

def filter(request, htmlkey=None, extravars={}):
    game_id = request.GET.get('selectedGame','any')
    category_id = request.GET.get('selectedCategory','any')
    patch_id = request.GET.get('selectedPatch','any')
    sorting_by = request.GET.get('selectedSorting','Downloads')
    sorting_order = request.GET.get('sorting_order','descending')
    
    if htmlkey is None:
        if game_id in ['none', 'any']:
            htmlkey = 'all'
        elif category_id in ['none', 'any']:
            htmlkey = 'base_game'
        elif patch_id in ['none', 'any']:
            htmlkey = 'category'
        else:
            htmlkey = 'base_patch'
    
    return main_filter(request, htmlkey, sorting_order, extravars=extravars, game_id=game_id, category_id=category_id, patch_id=patch_id, sorting_by=sorting_by)

def get_patch_list_only(request):
    display_mode = request.GET.get('display_mode')
    return filter(request, 'patch_list_page', {'display_mode': display_mode})