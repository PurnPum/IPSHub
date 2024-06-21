from django.db import models
import uuid

from django.forms import ValidationError

class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    base_game = models.ForeignKey('games.Game', on_delete=models.CASCADE, null=False, blank=False, related_name='categories')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    image_ref = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.parent_category is not None and self.parent_category in self.get_all_children():
            raise ValidationError('The parent category cannot be a subcategory of itself.')
        if self.parent_category == self:
            raise ValidationError('The parent category cannot be itself.')
        if self.parent_category is not None and self.parent_category.base_game != self.base_game:
            raise ValidationError('The parent category must be from the same game.')
        
        
    def get_all_parents(self):    
        parents = []
        current_category = self
        while current_category.parent_category is not None:
            parents.append(current_category.parent_category)
            current_category = current_category.parent_category
        return parents
        
    def get_all_children(self):
        children = []
        for subcategory in self.subcategories.all():
            children.append(subcategory)
            children.extend(subcategory.get_all_children())
        return children

        
            
