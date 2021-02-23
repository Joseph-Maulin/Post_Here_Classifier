
# django
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.clickjacking import xframe_options_exempt

# forms
from .forms.post_form import PostForm
from .forms.user_form import UserForm

# models
# from .model.Load_Model_H5 import get_model

# reddit
from .Reddit_API import get_reddit_api
import praw

# python
import os
import datetime
import json
import multiprocessing



def home_view(request, *args, **kwargs):
    return render(request, "home.html")


def post_view(request, *args, **kwargs):
    form = PostForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            print(request.POST)
            request.session['post_title'] = request.POST['post_title']
            request.session['post_text'] = request.POST['post_text']
            return redirect('/predict')

    else:
        context = {
            "form" : form
        }
        return render(request, "post.html", context)


def make_prediction(request, *args, **kwargs):
    m = get_model()

    post = {"post_title": title,
            "post_text" : text}

    pred = m.make_prediction(post)

    return HttpResponse(pred)


@xframe_options_exempt
def user_view(request, *args, **kwargs):
    form = UserForm(request.POST or None)

    r = get_reddit_api()
    posts = None

    context = {
        "form" : form,
        "posts" : posts
    }

    if request.method == 'POST' and form.is_valid():

        user = request.POST["user_name"]

        p1 = multiprocessing.Process(target = r.build_comment_history_html, args=[user])
        p2 = multiprocessing.Process(target = r.build_post_numbers_history_html, args=[user])
        p3 = multiprocessing.Process(target = r.build_user_recent_subreddit_numbers, args=[user])

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

        context["posts"] = r.get_user_posts(request.POST['user_name'])

    return render(request, "user.html", context)


def reddit_test(request):
    r = get_reddit_api()

    response = {}
    for i, x in enumerate(r.get_user_posts("masktoobig")):
        response[i] = {}
        response[i]["post_title"] = x.title
        response[i]["post_selftext"] = x.selftext
        response[i]["created_date"] = str(datetime.datetime.fromtimestamp(x.created_utc))
        response[i]["comments"] = []
        for y in r.get_post_comments(x):
            response[i]['comments'].append(y.body)

    return HttpResponse(json.dumps(response))
    # return render(request, "reddit_test.html", response)



#endpage
