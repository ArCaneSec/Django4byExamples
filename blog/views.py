from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post

# Create your views here.


def post_lists(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_details(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    print(post.title)
    return render(request, "blog/post/detail.html", {"post": post})
