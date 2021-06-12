# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 21:41
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *
urlpatterns = [
    path('unread', UnreadMessageListView.as_view()),
    path('list', MessageListView.as_view()),
    path('system', SystemMessageView.as_view()),
    path('detail', MessageDetailView.as_view()),
    path('send', SendMessageView.as_view()),
]