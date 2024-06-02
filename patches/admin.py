from django.contrib import admin
from .models import Patch, PatchOption

admin.site.register(Patch)
admin.site.register(PatchOption)