from django.contrib import admin
from .models import Patch, PatchOption, PatchData, POField

admin.site.register(Patch)
admin.site.register(PatchOption)
admin.site.register(POField)
admin.site.register(PatchData)