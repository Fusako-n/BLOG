from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Category, Tag, Topic, Good
from .forms import TopicForm, TopicCategoryForm, TopicTagForm, GoodForm, CustomUserEditForm
from users.models import CustomUser


class IndexView(View):
    def get(self, request, *args, **kwargs):
        query = Q()
        if 'search' in request.GET:
            words = request.GET['search'].replace('　', ' ').replace('、', ' ').replace(',', ' ').split(' ')
            for word in words:
                if word == '':
                    continue
                query &= Q(text__icontains=word)
        
        # カテゴリ検索
        form = TopicCategoryForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()
            if cleaned['category']:
                query &= Q(category=cleaned['category'])
        topics = Topic.objects.filter(query).order_by('-created_at')
        
        # タグ検索
        form = TopicTagForm(request.GET)
        if form.is_valid():
            cleaned = form.clean()
            selected_tags = cleaned['tag']
            for tag in selected_tags:
                topics = [topic for topic in topics if tag in topic.tag.all()]
        
        # ページネーション
        paginator = Paginator(topics, 6)
        if 'page' in request.GET:
            topics = paginator.get_page(request.GET['page'])
        else:
            topics = paginator.get_page(1)
        
        categories = Category.objects.all()
        tags = Tag.objects.all()
        form = TopicForm  # summernoteを入れたい時にTopicFormのオブジェクトをcontextに入れてレンダリング
        context = {'topics': topics, 'categories': categories, 'tags': tags, 'form': form}
        return render(request, 'blogsite/index.html', context)
    
    # def post(self, request, *args, **kwargs):
    #     form = TopicForm(request.POST)
    #     if not form.is_valid():
    #         values = form.errors.get_json_data().values()
    #         for value in values:
    #             for v in value:
    #                 messages.error(request, v['message'])
    #         return redirect('blogsite:index')
    #     form.save()
    #     messages.info(request, '投稿内容を保存しました')
    #     return redirect('blogsite:index')

index = IndexView.as_view()


class TopicDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        context['topic'] = Topic.objects.filter(id=pk).first()
        return render(request, 'blogsite/topic_detail.html', context)

topic_detail = TopicDetailView.as_view()


class TopicDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        if topic:
            topic.delete()
        else:
            print('対象のデータは見つかりませんでした')
        return redirect('blogsite:index')

topic_delete = TopicDeleteView.as_view()


class TopicGoodView(View):
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        
        # X-Forwarded-For(XFF)ヘッダー（クライアントの送信元IPアドレスを特定する標準となっているヘッダー）を参照して転送経路のIPアドレスを取得
        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        # XFFヘッダーがある場合は転送経路の先頭要素を取得
        if ip_list:
            ip = ip_list.split(',')[0]
        # なければ直接接続なのでRemote-Addrヘッダーを参照
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        dic = {}
        dic['ip'] = ip
        dic['topic'] = pk
        form = GoodForm(dic)
        
        # unique_togetherをしているので、すでにいいねをしている場合は保存されない
        if form.is_valid():
            form.save()
        else:
            print('すでにいいねしています')
            
            # いいねの解除
            # good = Good.objects.filter(topic=pk, ip=ip).first()
            # good.delete()
        
        return redirect('blogsite:topic_detail', pk)

topic_good = TopicGoodView.as_view()


# 認証している場合に限り、このビューを実行する（認証していない場合はログインページにリダイレクト）
class TopicEditView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        form = TopicForm(instance=topic)
        context = {'topic': topic, 'categories': categories, 'tags': tags, 'form': form}
        return render(request, 'blogsite/topic_edit.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        topic = Topic.objects.filter(id=pk).first()
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            messages.info(request, '投稿内容を変更しました')
        else:
            messages.info(request, 'バリデーションNGです')
        return redirect('blogsite:index')

topic_edit = TopicEditView.as_view()


class TopicCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TopicForm()
        context = {'form': form}
        return render(request, 'blogsite/topic_create.html', context)
    
    def post(self, request, *args, **kwargs):
        form = TopicForm(request.POST, request.FILES)  # 画像もバリデーションして保存
        if not form.is_valid():
            values = form.errors.get_json_data().values()
            for value in values:
                for v in value:
                    messages.error(request, v['message'])
            return redirect('blogsite:index')
        form.save()
        messages.info(request, '投稿内容を保存しました')
        return redirect('blogsite:index')

topic_create = TopicCreateView.as_view()


class MypageView(View):
    def get(self, request, *args, **kwargs):
        # user = CustomUser.objects.filter(id=request.user.id).first()
        return render(request, 'blogsite/mypage.html')

mypage = MypageView.as_view()


class MypageEditView(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.user.id).first()
        form = CustomUserEditForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, 'blogsite/mypage_edit.html', context)
    
    def post(self, request, *args, **kwargs):
        # 編集対象のモデルオブジェクトを特定
        user = CustomUser.objects.filter(id=request.user.id).first()
        
        # フォームクラスでバリデーション
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, 'プロフィール内容を更新しました')
        else:
            messages.info(request, 'バリデーションNGです')
        return redirect('blogsite:mypage')

mypage_edit = MypageEditView.as_view()