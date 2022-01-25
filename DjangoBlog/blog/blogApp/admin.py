from django.contrib import admin
from .models import Post, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)} # this create the slug field from the title field

admin.site.register(Post, PostAdmin)

