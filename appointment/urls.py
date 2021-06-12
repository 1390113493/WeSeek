# -*- coding: utf-8 -*-
# @Time    : 2021/6/5 16:53
# @Author  : HUII
# @FileName: urls.py
# @Software: PyCharm
from django.urls import path
from .views import *

urlpatterns = [
    path('submit', AppointmentSubmitView.as_view()),
    path('cancel', AppointmentDeleteView().as_view()),
    path('list', AppointmentListView.as_view()),
    path('allow', AllowAppointmentView.as_view()),
]