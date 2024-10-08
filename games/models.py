from django.db import models
import uuid

from core.utils import normalize_string
from categories.models import Category
from patches.models import Patch

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image_ref = models.CharField(max_length=200)
    image_mini_ref = models.CharField(max_length=200)
    title = models.CharField(max_length=200, unique=True)
    normalized_name = models.CharField(max_length=200)
    release_date = models.DateField()
    developer = models.CharField(max_length=100)
    best_emulator_url = models.URLField(max_length=200, blank=True, null=True)
    best_emulator = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    extra_info = models.URLField(max_length=200)
    repository = models.URLField(max_length=200)
    patch_file_name = models.CharField(max_length=200)
    patch_sha = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_string(self.title)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_patches(self):
        return Patch.objects.filter(patch_options__category__base_game=self).distinct()
    
    def get_categories(self):
        return Category.objects.filter(base_game=self)
    
    def get_latest_patch(self):
        return self.get_patches().latest('creation_date')
