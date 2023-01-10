from datetime import datetime

from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(default=datetime.now())
