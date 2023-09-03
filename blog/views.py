from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import EmailPostForm, AddCommentForm

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
    comments = post.comments.filter(active=True)
    form = AddCommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def post_email(request, post_id):
    """
    This view is for sharing posts via email.
    """
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
           
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            print(post.get_absolute_url())
            subject = f"{data['name']} has recommended you to read {post.title}!"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{data['name']}'s comments: {data['comment']}"
            )
            send_mail(subject, message, data["email"], [data["to"]])
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = AddCommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
