from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from activity.activities import get_activity_list, get_activity_detail, add_activity
from activity.collect import status, deal
from extensions.response import success, fail


class ActivityListView(APIView):
    """
    获得活动信息列表
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        page = int(self.request.GET.get('page', 1))
        limit = int(self.request.GET.get('page', 10))
        info_list = get_activity_list(page, limit)
        return success('获得活动信息列表成功', info_list)


class ActivityDetailView(APIView):
    """
    活动信息内容
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        a_id = int(self.request.GET.get('aid'), 0)
        if not a_id:
            return fail('请传递id')
        return success('获得内容成功', get_activity_detail(a_id))


class AddActivityView(APIView):
    """
        活动信息内容
        """
    authentication_classes = []

    def post(self, *args, **kwargs):
        title = self.request.POST.get('title')
        content = self.request.POST.get('content')
        host = self.request.POST.get('host')
        from_time = self.request.POST.get('from_time')
        to_time = self.request.POST.get('to_time')
        if add_activity(title, content, host, from_time, to_time):
            return success('成功添加活动信息')
        else:
            return fail('添加活动信息失败')


class CollectView(APIView):
    """
    收藏活动
    """

    def get(self, *args, **kwargs):
        uid = self.request.user
        aid = self.request.GET.get('aid')
        return success('成功获得收藏状态', data={
            'status': status(uid, aid)
        })

    def post(self, *args, **kwargs):
        uid = self.request.user
        aid = self.request.POST.get('aid')
        return success(deal(uid, aid))
