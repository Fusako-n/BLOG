from django.shortcuts import render, redirect
from django.views import View

from .models import Category, Tag, Post


class IndexView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        categories = Category.objects.all()
        context = {'posts': posts, 'categories': categories}
        return render(request, 'blogsite/index.html', context)

index = IndexView.as_view()