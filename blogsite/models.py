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
    def post_amount(self):
        return Post.objects.filter(category=self.id).count()


class Tag(models.Model):
    name = models.CharField(verbose_name='タグ名', max_length=10)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField(verbose_name='内容')
    author = models.CharField(verbose_name='書いた人', max_length=10, default='匿名')
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
