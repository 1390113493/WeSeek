from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from competition.collect import status, deal
from competition.competition_info import get_info_list, get_info_detail
from extensions.response import success, fail


class CompetitionListView(APIView):
    """
    比赛信息列表
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        page = int(self.request.GET.get('page', 1))
        limit = int(self.request.GET.get('page', 10))
        category = int(self.request.GET.get('category', 0))
        info_list = get_info_list(page, limit, category)
        return success('获得比赛信息列表成功', info_list)


class CompetitionDetailView(APIView):
    """
    比赛信息内容
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        c_id = int(self.request.GET.get('cid'), 0)
        if not c_id:
            return fail('请传递id')
        return success('获得内容成功', get_info_detail(c_id))


class CollectView(APIView):
    """
    收藏比赛
    """
    def get(self, *args, **kwargs):
        uid = self.request.user
        cid = self.request.GET.get('cid')
        return success('成功获得收藏状态', data={
            'status': status(uid, cid)
        })

    def post(self, *args, **kwargs):
        uid = self.request.user
        cid = self.request.POST.get('cid')
        return success(deal(uid, cid))