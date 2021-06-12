# -*- coding: utf-8 -*-
# @Time    : 2021/5/29 13:30
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *

urlpatterns = [
    path('list', CompetitionListView.as_view()),
    path('detail', CompetitionDetailView.as_view()),
    path('collect', CollectView.as_view()),
]