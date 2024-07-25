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
from django.urls import path
from games import views as g_views
from categories import views as c_views
from patches import views as p_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patches/', p_views.patches_list),
    path('patches/filter/', p_views.filter, name='patch_filter'),
    path('patches/list/', p_views.get_patch_list_only, name='patch_list'),
    path('patches/modal/', p_views.load_modal, name='load_modal_patch'),
    path('games/', g_views.games_list),
    path('games/filter/', g_views.main_filter, name='game_filter'),
    path('games/filter_patchgen/', g_views.main_filter_patchgen, name='game_filter_patchgen'),
    path('games/list/', g_views.get_game_list_only, name='game_list'),
    path('games/list_patchgen/', g_views.get_game_list_only_patchgen, name='game_list_patchgen'),
    path('games/modal/', g_views.load_modal, name='load_modal_game'),
    path('patch_generator/', p_views.patch_generator, name='patch_generator')
]
