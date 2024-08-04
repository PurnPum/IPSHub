from django.db import models
import uuid
from django.contrib.auth.models import User
from django.forms import ValidationError

class Patch(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    parent_patch = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subpatches')
    name = models.CharField(max_length=100, unique=True)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    patch_options = models.ManyToManyField('PatchOption', related_name='patches', blank=False)
    download_link = models.URLField(max_length=500)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.parent_patch is not None and self.parent_patch in self.get_all_subpatches():
            raise ValidationError('The parent patch cannot be a subpatch of itself.')
        if self.parent_patch == self:
            raise ValidationError('The parent patch cannot be itself.')
        if len(self.get_game_titles()) > 1:
            raise ValidationError('The patch options assigned to this patch must all be for the same game.')
        
        
    def get_game_titles(self):
        base_game_titles = []
        for patch_option in self.patch_options.all():
            base_game_titles.append(patch_option.category.base_game.title)
        return list(set(base_game_titles))
    
    def get_all_subpatches(self):
        subpatches = [self]
        for subpatch in self.subpatches.all():
            subpatches.extend(subpatch.get_all_subpatches())
        return subpatches
    
class PatchOption(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE) 
    # In the case of a category getting removed, before doing so make sure all the patch options linked to this category or any of its sub-categories have been moved to a different category, or they will also get erased.
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    #github_issue = models.URLField(max_length=200) TODO

    def __str__(self):
        return self.name
    
class POField(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    field_type = models.CharField(max_length=100)
    code_file = models.CharField(max_length=200)
    initial_data = models.JSONField(blank=True)
    parent_field = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subfields')
    patch_option = models.ForeignKey('patches.PatchOption', on_delete=models.CASCADE)
    default_data = models.JSONField(blank=True)

    def __str__(self):
        return self.name
    
class PatchData(models.Model):
    patch = models.ForeignKey('patches.Patch', on_delete=models.CASCADE)
    field = models.ForeignKey('patches.POField', on_delete=models.CASCADE)
    data = models.JSONField(blank=False)
    
    def __str__(self):
        return self.data
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patch', 'field'], name='patchdata_identifier')
        ]