from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Category, Tag, Post
from .forms import PostForm, PostCategoryForm, PostTagForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        query = Q()
        if 'search' in request.GET:
            words = request.GET['search'].replace('　', ' ').replace('、', ' ').replace(',', ' ').split(' ')
            for word in words:
                if word == '':
                    continue
                query &= Q(content__icontains=word)
        
        # カテゴリ検索
        form = PostCategoryForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()
            if cleaned['category']:
                query &= Q(category=cleaned['category'])
        posts = Post.objects.filter(query).order_by('-created_at')
        
        # タグ検索
        form = PostTagForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()
            selected_tags = cleaned['tag']
            for tag in selected_tags:
                posts = [post for post in posts if tag in post.tag.all()]
        
        # ページネーション
        paginator = Paginator(posts, 6)
        if 'page' in request.GET:
            posts = paginator.get_page(request.GET['page'])
        else:
            posts = paginator.get_page(1)
        
        categories = Category.objects.all()
        tags = Tag.objects.all()
        form = PostForm
        context = {'posts': posts, 'categories': categories, 'tags': tags, 'form': form}
        return render(request, 'blogsite/index.html', context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if not form.is_valid():
            values = form.errors.get_json_data().values()
            for value in values:
                for v in value:
                    messages.error(request, v['message'])
            return redirect('blogsite:index')
        form.save()
        messages.info(request, '投稿内容を保存しました！')
        return redirect('blogsite:index')

index = IndexView.as_view()


class PostDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        if post:
            post.delete()
        else:
            print('対象のデータは見つかりませんでした')
        return redirect('blogsite:index')

post_delete = PostDeleteView.as_view()


class PostEditView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        form = PostForm(instance=post)
        context = {'post': post, 'categories': categories, 'tags': tags, 'form': form}
        return render(request, 'blogsite/post_edit.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, '投稿内容を変更しました！')
        else:
            messages.info(request, 'バリデーションNG')
        return redirect('blogsite:index')

post_edit = PostEditView.as_view()