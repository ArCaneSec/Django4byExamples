from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list_collection"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_details,
        name="post_details",
    ),
    path("<int:post_id>/share/", views.post_email, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
]
