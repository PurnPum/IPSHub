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
    path('games/', g_views.games_list),
    path('categories/', c_views.categories_list),
    path('filter_categories_patches_and_main/', p_views.filter_categories_patches_and_main, name='filter_categories_patches_and_main'),
    path('filter_patches_and_main/', p_views.filter_patches_and_main, name='filter_patches_and_main')
]
