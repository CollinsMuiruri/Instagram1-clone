from django.contrib import admin
from .models import Image,tag,Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'

class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('tag')
# Register your models here.
admin.site.register(Image)
admin.site.register(tag)
admin.site.register(Profile)
