from django import forms
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import bleach

from .models import Post

class HTMLField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        return bleach.clean(value, tags=settings.ALLOWED_TAGS, attributes=settings.ATTRIBUTES)


class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['title', 'category', 'tag', 'content']

    content = HTMLField()


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category']


class PostTagForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tag']


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category', 'tag']

    content = HTMLField()