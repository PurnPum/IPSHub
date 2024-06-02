from django.db import models
import uuid
from django.contrib.auth.models import User

class Patch(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    parent_patch = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subpatches')
    name = models.CharField(max_length=100)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    patch_options = models.ManyToManyField('PatchOption', related_name='patches', blank=False)
    
    def __str__(self):
        return self.name
    
    
    
class PatchOption(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE) 
    # In the case of a category getting removed, before doing so make sure all the patch options linked to this category or any of its sub-categories have been moved to a different category, or they will also get erased.
    code_file = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    #github_issue = models.URLField(max_length=200) TODO

    def __str__(self):
        return self.name