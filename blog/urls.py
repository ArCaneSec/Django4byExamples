from django.urls import path
from .feeds import LatestPostsFeed
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_lists, name="list_collection"),
    path("<str:tag_slug>", views.post_lists, name="list_collection_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_details,
        name="post_details",
    ),
    path("<int:post_id>/share/", views.post_email, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.post_search, name="post_search"),
]
