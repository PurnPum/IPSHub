from django import template
from django.urls import reverse

from patches.models import Patch, PatchFav, PatchCommentLike
from ..models import Game
from ..utils import get_category_hierarchy
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

@register.filter
def getpatchurl(patch):
    return reverse('download_patch')+'?patch='+str(patch.id)

@register.filter
def patchgenpreseturl(patch):
    return reverse('patch_generator')+'?selectedPatch='+str(patch.id)

@register.filter
def getpatchgengameurl(game):
    return reverse('patch_generator')+'?selectedGame='+str(game.id)

@register.filter
def getpatchgencaturl(category,game):
    return reverse('patch_generator')+'?selectedGame='+str(game.id)+'&selectedCategory='+str(category.id)

@register.filter
def iscategoryparent(cat1,cat2):
    hierarchy = get_category_hierarchy(cat1)
    while 'children' in hierarchy and len(hierarchy['children']) > 0:
        if cat2 == hierarchy['element']:
            return True
        hierarchy = hierarchy['children'][0]
    return False

@register.filter
def whichcategoryisparent(listcats,cat2):
    result = []
    for category in listcats:
        if iscategoryparent(category,cat2):
            result.append(category)
    if len(result) > 0:
        result.append(cat2)
    return result

@register.filter
def hasuserlikedpatch(patch,user):
    return PatchFav.objects.filter(patch=patch,user=user).exists()

@register.filter
def hasuserinteractedwithcomment(comment,user):
    return PatchCommentLike.objects.filter(comment=comment,user=user).exists()

@register.filter
def howhasuserratedcomment(comment,user):
    if PatchCommentLike.objects.filter(comment=comment,user=user).exists():
        return PatchCommentLike.objects.get(comment=comment,user=user).likeordislike
    else:
        return 'None'
    
@register.filter
def likespercomment(comment):
    return PatchCommentLike.objects.filter(comment=comment,likeordislike=True).count()

@register.filter
def dislikespercomment(comment):
    return PatchCommentLike.objects.filter(comment=comment,likeordislike=False).count()

@register.filter
def getgamefrompatch(patch):
    return patch.get_base_game()

@register.filter
def getgamefromcategory(category):
    return category.base_game