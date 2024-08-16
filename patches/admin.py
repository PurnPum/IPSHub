from django.contrib import admin
from .models import Patch, PatchOption, PatchData, POField, DiffFile, PatchFav

admin.site.register(Patch)
admin.site.register(PatchOption)
admin.site.register(POField)
admin.site.register(PatchData)
admin.site.register(DiffFile)
admin.site.register(PatchFav)