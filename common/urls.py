# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 16:53
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *

urlpatterns = [
    path('savec', SaveCompetitionInfo.as_view()),
    path('index', IndexView.as_view()),
    path('search', SearchView.as_view()),
]