from django.db import models


class Post(models.Model):
    post_title = models.CharField(max_length=120)
    post_text  = models.TextField(blank=True, null=True)
