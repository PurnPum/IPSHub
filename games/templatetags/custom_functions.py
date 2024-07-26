from django import template

from patches.models import Patch
from ..models import Game
from categories.models import Category
from django.db.models import Count

register = template.Library()

@register.filter
def concatstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.filter
def top3patches(element,criteria="Downloads"):
    if isinstance(element, Category):
        elements = Patch.objects.filter(patch_options__category=element)
    elif isinstance(element, Game):
        elements = Patch.objects.filter(patch_options__category__base_game=element)
    else:
        return "Error: Invalid argument"
    result = [{'element': patch, 'img': getpatchimg(patch)} for patch in elements.order_by('-'+criteria.lower()).distinct()[:3]]
    return result

@register.filter
def amountpatches(category):
    return Patch.objects.filter(patch_options__category=category).count()

@register.filter
def top3categories(game):
    categories = Category.objects.filter(base_game=game).annotate(num_patches=Count('patchoption__patches')).order_by('-num_patches')[:3]
    result = [{'element': category, 'img': category.image_ref, 'amount_patches': amountpatches(category)} for category in categories]
    return result

@register.filter
def latestpatch(element):
    if isinstance(element, Category):
        return Patch.objects.filter(patch_options__category=element).order_by('-creation_date').first()
    elif isinstance(element, Game):
        return Patch.objects.filter(patch_options__category__base_game=element).order_by('-creation_date').first()
    else:
        return "Error: Invalid argument"

@register.filter
def getpatchimg(patch):
    return patch.patch_options.first().category.image_ref

@register.filter
def undertowhite(arg1):
    return arg1.replace('_', ' ')
