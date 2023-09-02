from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm

# Create your views here.


def post_lists(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    try:
        post_lists = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        return render(request, "blog/post/list.html", {"posts": posts})

    except PageNotAnInteger:
        post_lists = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": post_lists})


def post_details(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    print(post.title)
    return render(request, "blog/post/detail.html", {"post": post})


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"

def post_or_share_email(request, post_id):
    post = get_object_or_404(Post, post_details)

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        
    else:
        form = EmailPostForm()

    return render(request, "blog/post/share.html", {"post": post, "form": form})