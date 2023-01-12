from datetime import datetime
from django.contrib.auth.models import User

from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(unique=True)
    created = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "posts"
        ordering = ["-created"]

    def __str__(self):
        return f"Post: {self.title[:20]}"
