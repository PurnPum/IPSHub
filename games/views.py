from django.shortcuts import get_object_or_404, render
from django.db.models import Count, OuterRef, Subquery
from patches.models import Patch, PatchOption
from .models import Game
from categories.models import Category
from patches import add_real_data_to_db
from django.core.paginator import Paginator

def paginate(request, qs, limit=3):
    paginated_qs = Paginator(qs, limit)
    page_no = request.GET.get("page")
    return paginated_qs.get_page(page_no)

def games_list(request):
    
    add_real_data_to_db.clean_db()
    add_real_data_to_db.add_real_games_to_db()
    add_real_data_to_db.add_real_categories_to_db()
    add_real_data_to_db.add_real_patch_options_to_db()
    add_real_data_to_db.add_real_patches_to_db()
    
    patchgen = request.GET.get('patchgen',"False")
    
    return main_filter(request, patchgen=patchgen)

def main_filter_patchgen(request):
    return main_filter(request, patchgen="True")

def main_filter(request,extravars={},html='games/games.html',title='Games',CSS='games',nav_text_color='.text-warning-emphasis',nav_main_color='.bg-success',patchgen="False"):
    
    developer = request.GET.get('selectedDeveloper','any')
    emulator = request.GET.get('selectedEmulator','any')
    type = request.GET.get('selectedType','any')
    sorting_by = request.GET.get('selectedSorting','Patches')
    sorting_order = request.GET.get('sorting_order','descending')
    
    games = Game.objects.all()
    
    if developer and developer != 'any' and developer != 'none':
        games = games.filter(developer=developer)
        
    if emulator and emulator != 'any' and emulator != 'none':
        games = games.filter(best_emulator=emulator)
    
    if type and type != 'any' and type != 'none':
        games = games.filter(type=type)
    
    if sorting_by is None:
        sorting_by = "Patches"
    
    sorting_char = '-'
    
    if sorting_order == 'ascending':
        sorting_char = ''
    
    sorting_method = {
        'Patches': lambda x: x.annotate(num_patches=Count('categories__patchoption__patches')).order_by(sorting_char+'num_patches'),
        'Categories': lambda x: x.annotate(num_categories=Count('categories')).order_by(sorting_char+'num_categories'),
        'Name': lambda x: x.order_by(sorting_char+'title'),
        'Release Date': lambda x: x.order_by(sorting_char+'release_date'),
        'Latest Patch': lambda x: x.annotate(latest_patch=Subquery(Patch.objects.filter(patch_options__category__base_game=OuterRef('pk')).order_by('-creation_date').values('creation_date')[:1])).order_by(sorting_char+'latest_patch')
    }
    games = sorting_method[sorting_by](games)
    paginated_games = paginate(request, games)
    
    final_game_list = []
    for game in paginated_games:
        patches_amount = game.categories.aggregate(Count('patchoption__patches'))['patchoption__patches__count']
        categories_amount = game.categories.count()
        
        last_patch = Patch.objects.filter(patch_options__category__base_game=game).order_by('-creation_date').first()
        category_with_most_patches = game.categories.annotate(num_patches=Count('patchoption__patches')).order_by('-num_patches').first()
        
        final_game_list.append({
            'game': game,
            'patches_amount': patches_amount,
            'categories_amount': categories_amount,
            'last_patch': last_patch,
            'popular_category': category_with_most_patches
        })
    
    top_8_games_with_most_patches = Game.objects.all().annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')
    top_8_developers = list(set(top_8_games_with_most_patches.values_list('developer', flat=True)))[:8]
    
    top_8_emulators = list(set(top_8_games_with_most_patches.values_list('best_emulator', flat=True)))[:8]
    
    top_8_types = list(set(top_8_games_with_most_patches.values_list('type', flat=True)))[:8]
    
    top_5_games_with_the_most_patches = Game.objects.all().annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:5]
    
    most_downloaded_patches = []

    for game in top_5_games_with_the_most_patches:
        most_downloaded_patch = Patch.objects.filter(
            patch_options__category__base_game=game
        ).order_by('-downloads').first()
        
        if most_downloaded_patch:
            most_downloaded_patches.append(most_downloaded_patch)
    
    most_downloaded_patches = sorted(most_downloaded_patches, key=lambda p: p.downloads, reverse=True)
    
    sidebar_patches = []
    
    for patch in most_downloaded_patches:
        
        func_get_parent = lambda c: c.name if (c.parent_category is None) else func_get_parent(c.parent_category)
    
        loop_categories = set([func_get_parent(c) for c in [p.category for p in patch.patch_options.all()]])
        
        categories_string = ", ".join(loop_categories)
        
        game = patch.patch_options.first().category.base_game
        
        sidebar_patches.append({
            'patch': patch,
            'base_game': game,
            'categories': categories_string
        })
    
    top_5_games_with_the_most_categories = Game.objects.all().annotate(num_categories=Count('categories')).order_by('-num_categories')[:5]
    
    categories_with_the_most_patches = []
    
    for game in top_5_games_with_the_most_categories:
        top_category = game.categories.annotate(
            patch_count=Count('patchoption__patches', distinct=True)
        ).order_by('-patch_count').first()
        
        if top_category:
            categories_with_the_most_patches.append((top_category,top_category.patch_count))
            
    top_5_categories_with_the_most_patches = sorted(categories_with_the_most_patches, key=lambda x: x[1], reverse=True)[:5]

    top_5_categories_with_the_most_patches = [category for category, _ in top_5_categories_with_the_most_patches]
    
    sidebar_categories = []
    
    for category in top_5_categories_with_the_most_patches:

        base_game = category.base_game
        
        amount_of_patches_in_category = Patch.objects.filter(patch_options__category=category).count()
        
        latest_patch = Patch.objects.filter(patch_options__category=category).order_by('-creation_date').first()
        
        patch_options_amount = PatchOption.objects.filter(category=category).count()
        
        sidebar_categories.append({
            'category': category,
            'base_game': base_game,
            'patches_amount': amount_of_patches_in_category,
            'latest_patch': latest_patch,
            'patch_options_amount': patch_options_amount
        })
    
    context = {
        'final_list' : final_game_list,
        'paginated_list': paginated_games,
        'top8developers': top_8_developers,
        'top8emulators': top_8_emulators,
        'top8types': top_8_types,
        'sidebar_categories': sidebar_categories,
        'sidebar_patches': sidebar_patches,
        'amountDev': len(top_8_developers),
        'amountEmu': len(top_8_emulators),
        'amountTyp': len(top_8_types),
        'sorting_criteria': ['Patches','Categories','Name','Release Date','Latest Patch'],
        'sorting_by': sorting_by,
        'title': title,
        'CSS': CSS,
        'nav_text_color': nav_text_color,
        'nav_main_color': nav_main_color,
        'patchgen': patchgen,
        'extravars': extravars
    }
    
    return render(request, html, context)

def get_game_list_only_patchgen(request):
    return get_game_list_only(request,patchgen="True")

def get_game_list_only(request,patchgen="False"):
    return main_filter(request, html='games/filters/filter_game_list_scroll.html', patchgen=patchgen)

def load_modal(request):
    html='games/main_modal.html'
    game_id = request.GET.get('selectedGame')
    category_id = request.GET.get('selectedCategory')
    if game_id:
        game = Game.objects.get(id=game_id)
        context = {'element': game}
    elif category_id:
        html = 'games/sidebar/second/sidebar_modal.html'
        category = Category.objects.get(id=category_id)
        game = category.base_game
        context={'element': category, 'hierarchy': get_category_hierarchy(category), 'game': game}
    else:
        context={'element': 'any'}
    return render(request, html, context)

def get_category_hierarchy(category):
    category_hierarchy = {}
    current_category = category
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
    return category_hierarchy

def get_category_children(category):
    children = Category.objects.filter(parent_category=category)
    if len(children) > 0:
        return children
    else:
        return None