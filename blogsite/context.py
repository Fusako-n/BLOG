from .models import Tag, Category

def search_context(request):
    context = {}
    context['CATEGORIES'] = Category.objects.all()
    context['TAGS'] = Tag.objects.all()
    
    return context