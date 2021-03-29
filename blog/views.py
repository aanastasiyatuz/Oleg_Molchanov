from django.shortcuts import render
from .models import Post

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', locals())
