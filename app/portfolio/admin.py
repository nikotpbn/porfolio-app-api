from django.contrib import admin
from portfolio import models

class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.Character, CharacterAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Artist, ArtistAdmin)
admin.site.register(models.Art)
