from django import forms
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import bleach
from bleach.css_sanitizer import CSSSanitizer

from .models import Topic, Good


class HTMLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        return bleach.clean(value, tags=settings.ALLOWED_TAGS, attributes=settings.ATTRIBUTES, css_sanitizer=CSSSanitizer())


class TopicForm(forms.ModelForm):
    class Meta:
        model   = Topic
        fields  = ['title', 'category', 'tag', 'text', 'image']

    text = HTMLField()


class TopicCategoryForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['category']


class TopicTagForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['tag']


# 管理画面用
class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'text', 'author', 'category', 'tag']

    text = HTMLField()


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['topic', 'ip']