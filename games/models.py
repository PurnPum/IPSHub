from django.db import models
import uuid

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image_ref = models.CharField(max_length=200)
    image_mini_ref = models.CharField(max_length=200)
    title = models.CharField(max_length=100, unique=True)
    release_date = models.DateField()
    developer = models.CharField(max_length=100)
    best_emulator_url = models.URLField(max_length=200, blank=True, null=True)
    best_emulator = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    extra_info = models.URLField(max_length=200)
    repository = models.URLField(max_length=200)

    def __str__(self):
        return self.title
