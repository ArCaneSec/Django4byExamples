from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_lists, name="list_collection"),
    path("<int:id>/", views.post_details, name="post_details"),
]
