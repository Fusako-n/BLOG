from django.db import models
import bs4


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
    
    # 同じカテゴリのトピックを取得するモデルメソッド
    def topics(self):
        return Topic.objects.filter(category=self.id)


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
    
    # summernote装飾をしていても一覧表示でレイアウトが崩れないようにするモデルメソッド
    def plain_text(self):
        soup = bs4.BeautifulSoup(self.text, 'html.parser')
        return soup.get_text()  # HTMLタグを除去した文字列を返す
    
    # summernoteにセットされた画像を抜き取ってサムネイルにするモデルメソッド
    def text_thumbnail(self):
        soup = bs4.BeautifulSoup(self.text, 'html.parser')
        img_elems = soup.select('img')
        if len(img_elems) >= 1:
            return str(img_elems[0])  # 一番最初のimgタグを抜き取る
        else:
            return '<img src="/media/images/noimage.png" alt="サムネイル" style="max_width:100%; max-height:10rem;">'


class Good(models.Model):
    class Meta:
        unique_together = ('topic', 'ip')
    
    topic = models.ForeignKey(Topic, verbose_name='記事', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='IPアドレス')
