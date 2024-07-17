from django import template

from patches.models import Patch
from categories.models import Category
from django.db.models import Count

register = template.Library()

@register.filter
def concatstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.filter
def topXpatches(game,amount):
    return Patch.objects.filter(patch_options__category__base_game=game).order_by('-downloads').distinct()[:amount]

@register.filter
def amountpatches(category):
    return Patch.objects.filter(patch_options__category=category).count()

@register.filter
def topXcategories(game,amount):
    return Category.objects.filter(base_game=game).annotate(num_patches=Count('patchoption__patches')).order_by('-num_patches')[:amount]

@register.filter
def latestpatch(game):
    return Patch.objects.filter(patch_options__category__base_game=game).order_by('-creation_date').first()

@register.filter
def patchimgfromgame(patch):
    return patch.patch_options.first().category.image_ref