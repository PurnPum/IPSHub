import datetime, json, time
from django.db import IntegrityError, transaction
from django.forms import ValidationError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, OuterRef, Subquery, Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache

from games.views import get_category_hierarchy, main_filter as g_main_filter
from patches.forms import DynamicPatchForm
from .models import Patch, PatchFav, PatchOption, POField, PatchData, DiffFile, PatchComment, PatchCommentLike, get_hash_code_from_patchDatas
from categories.models import Category
from games.models import Game
from . import add_real_data_to_db

import os
import subprocess

def add_data_to_bd():
    add_real_data_to_db.clean_db()
    add_real_data_to_db.add_real_games_to_db()
    add_real_data_to_db.add_real_categories_to_db()
    add_real_data_to_db.add_real_patch_options_to_db()
    add_real_data_to_db.add_real_fields_to_db()
    add_real_data_to_db.add_real_patches_to_db()
    add_real_data_to_db.add_real_diff_files_to_db()

def paginate(request, qs, limit=4):
    paginated_qs = Paginator(qs, limit)
    page_no = request.GET.get("page")
    return paginated_qs.get_page(page_no)

def patch_generator(request):
    
    extravars = {
        'title': 'Patch Generator',
        'CSS': 'patchgen',
        'nav_text_color': '.text-danger-emphasis',
        'nav_main_color': '.custom-navbar-darker-bg',
        'patchgen': 'True'
    }
    
    game_id = request.GET.get('selectedGame')
    patch_id = request.GET.get('selectedPatch')
    category_id = request.GET.get('selectedCategory')
    
    context = {}
    
    if category_id is not None:
        extra_cats = Category.objects.get(id=category_id)
        extravars.update({'selected_category': extra_cats})
    if patch_id is not None:
        game_id = Patch.objects.get(id=patch_id).get_base_game().id
        patch = Patch.objects.get(id=patch_id)
        context.update({'patch': patch})
        patch_datas = PatchData.objects.filter(patch=patch)
        extra_cats = Category.objects.filter(id__in=patch_datas.values_list('field__patch_option__category', flat=True).distinct())
        extravars.update({'modified_categories': extra_cats})
    if game_id is not None:
        game=Game.objects.get(id=game_id)
        patches = get_top_5_patches_by_subpatches(game_id)
        
        children_categories = get_all_categories_from_game_by_parents(game_id=game_id)
        
        func_get_parent = lambda c: c if (c.parent_category is None) else func_get_parent(c.parent_category)
        top_5_patches = []
        for patch in patches:
            subpatches_amount = patch.subpatches.count()
            patch_options = patch.patch_options.all()
            categories = list(set([func_get_parent(p.category) for p in patch_options]))
            top_5_patches.append({'patch': patch, 'subpatches_amount': subpatches_amount, 'categories': categories})
            
        extravars['patch_options_list_nav_id'] = 'patch_options_list_nav_primary'
        extravars['primary'] = 'True'
        
        context.update({
            'children_categories': children_categories,
            'top_5_patch_list': top_5_patches,
            'game': game,
            'extravars':extravars})
        
        return render(request, 'patch_generator/patch_generator.html', context)
    else:
        return g_main_filter(request, html='patch_generator/game_select/patchgen_select_game.html', extravars=extravars)

def patch_generator_load_data(request):
    patch_id = request.GET.get('patch')
    if patch_id is not None:
        patch = Patch.objects.get(id=patch_id)
    else:
        patch=None
    parent_id = request.GET.get('parent')
    parental_tree = get_category_parent_tree(Category.objects.get(id=parent_id))
    children_categories = get_all_categories_from_game_by_parents(parent_id=parent_id)
    patch_options = get_patch_options_from_category(parent_id)
    po_fields = POField.objects.filter(patch_option__in=patch_options)

    forms = [DynamicPatchForm(patch_options=[po],patch=patch) for po in patch_options]
 
    patch_option_data = { patch_option:fields for patch_option,fields in
                              [(po,
                                [field for field in po_fields.filter(patch_option_id=po.id)]
                                ) for po in patch_options]}
 
    context={
        'patch': patch,
        'patch_option_data_forms': zip(forms, patch_option_data),
        'parental_tree': parental_tree,
        'children_categories': children_categories,
        
        'extravars':{
            'patch_options_list_nav_id': 'patch_options_list_nav_'+parent_id,
            'patch_options_list_data_id': 'patch_options_list_data_'+parent_id,
            'patch_options_subcategories_div_id': 'patch_options_subcategories_div_'+parent_id,
        }
    }
    
    return render(request, 'patch_generator/patch_options_list/patch_options_load_data.html', context)

def get_progress_percentile(request):
    progress_ck = f'progress_{request.user.id}'
    current_task_ck = f'current_task_{request.user.id}'
    return render(request, 'patch_generator/main_progress_bar_animation.html', {'progress': cache.get(progress_ck, 0), 'current_task': cache.get(current_task_ck, '...')})

def get_progress_bar(request):
    return render(request, 'patch_generator/modal_progress_bar.html')

def gather_form_data(request):
    
    progress_ck = f'progress_{request.user.id}' # We're going to use local cache in the developing environment. On production, this should be a Redis cache
    current_task_ck = f'current_task_{request.user.id}'
    cache.set(progress_ck, 0)
    cache.set(current_task_ck, 'Loading patch data...')
    
    patch_name = request.POST.get('patchName')
    
    patch_exists = Patch.objects.filter(name=patch_name).exists()
    if patch_exists:
        patchgen_error = 'Could not create patch: Patch with the same name already exists.'
        context = {
            'error_message': patchgen_error
        }
        return render(request,'generic/modal/modal_patchgen_error.html', context)
    
    patch_options_ids = request.POST.getlist('patch_option_ids')
    patch_options = PatchOption.objects.filter(id__in=patch_options_ids)
    patchgen_error = ""
    cache.set(progress_ck, 2)
    cache.set(current_task_ck, 'Loading form data...')
        
    if patch_options and len(patch_options) > 0:
        forms = [DynamicPatchForm(request.POST, patch_options=[po], patch=None) for po in patch_options]
        cache.set(progress_ck, 4)
        cache.set(current_task_ck, 'Validating forms...')
        if any([not form.is_valid() for form in forms]):
            print("INVALID FORM")
            patchgen_error = "Invalid form: " + form
        else:
            list_patchless_data = []
            for form in forms:
                try:
                    patchless_data = form.patchless()
                except ValidationError as e:
                    continue
                if patchless_data and len(patchless_data) > 0:
                    list_patchless_data.append(patchless_data)
            list_patchless_data = [item for sublist in list_patchless_data for item in sublist]
            if len(list_patchless_data) == 0:
                patchgen_error = 'Error: No configuration selected'
                context = {
                    'error_message': patchgen_error
                }
                return render(request,'generic/modal/modal_patchgen_error.html', context)
            cache.set(progress_ck, 7)
            cache.set(current_task_ck, 'Creating objects...')
            temporal_hash = get_hash_code_from_patchDatas(list_patchless_data)
            if not is_duplicated_temporal_hash(temporal_hash):
                with transaction.atomic():
                    patch = generate_patch_object(request,patch_options,forms)
                    cache.set(progress_ck, 15)
                    cache.set(current_task_ck, 'Beggining patch generation...')
                if isinstance(patch, Patch):
                    base_game = patch.get_base_game()
                    error_message = generate_real_patch(request,patch,base_game)
                    if error_message is not None:
                        context = {
                            'error_message': error_message
                        }
                        return render(request,'generic/modal/modal_patchgen_error.html', context)
                    context = {
                        'element': patch,
                        'patch_config': { po: PatchData.objects.filter(patch=patch, field__patch_option=po) for po in patch_options },
                        'game': patch.get_base_game(),
                        'patchgen': 'True',
                        'in_patchgen': 'True'
                    }
                    cache.set(progress_ck, 100)
                    cache.set(current_task_ck, 'Finalizing...')

                    return render(request, 'generic/modal/modal_patchgen_result.html', context)
                else:
                    patchgen_error = str(patch)
            else:
                existing_patch = Patch.objects.get(patch_hash=temporal_hash)
                context = {
                    'element': existing_patch,
                    'patch_config': { po: PatchData.objects.filter(patch=existing_patch, field__patch_option=po) for po in patch_options },
                    'game': existing_patch.get_base_game(),
                    'duplicated': 'True',
                    'in_patchgen': 'True'
                }
                return render(request,'generic/modal/modal_patchgen_result.html', context)

    context = {
        'error_message': patchgen_error
    }
    return render(request,'generic/modal/modal_patchgen_error.html', context)
                
@transaction.atomic
def generate_patch_object(request,patch_options,forms):
    patch = Patch()
    patch.name = request.POST.get('patchName')
    patch.downloads = 0
    patch.favorites = 0
    if request.user.is_authenticated:
        patch.creator = request.user
    else:
        patch.creator = User.objects.get(username='anonymous')
    patch.creation_date = datetime.date.today()
    patch.download_link = 'TEMPORAL_PLACEHOLDER'
    patch.save()
    saved_forms = 0
    for form in forms:
        try:
            saved_forms += 1
            form.save(patch)
        except:
            continue
    if saved_forms == 0:
        raise ValidationError('All fields have their default value')
    patch.patch_options.set(PatchOption.objects.filter(id__in=[po.id for po in patch_options]))
    patch.full_clean()
    patch.patch_hash = patch.generate_patch_code()
    patch.save()
    return patch

def generate_real_patch(request, patch, game):
    progress_ck = f'progress_{request.user.id}'
    current_task_ck = f'current_task_{request.user.id}'
    # Define paths
    repo_url = game.repository
    repo_dir = settings.CLONE_DIR
    output_diff = os.path.join(settings.PATCH_ROOT, f'{patch.id}.xdelta')
     
    # Cleanup
    try:
        clean_up_dir(repo_dir)
    except Exception as e:
        print(str(e))
     
    # Define the path to the shell script
    clone_repo_script = os.path.join(settings.BASE_DIR, 'static/code/clone_repository.sh')
    make_script = os.path.join(settings.BASE_DIR, 'static/code/make.sh')
    apply_diff_script = os.path.join(settings.BASE_DIR, 'static/code/apply_diff.sh')
    generate_patch_script = os.path.join(settings.BASE_DIR, 'static/code/generate_patch.sh')
    verify_rename_script = os.path.join(settings.BASE_DIR, 'static/code/verify_rename.sh')

    patch_datas = PatchData.objects.filter(patch=patch) # All patch datas are the ones recently created, so no extra filtering needed
    
    diff_files = []
    for pd in patch_datas:
        
        dfs = DiffFile.objects.filter(field=pd.field)
        for df in dfs.filter(trigger_value=pd.data):
            diff_files.append(df)
            
    original_files = ','.join([str(settings.CLONE_DIR / df.original_file) for df in diff_files])
    filenames = ','.join([str(settings.DIFF_ROOT / df.filename) for df in diff_files])

    # Run the shell script with the necessary arguments
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    data = [{'args':[clone_repo_script, repo_url, repo_dir],'progress': 25, 'current_task': "Cloning repository of the game...", 'error_msg': "Internal error while cloning the original game's repository"},
            {'args':[make_script, game.patch_file_name, repo_dir],'progress': 32, 'current_task': "Building original game...", 'error_msg': "Internal error while building the original game"},
            {'args':[verify_rename_script, game.patch_file_name, repo_dir, game.patch_sha],'progress': 38, 'current_task': "Verifying built files...", 'error_msg': "Internal error while verifying the built files"},
            {'args':[apply_diff_script, original_files, filenames, repo_dir],'progress': 56, 'current_task': "Applying selected configurations to the game...", 'error_msg': "Internal error while applying all the changes to the original game code."},
            {'args':[make_script, game.patch_file_name, repo_dir],'progress': 78, 'current_task': "Building modified game...", 'error_msg': "Internal error while building the modified game"},
            {'args':[generate_patch_script, output_diff, game.patch_file_name, repo_dir],'progress': 95, 'current_task': "Creating patch file...", 'error_msg': "Internal error while creating the patch file"}
            ]
    
    with open(settings.LOGS_DIR / str(str(patch.id) + '-' + current_datetime + '.log'), 'w') as f:
        error_message = None
        
        for step in data:
            error_message = run_subprocess(step['args'],f,patch,progress_ck,current_task_ck,step['progress'],step['error_msg'],step['current_task'])
            if error_message is not None:
                return error_message

    # Save the diff file path to the Patch model
    patch.download_link = output_diff
    patch.save()
    
    clean_up_dir(repo_dir)

def clean_up_dir(repo_dir):
    subprocess.run(['rm', '-rf', repo_dir])
    
def run_subprocess(list_args,f,patch,progress_ck,current_task_ck,progress,error_msg,current_task):
    cache.set(progress_ck, progress)
    cache.set(current_task_ck, current_task)
    try:
        subprocess.run(
            ['bash', *list_args],
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True
        )
    except subprocess.CalledProcessError:
        patch.delete()
        error_message = error_msg
        return error_message


def is_duplicated_temporal_hash(hash):
    return Patch.objects.filter(patch_hash=hash).exists()

def get_category_parent_tree(category,result=[]):
    if category.parent_category is None:
        return result
    else:
        return get_category_parent_tree(category.parent_category, result=[category]+result)

def get_patch_options_from_category(category_id):
    return PatchOption.objects.filter(category_id=category_id)

def get_top_5_patches_by_subpatches(game_id):
    patches = Patch.objects.filter(patch_options__category__base_game_id=game_id)
    sorted_patches = patches.annotate(subpatch_count=Count('subpatches')).order_by('-subpatch_count')
    return sorted_patches[:5]

def get_all_categories_from_game_by_parents(game_id=None,parent_id=None):
    if parent_id:
        categories = Category.objects.all().filter(parent_category=parent_id)
    elif game_id:
        categories = Category.objects.all().filter(base_game_id=game_id).filter(parent_category=parent_id)
    else:
        print("Error, neither game nor category provided")
        return None
    return categories

def patches(request):

    game_id = request.GET.get('selectedGame','any')
    category_id = request.GET.get('selectedCategory','any')
    patch_id = request.GET.get('selectedPatch','any')
    sorting_by = request.GET.get('selectedSorting','Downloads')
    sorting_order = request.GET.get('sorting_order','descending')
    
    return main_filter(request, 'all', sorting_order=sorting_order, game_id=game_id, category_id=category_id, patch_id=patch_id, sorting_by=sorting_by)

def main_filter(request,htmlkey,sorting_order='descending',extravars=None,game_id=None,category_id=None,patch_id=None,sorting_by=None):
    
    default_extravars = {'title':'Patches','CSS':'patches','nav_text_color':'.text-info','nav_main_color':'.bg-primary'}

    if extravars is None:
        extravars = {}

    merged_extravars = {**default_extravars, **extravars}
    
    htmls = {'all': 'patches/patches.html', 'base_game': 'patches/filters/filter_categories_patches_and_main.html' , 'category': 'patches/filters/filter_patches_and_main.html', 'base_patch': 'patches/filters/element/filter_main.html', 'patch_list_page': 'patches/filters/element/filter_main_scroll.html'}
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
        subpatch_count = patch.subpatches.count()
        
        if len(games) == 1:
            game = games.pop()
        else:
            game = None  # TODO
        
        func_get_parent = lambda c: c if (c.parent_category is None) else func_get_parent(c.parent_category)
    
        loop_categories = list(set([func_get_parent(c) for c in loop_categories]))
        
        final_patch_list.append({
            'patch': patch,
            'game': game,
            'categories': loop_categories,
            'subpatches_amount': subpatch_count
        })
    
    top_8_games = Game.objects.annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:8]
    
    top_8_categories = categories.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:8]
    
    subpatches_in_patch_list = patches.filter(parent_patch=OuterRef('pk'), id__in=patch_list).values('id')

    top_8_parent_patches = patches.annotate(
        subpatch_count=Count(Subquery(subpatches_in_patch_list))
    ).filter(
        subpatch_count__gt=0
    ).order_by('-subpatch_count')[:8]
    
    top_5_games = Game.objects.annotate(num_patches=Count('categories__patchoption__patches')).order_by('-num_patches')[:5]
    
    sidebar_games = []
    
    for game in top_5_games:
        game_patches = Patch.objects.filter(patch_options__category__base_game=game)
        game_patches_amount = game_patches.count()
        game_categories_amount = game.categories.count()
        latest_patch = game_patches.order_by('-creation_date').first()
        try:
            latest_patch = latest_patch.creation_date
        except:
            latest_patch = "No patches"
        sidebar_games.append({
            'game': game,
            'patches_amount': game_patches_amount,
            'latest_patch': latest_patch,
            'categories_amount': game_categories_amount
        })
    
    top_5_categories = Category.objects.annotate(num_categories=Count('patchoption__patches')).order_by('-num_categories')[:5]
    
    sidebar_categories = []
    
    for category in top_5_categories:
        category_patches = Patch.objects.filter(patch_options__category=category)
        category_patches_amount = category_patches.count()
        base_game = category.base_game
        latest_patch = category_patches.order_by('-creation_date').first()
        try:
            latest_patch = latest_patch.creation_date
        except:
            latest_patch = "No patches"
        patch_options_amount = category.patchoption_set.count()
        sidebar_categories.append({
            'category': category,
            'patches_amount': category_patches_amount,
            'latest_patch': latest_patch,
            'base_game': base_game,
            'patch_options_amount': patch_options_amount
        })
    
        
    context = {
        'final_list' : final_patch_list,
        'paginated_list': paginated_patches,
        'top8categories': top_8_categories,
        'top8parentpatches': top_8_parent_patches,
        'top8games': top_8_games,
        'sidebar_categories': sidebar_categories,
        'sidebar_games': sidebar_games,
        'amountCat': len(top_8_categories),
        'amountPat': len(top_8_parent_patches),
        'sorting_criteria': sorting_criteria,
        'sorting_by': sorting_by,
        'extravars': merged_extravars
    }
    
    return render(request, html, context)

def filter(request, htmlkey=None, extravars={}):
    game_id = request.GET.get('selectedGame','any')
    category_id = request.GET.get('selectedCategory','any')
    patch_id = request.GET.get('selectedPatch','any')
    sorting_by = request.GET.get('selectedSorting','Downloads')
    sorting_order = request.GET.get('sorting_order','descending')
    selected_filter = request.GET.get('selected_filter','none')
    
    if htmlkey is None:
        if selected_filter and selected_filter != 'none':
            htmlkey = selected_filter
        elif game_id in ['none', 'any']:
            htmlkey = 'all'
        elif category_id in ['none', 'any']:
            htmlkey = 'base_game'
        elif patch_id in ['none', 'any']:
            htmlkey = 'category'
        else:
            htmlkey = 'base_patch'
    
    if selected_filter == 'base_game':
        category_id = 'any'
        patch_id = 'any'
    
    if selected_filter == 'category':
        patch_id = 'any'
    
    return main_filter(request, htmlkey, sorting_order, extravars=extravars, game_id=game_id, category_id=category_id, patch_id=patch_id, sorting_by=sorting_by)

def get_patch_list_only(request):
    htmlkey='patch_list_page'     
    return filter(request, htmlkey)

def load_modal(request):
    game_id = request.GET.get('selectedGame')
    category_id = request.GET.get('selectedCategory')
    patch_id = request.GET.get('selectedPatch')
    html='patches/main_modal.html'
    if game_id:
        html = 'patches/sidebar/first/sidebar_modal.html'
        game = Game.objects.get(id=game_id)
        context = {'element': game}
    elif category_id:
        html = 'patches/sidebar/second/sidebar_modal.html'
        category = Category.objects.get(id=category_id)
        game = category.base_game
        context={'element': category, 'hierarchy': get_category_hierarchy(category), 'game': game}
    elif patch_id:
        patch = Patch.objects.get(id=patch_id)
        patch_options = PatchOption.objects.filter(id__in=PatchData.objects.filter(patch=patch).values_list('field__patch_option', flat=True).distinct())
        context = {
            'element': patch,
            'patch_config': { po: PatchData.objects.filter(patch=patch, field__patch_option=po) for po in patch_options },
            'game': patch.get_base_game(),
            'latest_comments': PatchComment.objects.filter(patch=patch).order_by('-created')[:5]
        }
    else:
        context={'element': 'any'}

    return render(request, html, context)

def download_patch(request):
    patch = request.GET.get('patch')
    real_patch = Patch.objects.get(id=patch)
    patch_file_path = real_patch.download_link
    patch_file_name = f'{patch}.xdelta'
    
    if os.path.exists(patch_file_path):
        real_patch.downloads += 1
        real_patch.save()
        response = FileResponse(open(patch_file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{patch_file_name}"'
        return response
    else:
        raise Http404("File not found")
    
def modal_login(request):
    return render(request, 'account/modal_login.html')

def favorite_patch(request,patch_id):
    patch = get_object_or_404(Patch, id=patch_id)
    if not request.user.is_authenticated:
        print("Only logined users can favorite a patch!")
    else:
        patchfav_match = PatchFav.objects.filter(patch=patch, user=request.user)
        if patchfav_match.exists():
            patchfav_match.delete()
            if patch.favorites > 0:
                patch.favorites -= 1
                patch.save()
        else:
            PatchFav.objects.create(patch=patch, user=request.user)
            patch.favorites += 1
            patch.save()
            
    return render(request, 'generic/modal/components/modal_favorite_button.html', {'element': patch})

def add_patch_comment(request,patch_id):
    patch = get_object_or_404(Patch, id=patch_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            PatchComment.objects.create(
                patch=patch,
                author=request.user,
                comment=comment_text
            )
    return render(request, 'generic/modal/components/modal_comments.html', {'latest_comments': PatchComment.objects.filter(patch=patch).order_by('-created')[:5]})

def like_patch_comment(request,comment_id,dislike=False):
    comment = get_object_or_404(PatchComment, id=comment_id)
    if not request.user.is_authenticated:
        print("Only logined users can like a comment!")
    else:
        commentlike_match = PatchCommentLike.objects.filter(comment=comment, user=request.user)
        if commentlike_match.exists():
            current_value = commentlike_match.first().likeordislike
            if current_value != dislike:
                commentlike_match.delete()
            else:
                commentlike_match.update(likeordislike=not dislike)
        else:
            PatchCommentLike.objects.create(comment=comment, user=request.user, likeordislike=not(dislike))
    return render(request, 'generic/modal/components/modal_like_comment_button.html', {'element': comment, 'dislike':str(dislike)})

def dislike_patch_comment(request,comment_id):
    return like_patch_comment(request,comment_id,dislike=True)

def update_likes_patch_comment(request,comment_id):
    return render(request, 'generic/modal/components/modal_like_comment_button.html', {'element': get_object_or_404(PatchComment, id=comment_id), 'dislike':"False"})

def update_dislikes_patch_comment(request,comment_id):
    return render(request, 'generic/modal/components/modal_like_comment_button.html', {'element': get_object_or_404(PatchComment, id=comment_id), 'dislike':"True"})