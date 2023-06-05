from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリ名', max_length=20)
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    # idを文字列型に変更するモデルメソッド
    def str_id(self):
        return str(self.id)
    
    # 投稿数を数えるモデルメソッド
    def topic_amount(self):
        return Topic.objects.filter(category=self.id).count()


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=10)
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    title = models.CharField(verbose_name='タイトル', max_length=100)
    text = models.TextField(verbose_name='内容')
    author = models.CharField(verbose_name='書いた人', max_length=10)
    image = models.ImageField(upload_to='images/', blank=True, default='images/noimage.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    # いいねを数えるモデルメソッド
    def good_amount(self):
        return Good.objects.filter(topic=self.id).count()


class Good(models.Model):
    class Meta:
        unique_together = ('topic', 'ip')
    
    topic = models.ForeignKey(Topic, verbose_name='記事', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='IPアドレス')
