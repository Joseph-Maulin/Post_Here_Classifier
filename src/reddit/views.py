from django.shortcuts import render
from .post_form import PostForm
from .Reddit_API import Reddit_API
import praw
import os
import datetime


def home_view(request, *args, **kwargs):

    return render(request, "home.html")



def post_view(request, *args, **kwargs):

    r = Reddit_API()

    for x in r.get_user_posts("masktoobig"):
        print(x.title)
        print(x.created_utc)
        print(datetime.datetime.fromtimestamp(x.created_utc))
        for y in r.get_post_comments(x):
            print(y.body)

    form = PostForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)

    context = {
        "form" : form
    }
    return render(request, "post.html", context)
