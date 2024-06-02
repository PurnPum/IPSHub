from django.db import models
import uuid

from django.forms import ValidationError

class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    base_game = models.ForeignKey('games.Game', on_delete=models.CASCADE, null=False, blank=False, related_name='categories')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    image_ref = models.CharField(max_length=200)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
            
