from django.shortcuts import render
from rest_framework.views import APIView

from activity.activities import get_activity_list
from common.search import search
from competition.competition_info import get_info_list
from competition.save_competition import save_ah_competition
from extensions.response import success, fail


class IndexView(APIView):
    """
    首页
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        rtype = self.request.GET.get('type')
        if rtype == 'banners' or rtype == 'competition':
            c_list = get_info_list(limit=4)
            res = c_list['list']
        elif rtype == 'activity':
            a_list = get_activity_list(limit=4)
            res = a_list['list']
        else:
            c_list = get_info_list(limit=4)
            a_list = get_activity_list(limit=4)
            res = {
                'banners': c_list['list'],
                'competition': c_list['list'],
                'activity': a_list['list']
            }

        return success('获得首页内容成功', res)


class SearchView(APIView):
    """
    搜索
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return fail('请输入搜索关键词')
        return success('获得搜索结果成功', search(keyword))


class SaveCompetitionInfo(APIView):
    """
    保存比赛信息到数据库
    """
    authentication_classes = []

    def get(self, *args, **kwargs):
        try:
            save_ah_competition()
            return success('更新比赛信息成功！')
        except:
            return fail('更新失败')
