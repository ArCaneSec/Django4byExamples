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
]
