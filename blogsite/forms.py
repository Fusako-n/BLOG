from django import forms
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import bleach

from .models import Topic, Good


class HTMLField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        return bleach.clean(value, tags=settings.ALLOWED_TAGS, attributes=settings.ATTRIBUTES)


class TopicForm(forms.ModelForm):
    class Meta:
        model   = Topic
        fields  = ['title', 'category', 'tag', 'text']

    text = HTMLField()


class TopicCategoryForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['category']


class TopicTagForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['tag']


class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'text', 'author', 'category', 'tag']

    text = HTMLField()


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['topic', 'ip']