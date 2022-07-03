from django.contrib import admin
from .models import Location, Tag, SideImage
# Register your models here.
admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(SideImage)