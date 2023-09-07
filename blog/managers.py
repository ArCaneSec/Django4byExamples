from django.db import models
from . import models as m


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=m.Post.Status.PUBLISHED)
