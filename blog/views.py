from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, AddCommentForm, SearchForm

# Create your views here.


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector(
                "title", weight="A", config="english"
            ) + SearchVector("body", weight="B")
            search_query = SearchQuery(query, config="english")
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.3)
                .order_by("-rank")
            )
            if not results.exists():
                results = (
                    Post.published.annotate(
                        similarity=TrigramSimilarity("title", query),
                    )
                    .filter(similarity__gt=0.1)
                    .order_by("-similarity")
                )

    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )


def post_lists(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    try:
        post_lists = paginator.page(page_number)
    except EmptyPage:
        post_lists = paginator.page(paginator.num_pages)
        return render(request, "blog/post/list.html", {"posts": post_lists})

    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": post_lists, "tag": tag})


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

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    # similar_posts = post.tags.similar_objects()
    # tags = post.tags.all()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
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
