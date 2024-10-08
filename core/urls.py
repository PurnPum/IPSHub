"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from games import views as g_views
from categories import views as c_views
from patches import views as p_views

urlpatterns = [
    path('', p_views.patches),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/modal_login/' , p_views.modal_login, name='modal_login'),
    path('search/modal/' , p_views.search_modal, name='search_modal'),
    path('search/' , p_views.search_generic, name='search_generic'),
    path('patches/<uuid:patch_id>/favorite/', p_views.favorite_patch, name='favorite_patch'),
    path('patches/', p_views.patches, name='patches'),
    path('patches/filter/', p_views.filter, name='patch_filter'),
    path('patches/list/', p_views.get_patch_list_only, name='patch_list'),
    path('patches/modal/', p_views.load_modal, name='load_modal_patch'),
    path('patches/download/', p_views.download_patch, name='download_patch'),
    path('patch/<uuid:patch_id>/comments/add_comment/', p_views.add_patch_comment, name='add_patch_comment'),
    path('patch/comments/<uuid:comment_id>/like/', p_views.like_patch_comment, name='like_patch_comment'),
    path('patch/comments/<uuid:comment_id>/dislike/', p_views.dislike_patch_comment, name='dislike_patch_comment'),
    path('patch/comments/<uuid:comment_id>/update_likes/', p_views.update_likes_patch_comment, name='update_likes_patch_comment'),
    path('patch/comments/<uuid:comment_id>/update_dislikes/', p_views.update_dislikes_patch_comment, name='update_dislikes_patch_comment'),
    path('patch/<uuid:patch_id>/comments/refresh/', p_views.refresh_patch_comments, name='refresh_patch_comments'),
    path('patches/search/', p_views.search_patches, name='search_patches'),
    path('categories/search/', c_views.search_categories, name='search_categories'),
    path('games/', g_views.games_list, name='games'),
    path('games/filter/', g_views.main_filter, name='game_filter'),
    path('games/filter_patchgen/', g_views.main_filter_patchgen, name='game_filter_patchgen'),
    path('games/list/', g_views.get_game_list_only, name='game_list'),
    path('games/list_patchgen/', g_views.get_game_list_only_patchgen, name='game_list_patchgen'),
    path('games/modal/', g_views.load_modal, name='load_modal_game'),
    path('games/search/', g_views.search_games, name='search_games'),
    path('patch_generator/', p_views.patch_generator, name='patch_generator'),
    path('patch_generator/subcategories/', p_views.patch_generator_load_data, name='patch_generator_load_data'),
    path('patch_generator/generate_patch/', p_views.gather_form_data, name="gather_form_data"),
    path('patch_generator/current_progress/', p_views.get_progress_percentile, name="get_progress_percentile"),
    path('patch_generator/progress_bar/', p_views.get_progress_bar, name="get_progress_bar"),
]
