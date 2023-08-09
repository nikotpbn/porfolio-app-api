from django.contrib import admin
from portfolio import models


class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['name']


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ArtAdmin(admin.ModelAdmin):
    search_fields = ['title']
    filter_horizontal = ['characters']


admin.site.register(models.Character, CharacterAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Art, ArtAdmin)
