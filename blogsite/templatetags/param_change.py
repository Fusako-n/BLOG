from django import template
register = template.Library()

@register.simple_tag()
def url_replace(request, key, value):
    copied = request.GET.copy()
    copied[key] = value
    return copied.urlencode()


@register.simple_tag()
def tag_check(request, tag):
    tags = request.GET.getlist('tag')  # 検索でチェックされたtagのidを取得
    # print(tags)  # チェックされているタグのid（文字列型）
    if str(tag.id) in tags:
        return 'checked'
    else:
        return ''