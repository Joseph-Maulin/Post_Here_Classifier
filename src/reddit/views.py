from django.shortcuts import render
from .post_form import PostForm


def home_view(request, *args, **kwargs):

    return render(request, "home.html")



def post_view(request, *args, **kwargs):

    form = PostForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)

    context = {
        "form" : form
    }
    return render(request, "post.html", context)
