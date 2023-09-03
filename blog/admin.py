from django.contrib import admin
from .models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created_at", "publish", "author__id"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "body", "created", "updated", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "post"]
    date_hierarchy = "created"
    ordering = ["created", "active"]
