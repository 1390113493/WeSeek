# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 16:52
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *

urlpatterns = [
    path('list', ActivityListView.as_view()),
    path('detail', ActivityDetailView.as_view()),
    path('add', AddActivityView.as_view()),
    path('collect', CollectView.as_view()),
]