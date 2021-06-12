# -*- coding: utf-8 -*-
# @Time    : 2021/5/22 13:51
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('info', UserInfoView.as_view(), name='info'),
    path('uinfo', CommonUserInfo.as_view(), name='uinfo'),
    path('home', HomeView.as_view(), name='home'),
    path('test', TestView.as_view(), name='test'),
]