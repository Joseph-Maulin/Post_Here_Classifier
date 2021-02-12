from django.shortcuts import render
from django.http import HttpResponse
from .post_form import PostForm
from .Reddit_API import Reddit_API
import praw
import os
import datetime
from .model.Load_Model_H5 import get_model
import json



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


def make_prediction(request, *args, **kwargs):

    m = get_model()

    post = {"post_title": "Only in 1989",
            "post_text" : "I'm absolutely losing my mind that credit scores weren't established in the US until 1989. We really are teh guinea pig generations for all the bad boomer ideas"}

    pred = m.make_prediction(post)

    return HttpResponse(pred)
