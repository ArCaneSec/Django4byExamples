from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    """
    This model contains attributes about post table.
    """

    class Status(models.TextChoices):
        """
        Text choices class, You can choose between `DF` and `PB`
        """

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def get_absolute_url(self):
        return reverse(
            "blog:post_details",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def __str__(self):
        return self.title
