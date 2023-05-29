from django.contrib import admin
from django.utils.html import format_html

from .models import Topic, Category, Tag
from .forms import TopicAdminForm


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'author', 'format_tag']
    list_filter = ['author']
    form = TopicAdminForm
    
    def format_tag(self, obj):
        tag_str = ''
        if obj.tag:
            for tag in obj.tag.all():
                tag_str += tag.name + ', '
            return format_html(f'<div>{tag_str}</div>')

admin.site.register(Topic, TopicAdmin)
admin.site.register(Category)
admin.site.register(Tag)