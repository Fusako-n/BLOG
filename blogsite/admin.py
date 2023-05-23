from django.contrib import admin
from django.utils.html import format_html

from .models import Post, Category, Tag
from .forms import PostAdminForm


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'author', 'created_at', 'updated_at', 'format_tag']
    list_filter = ['author']
    form = PostAdminForm
    
    def format_tag(self, obj):
        tag_str = ''
        if obj.tag:
            for tag in obj.tag.all():
                tag_str += tag.name + ','
            return format_html('<div>{}</div>', tag_str)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)