"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reddit.views import home_view, post_view, make_prediction, user_view, reddit_test


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name="home"),
    path("post/", post_view, name="post"),
    path("predict/", make_prediction, name="prediction"),
    path("user/", user_view, name="user"),
    path("reddit_test/", reddit_test, name="reddit_test")
]
