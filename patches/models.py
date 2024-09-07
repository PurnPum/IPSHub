import hashlib
import json
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.forms import ValidationError
from core.utils import normalize_string

class Patch(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    parent_patch = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subpatches')
    name = models.CharField(max_length=200, unique=True)
    normalized_name = models.CharField(max_length=200)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    patch_options = models.ManyToManyField('PatchOption', related_name='patches', blank=False) # TODO Discard this relationship, since we can go through PatchData and POFields to have a relation
    download_link = models.TextField(max_length=500)
    patch_hash = models.CharField(max_length=64, editable=False, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.normalized_name = normalize_string(self.name)
        if self.pk is None:
            super(Patch, self).save(*args, **kwargs)
        else:
            self.patch_hash = self.generate_patch_code()
            super(Patch, self).save(*args, **kwargs)
    
    def clean(self):
        if self.parent_patch is not None and self.parent_patch in self.get_all_subpatches():
            raise ValidationError('The parent patch cannot be a subpatch of itself.',code='self_sub_parent')
        if self.parent_patch == self:
            raise ValidationError('The parent patch cannot be itself.',code='self_parent')
        if len(self.get_games()) > 1:
            raise ValidationError('The patch options assigned to this patch must all be for the same game.',code='multiple_game_patch')
        existing_patches = Patch.objects.filter(name=self.name).exclude(id=self.id)
        if existing_patches.exists():
            raise ValidationError('A patch with this name already exists.',code='duplicated_name')
        #if not self.patch_options.exists():
        #    raise ValidationError('A patch must have at least one patch option.',code='empty_patch') TODO
        
    def generate_patch_code(self):
        return get_hash_code_from_patchDatas(PatchData.objects.filter(patch=self).order_by('field__id'))
    
    def get_base_game(self):
        return self.patch_options.first().category.base_game
        
    def get_games(self):
        base_games = []
        for patch_option in self.patch_options.all():
            base_games.append(patch_option.category.base_game)
        return list(set(base_games))
    
    def get_all_subpatches(self, visited=None):
        if visited is None:
            visited = set()

        if self in visited:
            return []
        subpatches = [self]
        visited.add(self)
        for subpatch in self.subpatches.all():
            if subpatch not in visited:
                subpatches.extend(subpatch.get_all_subpatches(visited=visited))
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
    initial_data = models.JSONField(blank=True)
    parent_field = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subfields')
    patch_option = models.ForeignKey('patches.PatchOption', on_delete=models.CASCADE)
    default_data = models.JSONField(blank=True)

    def __str__(self):
        return self.name
    
class DiffFile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    filename = models.CharField(max_length=200)
    original_file = models.CharField(max_length=200)
    trigger_value = models.CharField(max_length=10000)
    field = models.ForeignKey('patches.POField', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.filename
    
class PatchData(models.Model):
    patch = models.ForeignKey('patches.Patch', on_delete=models.CASCADE)
    field = models.ForeignKey('patches.POField', on_delete=models.CASCADE)
    data = models.CharField(blank=False,max_length=10000)
    
    def __str__(self):
        return self.data
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patch', 'field'], name='patchdata_identifier')
        ]
        
class PatchFav(models.Model):
    patch = models.ForeignKey('patches.Patch', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patch', 'user'], name='patchfav_identifier')
        ]
    
    def __str__(self):
        return self.user.username+'-'+self.patch.name
    
class PatchComment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    patch = models.ForeignKey('patches.Patch', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    
    def __str__(self):
        try:
            return f'{self.author.username}: {self.comment}'
        except:
            return f'<deleted> : {self.comment}'
        
    def getLikes(self):
        return PatchCommentLike.objects.filter(comment=self, likeordislike=True).count()
    
    def getDislikes(self):
        return PatchCommentLike.objects.filter(comment=self, likeordislike=False).count()
        
class PatchCommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('patches.PatchComment', on_delete=models.CASCADE)
    likeordislike = models.BooleanField()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['comment', 'user'], name='patchcommentlike_identifier')
        ]
    
    def __str__(self):
        if self.likeordislike:
            return self.user.username+' liked comment '+self.comment.comment
        else:
            return self.user.username+' disliked comment '+self.comment.comment
        
def get_hash_code_from_patchDatas(patch_data):
    data_list = []
    for pd in patch_data:
        data_tuple = (str(pd.field.id), pd.data)
        data_list.append(data_tuple)
    
    data_string = json.dumps(data_list, sort_keys=True)
    patch_code = hashlib.sha256(data_string.encode('utf-8')).hexdigest()
    return patch_code