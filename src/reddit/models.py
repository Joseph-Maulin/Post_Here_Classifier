from django.db import models


class Post(models.Model):
    post_title = models.TextField(max_length=120)
    post_text  = models.TextField(blank=True, null=True)


class User(models.Model):
    user_name = models.TextField(max_length=40)
