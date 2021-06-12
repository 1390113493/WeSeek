# -*- coding: utf-8 -*-
# @Time    : 2021/5/29 13:30
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *
urlpatterns = [
    path('init', InitGroupView.as_view()),
    path('join', JoinGroupView.as_view()),
    path('quit', CancelGroupView.as_view()),
    path('info', GroupInfoView.as_view()),
    path('list', GroupListView.as_view()),
    path('manage', GroupManagementView.as_view()),
]